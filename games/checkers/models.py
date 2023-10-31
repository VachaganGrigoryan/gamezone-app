import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from games.checkers.choices import BoardLength
from django.utils.translation import gettext_lazy as _


class Board(models.Model):
    """
    A game board
    """
    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier of the board.'),
    )

    owner = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        verbose_name=_('Owner'),
        help_text=_('The owner of the board.'),
        related_name='boards_owner',
    )
    players = models.ManyToManyField(
        'account.User',
        verbose_name=_('Players'),
        help_text=_('The players of the board.'),
        related_name='boards_players',
        through='BoardPlayers',
    )
    winner = models.ForeignKey(
        'account.User',
        on_delete=models.SET_NULL,
        verbose_name=_('Winner'),
        help_text=_('The winner of the board.'),
        related_name='boards_winner',
        blank=True,
        null=True
    )
    queue = models.ForeignKey(
        'account.User',
        on_delete=models.SET_NULL,
        verbose_name=_('Queue'),
        help_text=_('The queue of the board.'),
        related_name='boards_queue',
        blank=True,
        null=True
    )

    grid = ArrayField(
        ArrayField(
            models.IntegerField(blank=True, null=True),
            blank=True,
            null=True
        ),
        verbose_name=_('Grid'),
        help_text=_('The grid of the board.'),
        default=list,
        blank=True,
        null=True
    )
    length = models.IntegerField(
        verbose_name=_('Length'),
        help_text=_('The length of the board.'),
        choices=BoardLength.choices,
        default=BoardLength.EIGHT
    )

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
        db_table = 'checkers_boards'

        verbose_name = _('Checkers board')
        verbose_name_plural = _('Checkers boards')
        ordering = ['-pk']

    def __str__(self):
        return f'{self.guid}'

    def get_next_queue(self, current):
        players = self.players.all()
        return players[0] == current and players[1] or players[0]


class BoardPlayers(models.Model):
    STONE_CHOICES = [
        (2, 'White'),
        (3, 'Black'),
    ]

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
    )
    stone_type = models.PositiveSmallIntegerField(
        choices=STONE_CHOICES,
        default=2,
    )

    class Meta:
        unique_together = ('board', 'stone_type')


class Histories(models.Model):
    """
        A game history
    """

    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier of the history.'),
    )

    board = models.ForeignKey(
        'checkers.Board',
        on_delete=models.CASCADE,
        verbose_name=_('Board'),
        help_text=_('The board of the history.'),
        related_name='histories',
    )

    player = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        verbose_name=_('Player'),
        help_text=_('The player of the history.'),
        related_name='histories',
    )

    grid_changes = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=2,
        ),
        verbose_name=_('Grid changes'),
        help_text=_('Move points of the history.'),
        null=True,
    )

    taken_points = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=2,
        ),
        verbose_name=_('Taken points'),
        help_text=_('The taken points of the history.'),
        blank=True,
        null=True
    )

    played_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
        help_text=_('The date and time when the history was created.'),
    )

    class Meta:
        db_table = 'checkers_histories'

        verbose_name = _('Checkers history')
        verbose_name_plural = _('Checkers histories')
        ordering = ['-pk']

    def __str__(self):
        return f'{self.guid}'
