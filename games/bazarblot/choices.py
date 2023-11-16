from django.db import models
from django.utils.translation import gettext_lazy as _


class GamePoint(models.IntegerChoices):
    """
    The length of a board
    """
    SMALL = 151, _('Small')
    MEDIUM = 301, _('Medium')
    LARGE = 501, _('Large')


class CombinationType(models.TextChoices):
    Terz = 'Terz'
    Fifty = 'Fifty'
    Hundred = 'Hundred'
    FourCards = 'FourCards'


class CardSuit(models.TextChoices):
    Clubs = ('♧', '♣'), 'C'
    Diamonds = ('♢', '♦'), 'D'
    Hearts = ('♡', '♥'), 'H'
    Spades = ('♤', '♠'), 'S'
