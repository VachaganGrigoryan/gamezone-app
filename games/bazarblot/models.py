import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from games.bazarblot.choices import GamePoint, CombinationType, CardSuit
from games.bazarblot.fields import CardField


class Team(models.Model):
    players = models.ManyToManyField(get_user_model(), max_length=2)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'bazarblot_teams'

        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ['-pk']


class Table(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier of the board.'),
    )

    teams = models.ManyToManyField(
        Team,
        related_name='tables_teams'
    )
    winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    players_order = models.JSONField(blank=True, null=True)

    max_points = models.IntegerField(choices=GamePoint.choices, default=GamePoint.MEDIUM)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
        help_text=_('The date and time when the board was created.'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
        help_text=_('The date and time when the board was updated.'),
    )
    is_ended = models.BooleanField(
        default=False,
        verbose_name=_('Is ended'),
        help_text=_('The status of the game.'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active'),
        help_text=_('The status of the board.'),
    )

    class Meta:
        db_table = 'bazarblot_tables'

        verbose_name = _('Table')
        verbose_name_plural = _('Tables')
        ordering = ['-pk']

    def re_order(self):
        players_order = self.players_order
        if isinstance(players_order, list):
            self.players_order = players_order[1:] + players_order[:1]
        else:
            # ToDo: need to check if above code is working correct
            print(self.players_order, type(self.players_order))


class Round(models.Model):
    table = models.ForeignKey(Table, related_name='rounds', on_delete=models.CASCADE)

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active'),
        help_text=_('The status of the board.'),
    )

    trump_suit = models.CharField(
        max_length=10,
        choices=CardSuit.choices,
        null=True,
        blank=True,
    )

    order = models.IntegerField()

    class Meta:
        db_table = 'bazarblot_rounds'

        constraints = [
            models.UniqueConstraint(
                fields=['table', 'is_active'],
                condition=Q(is_active=True),
                name='unique_one_table_round_is_active'
            )
        ]

        verbose_name = _('Round')
        verbose_name_plural = _('Rounds')
        ordering = ['-pk']


class RoundPlayersCards(models.Model):
    round = models.OneToOneField(Round, related_name='players_cards', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    cards = ArrayField(
        CardField(),
        size=8,
    )

    class Meta:
        db_table = 'bazarblot_rounds_players_cards'

        constraints = [
            models.UniqueConstraint(
                fields=['round', 'player'],
                name='unique_one_round_players'
            )
        ]

        verbose_name = _('Players Cards')
        verbose_name_plural = _('Players Cards')
        ordering = ['-pk']


class RoundScore(models.Model):
    round = models.OneToOneField(Round, related_name='score', on_delete=models.CASCADE)

    team_one_value = models.IntegerField()
    team_two_value = models.IntegerField()


class Bazar(models.Model):
    round = models.ForeignKey(Round, related_name='bazars', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    card = CardField()
    value = models.CharField()

    order = models.IntegerField()

    class Meta:
        db_table = 'bazarblot_bazars'

        verbose_name = _('Bazar')
        verbose_name_plural = _('Bazars')
        ordering = ['-pk']


class Contra(models.Model):
    bazar = models.OneToOneField(Bazar, related_name='contra', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = 'bazarblot_contras'

        verbose_name = _('Contra')
        verbose_name_plural = _('Contras')
        ordering = ['-pk']


class ReContra(models.Model):
    contra = models.OneToOneField(Contra, related_name='re_contra', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = 'bazarblot_recontras'

        verbose_name = _('Re Contra')
        verbose_name_plural = _('Re Contras')
        ordering = ['-pk']


class Combination(models.Model):
    round = models.ForeignKey(Round, related_name='combinations', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    type = models.CharField(
        choices=CombinationType.choices,
        max_length=12,
    )
    value = ArrayField(
        CardField(),
        size=5,
    )

    is_passed = models.BooleanField(default=True)
    is_shown = models.BooleanField(default=False)

    class Meta:
        db_table = 'bazarblot_combinations'

        verbose_name = _('Combination')
        verbose_name_plural = _('Combinations')
        ordering = ['-pk']


class Hand(models.Model):
    round = models.ForeignKey(Round, related_name='hands', on_delete=models.CASCADE)

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active'),
        help_text=_('The status of the board.'),
    )
    order = models.IntegerField()

    class Meta:
        db_table = 'bazarblot_hands'

        constraints = [
            models.UniqueConstraint(
                fields=['round', 'is_active'],
                condition=Q(is_active=True),
                name='unique_one_round_hand_is_active'
            )
        ]

        verbose_name = _('Hand')
        verbose_name_plural = _('Hands')
        ordering = ['-pk']


class HandTrick(models.Model):
    hand = models.ForeignKey(Round, related_name='tricks', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    card = CardField()

    order = models.IntegerField()

    class Meta:
        db_table = 'bazarblot_hand_tricks'

        verbose_name = _('Hand Trick')
        verbose_name_plural = _('Hand Tricks')
        ordering = ['-pk']


class HandScore(models.Model):
    hand = models.OneToOneField(Hand, related_name='score', on_delete=models.CASCADE)
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    value = models.IntegerField()
