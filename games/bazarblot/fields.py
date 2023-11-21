from dataclasses import dataclass

from django.db.models import JSONField

from games.bazarblot.game import Rank, Suit


@dataclass(slots=True)
class Card:
    rank: Rank
    suit: Suit

    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit,
        }


class CardField(JSONField):

    def from_db_value(self, value, expression, connection):
        db_val = super().from_db_value(value, expression, connection)

        if db_val is None:
            return db_val

        return Card(**db_val)

    def get_prep_value(self, value):
        dict_value = value.to_dict()
        prep_value = super().get_prep_value(dict_value)
        return prep_value
