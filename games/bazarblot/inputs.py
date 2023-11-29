import strawberry

from games.bazarblot.game import Rank, Suit


@strawberry.input
class CardInput:
    rank: strawberry.enum(Rank)
    suit: strawberry.enum(Suit)

    def to_dict(self):
        return {
            'rank': self.rank.value[0],
            'suit': self.suit.value[1],
        }
