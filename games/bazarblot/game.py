import json
from dataclasses import dataclass
from enum import Enum
from functools import partial
from itertools import product
from random import shuffle
from typing import List, Dict, Callable


class Suit(Enum):
    Clubs = ('♧', '♣'), 'Clubs'
    Diamonds = ('♢', '♦'), 'Diamonds'
    Hearts = ('♡', '♥'), 'Hearts'
    Spades = ('♤', '♠'), 'Spades'
    Ace = ('A', 'A'), 'Ace'


class Rank(Enum):
    seven = 7, '7'
    eight = 8, '8'
    nine = 9, '9'
    ten = 10, '10'
    Jack = 11, 'J'
    Queen = 12, 'Q'
    King = 13, 'K'
    Ace = 14, 'A'


class CType(Enum):
    Terz = 'Terz'
    Fifty = 'Fifty'
    Hundred = 'Hundred'
    FourCards = 'FourCards'


@dataclass(slots=True)
class Card:
    rank: Rank
    suit: Suit

    def to_dict(self):
        return {
            'rank': self.rank.value[0],
            'suit': self.suit.value[1],
        }

    def to_json(self):
        return self.rank.value[0], self.suit.value[1]

    def __str__(self):
        return f'Card<|{self.rank.value[0]}-{self.suit.value[0][1]}|>'


@dataclass
class Combination:
    type: CType
    value: List[Card]


class CombinationBaseValidator:
    def __init__(self, combination: Combination, player_cards: List[Card]):
        self.combination = combination
        self.player_cards = player_cards
        self._errors = {}

    def validate(self):
        for card in self.combination.value:
            if card not in self.player_cards:
                self._errors.update({
                    'invalid_card': f'Player have not {card}.'
                })
                return False
        return True


class ComboValidator(CombinationBaseValidator):

    def __init__(self, card_count, remain, combination: Combination, player_cards: List[Card]):
        super().__init__(combination, player_cards)
        self.card_count = card_count
        self.remain = remain

    def validate(self):  # Todo:  add error information into self._errors dict
        return self.validate_count() and self.validate_suit() and self.validate_sequence() and super().validate()

    def validate_count(self):
        return len(self.combination.value) == self.card_count

    def validate_suit(self):
        return len(set([c.suit for c in self.combination.value])) == 1

    def validate_sequence(self):
        return sum(c.rank.value[0] for c in self.combination.value) % self.card_count == self.remain


class FourCardValidator(CombinationBaseValidator):

    def validate(self):
        return self.validate_count() and self.validate_suit() and self.validate_sequence() and super().validate()

    def validate_count(self):
        return len(self.combination.value) == 4

    def validate_suit(self):
        return len(set([c.suit for c in self.combination.value])) == 4

    def validate_sequence(self):
        return len(set([c.rank for c in self.combination.value])) == 1


Validators: Dict[CType, Callable] = {
    CType.Terz: partial(ComboValidator, 3, 0),
    CType.Fifty: partial(ComboValidator, 4, 2),
    CType.Hundred: partial(ComboValidator, 5, 0),
    CType.FourCards: FourCardValidator,
}


class Game:

    def __init__(self, player_cards: List[Card]):
        self.player_cards = player_cards

    @staticmethod
    def build_deck() -> List[Card]:
        deck = [Card(r, s) for r, s in product(Rank, Suit)]
        shuffle(deck)
        return deck

    def validate_combinations(self, combination: Combination):
        validator = Validators.get(combination.type)(combination, self.player_cards)

        if validator.validate():
            return True

        raise ValueError('Incorrect')


class BazarValidation:
    def __init__(self, bazars, player):
        self.bazars = bazars
        self.player = player

    def get_max_bazar(self):
        return max(7, 7, *[int(b.value) for b in self.bazars])

    def get_last_bazar(self):
        return self.bazars[-1] if self.bazars else None

    def has_contra(self):
        return hasattr(self.get_last_bazar(), "contra") if self.bazars else None

    def validate(self, card, value):
        if value == "PASS":
            return True
        if not self.has_contra() and int(value) > int(self.get_max_bazar()):
            if len(self.bazars) > 3 and self.bazars[-4].value == "PASS":
                if self.bazars[-2].card.suit != card.suit or self.bazars[-2].value == "PASS":
                    return False
            return True
        return False


if __name__ == '__main__':

    g = Game(player_cards=[
        Card(
            rank=Rank.seven,
            suit=Suit.Hearts
        ),
        Card(
            rank=Rank.eight,
            suit=Suit.Hearts
        ),
        Card(
            rank=Rank.nine,
            suit=Suit.Hearts
        ),
        Card(
            rank=Rank.ten,
            suit=Suit.Hearts
        )
    ])
    is_valid = g.validate_combinations(Combination(
        type=CType.Fifty,
        value=[
            Card(
                rank=Rank.seven,
                suit=Suit.Hearts
            ),
            Card(
                rank=Rank.eight,
                suit=Suit.Hearts
            ),
            Card(
                rank=Rank.nine,
                suit=Suit.Hearts
            ),
            Card(
                rank=Rank.ten,
                suit=Suit.Hearts
            )
        ]
    ))

    print(is_valid)

    # d = g.build_deck()
    #
    # players_cards = {}
    # for i in range(4):
    #     players_cards[i] = d[i * 8:(i + 1) * 8]
    #
    # print(json.dumps(players_cards, default=lambda o: o.to_json(), indent=4))
