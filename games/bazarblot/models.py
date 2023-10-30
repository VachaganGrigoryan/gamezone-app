from django.db import models
from django.conf import settings



class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Card(models.Model):
    SUIT_CHOICES = (
        ('Hearts', 'Hearts'),
        ('Diamonds', 'Diamonds'),
        ('Clubs', 'Clubs'),
        ('Spades', 'Spades'),
    )

    VALUE_CHOICES = (
        ('A', 'A'),
        ('10', '10'),
        ('K', 'K'),
        ('Q', 'Q'),
        ('J', 'J'),
        ('9', '9'),
        ('8', '8'),
        ('7', '7'),
    )

    suit = models.CharField(max_length=10, choices=SUIT_CHOICES)
    value = models.CharField(max_length=2, choices=VALUE_CHOICES)


class Game(models.Model):
    name = models.CharField(max_length=100)  # Name of the game
    start_date = models.DateTimeField(auto_now_add=True)  # Date and time when the game started
    is_finished = models.BooleanField(default=False)  # Flag to indicate if the game has finished
    winning_team = models.CharField(max_length=20, null=True,
                                    blank=True)  # Name of the winning team (if the game is finished)
    current_round = models.IntegerField(default=1)  # The current round of the game
    max_points = models.IntegerField(default=301)  # Maximum points required to win the game


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    trump_suit = models.CharField(max_length=10, choices=Card.SUIT_CHOICES, null=True, blank=True)
    dealer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='round_dealer')  # Player who is the dealer for the round
    current_player = models.ForeignKey(Player, on_delete=models.CASCADE,  related_name='round_current_player')  # Player whose turn it is in the round
    round_number = models.IntegerField()  # Round number within the game
    is_completed = models.BooleanField(default=False)  # Flag to indicate if the round is completed


class Trick(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card_played = models.ForeignKey(Card, on_delete=models.CASCADE)


class Combination(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    combination_type = models.CharField(max_length=10)  # '4 cards', '100', '50', 'Terz'
    trump_card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True,
                                   blank=True,related_name='combination_trump_card')  # Trump card of the combination
    cards_in_combination = models.ManyToManyField(Card, related_name='combinations_in_cards')  # Cards in the combination
    is_sharpened = models.BooleanField(default=False)  # Flag to indicate if the combination is sharpened


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    points = models.IntegerField()


class Quanch(models.Model):
    player_quanching = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='quanch_player_quanching')
    trump_suit = models.CharField(max_length=10, choices=Card.SUIT_CHOICES)
    x_points = models.IntegerField()
    y_points = models.IntegerField()
    is_successful = models.BooleanField()
    quanch_type = models.CharField(max_length=20,
                                   choices=(('Quanch', 'Quanch'), ('Sharpened Quanch', 'Sharpened Quanch')))
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player_sharpening = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, related_name='quanch_player_sharpening')
    sharpened_x_points = models.IntegerField(null=True, blank=True)
    sharpened_y_points = models.IntegerField(null=True, blank=True)

