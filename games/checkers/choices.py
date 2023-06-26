from django.db import models
from django.utils.translation import gettext_lazy as _


class BoardLength(models.IntegerChoices):
    """
    The length of a board
    """
    EIGHT = 8, _('Eight')
    TEN = 10, _('Ten')
