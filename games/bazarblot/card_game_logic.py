import logging
from django.utils import timezone
from .models import Rating, Game, Player, Card, Trick, Combination
from random import random


class BazaarBlotGame:
    def __init__(self):
        self.players = []  # List of player instances
        self.current_round = 1
        self.max_points = 301
        self.trump_suit = None
        self.dealer = None
        self.current_player = None
        self.tricks = []
        self.combinations = []
        self.scores = {}  # Player scores stored as {player: score}
        self.caput = None  # Stores the player who makes a caput

    def start_game(self, player_data):
        # Initialize the game with player data
        for player_info in player_data:
            player = Player.objects.create(name=player_info["name"])
            self.players.append(player)

        self.dealer = self.players[0]  # Assign the dealer for the first round
        self.current_player = self.dealer  # Start the first round with the dealer

    def determine_trump_suit(self, player_declarations):
        # Create a dictionary to store the total declarations for each suit
        suit_declarations = {
            'Hearts': 0,
            'Diamonds': 0,
            'Clubs': 0,
            'Spades': 0,
        }

        # Calculate total declarations for each suit
        for declaration in player_declarations:
            suit = declaration['suit']
            points = declaration['points']

            if suit in suit_declarations:
                suit_declarations[suit] += points

        # Determine the suit with the highest total declarations
        trump_suit = max(suit_declarations, key=suit_declarations.get)

        # Set the trump suit for the round
        self.trump_suit = trump_suit

    def determine_winning_player(self, trick):
        if not trick:
            return None

        leading_suit = trick.cards[0].suit

        trick.cards.sort(key=lambda card: (card.suit != self.trump_suit, card.rank), reverse=True)

        winning_card = trick.cards[0]

        winning_player = trick.get_player(winning_card)

        return winning_player

    def shuffle_and_deal(self):
        # Implement logic to shuffle and deal cards to players
        # Create and shuffle a deck of cards
        deck = [Card(suit=suit, value=value) for suit in Card.SUIT_CHOICES for value in Card.VALUE_CHOICES]
        random.shuffle(deck)

        # Deal cards to players
        for i in range(len(self.players)):
            player = self.players[i]
            player.hand.add(deck[i * 8:(i + 1) * 8])

    def play_card(self, player, card):
        # Implement logic for players to take turns and play cards
        trick = self.get_current_trick()
        if self.is_valid_card_play(player, card, trick):
            trick.add_card(player, card)

            if len(trick.cards) == len(self.players):
                self.complete_trick()

    def is_valid_card_play(self, player, card, trick):
        if not trick:
            return True  # First card in the trick is always valid

        leading_suit = trick.cards[0].suit
        player_hand = player.hand.all()

        # Check if the card follows the suit of the leading card (if any)
        if card.suit == leading_suit:
            if any(c.suit == leading_suit for c in player_hand):
                return True
            return False

        # Check if the player has to play a trump card based on the round's trump suit
        if self.trump_suit and card.suit == self.trump_suit:
            if any(c.suit == self.trump_suit for c in player_hand):
                return True
            return False

        if not trick.cards:
            return True  # No capturing rules apply on the first play in a trick

        # Implement your game's capturing rules here
        for trick_card in trick.cards:
            if card.rank == trick_card.rank:
                # Implement capturing logic here
                trick.cards.remove(trick_card)
                trick.cards.remove(card)
                return True

        return False

    def complete_trick(self):
        # Implement logic to determine the winning card in the trick and update scores
        trick = self.get_current_trick()
        winning_card = self.get_winning_card(trick)
        winning_player = trick.get_player(winning_card)
        self.scores[winning_player] += 1

        if len(winning_player.hand.all()) == 0:
            # Check for caput (winning all the cards)
            if len(self.players) == 4:
                self.caput = winning_player
                self.scores[winning_player] += 250
            else:
                self.scores[winning_player] += 10

        # Start the next trick
        self.start_new_trick()

    def get_next_player(self):
        current_player_index = self.players.index(self.current_player)
        next_player_index = (current_player_index + 1) % len(self.players)
        next_player = self.players[next_player_index]
        return next_player

    def start_new_trick(self):
        # Initialize a new trick for the current round
        trick = Trick(round=self.get_current_round(), player=self.get_next_player())
        trick.save()
        self.tricks.append(trick)

    def get_current_trick(self):
        # Return the current trick in the round
        return self.tricks[-1]

    def get_winning_card(self, trick):
        # Implement logic to determine the winning card based on the trump suit and card ranking
        leading_suit = trick.cards[0].suit

        # Sort the cards in descending order considering trump rules
        trick.cards.sort(key=lambda card: (card.suit != self.trump_suit, card.rank), reverse=True)

        return trick.cards[0]

    def declare_combination(self, player, combination_type, trump_card, cards):
        # Implement logic for players to declare combinations
        combination = Combination(player=player, combination_type=combination_type, trump_card=trump_card)
        combination.save()
        combination.cards_in_combination.add(*cards)
        self.combinations.append(combination)

    def check_game_over(self):
        for player, score in self.scores.items():
            if score >= self.max_points:
                return True
        return False

    def determine_caput_winner(self):
        for player, score in self.scores.items():
            if score == 162:
                return player

        return None

    def prepare_for_next_round(self):
        self.current_round += 1

        self.tricks = []
        self.combinations = []

        dealer_index = self.players.index(self.dealer)
        if dealer_index < len(self.players) - 1:
            self.dealer = self.players[dealer_index + 1]
        else:
            self.dealer = self.players[0]

        self.current_player = self.dealer

        self.shuffle_and_deal()

    def calculate_scores(self):
        # Iterate through rounds to calculate scores
        for round in self.rounds:
            # Initialize round scores
            round_scores = {player: 0 for player in self.players}

            # Calculate scores from tricks won
            for trick in round.tricks:
                winning_player = self.determine_winning_player(trick)
                round_scores[winning_player] += 1  # Adjust score based on tricks won

            # Calculate scores from combinations
            for player in round.declarations:
                for combination in player.combinations:
                    if combination.is_valid:
                        round_scores[player] += combination.calculate_points()

            # Add the round scores to the overall scores
            for player, score in round_scores.items():
                self.scores[player] += score

        # Check for caput
        caput_winner = self.determine_caput_winner()
        if caput_winner:
            self.scores[caput_winner] += 50

        # Check for game-over conditions
        if self.check_game_over():
            self.is_finished = True

        # Continue to the next round or end the game
        self.current_round += 1
        if not self.is_finished:
            self.prepare_for_next_round()

    def is_game_over(self):
        # Implement logic to check if the game is over
        return any(score >= self.max_points for score in self.scores.values())

    def get_current_round(self):
        return self.current_round


def is_valid_rate_action(player, card_type, new_rate, current_rate):
    if current_rate >= new_rate:
        return False
    if current_rate == "contra" and new_rate not in ("recontra", "pass"):
        return False
    else:
        return True


def add_rating(player, card_type, new_rate, current_rate):
    if is_valid_rate_action(player, card_type, new_rate, current_rate):
        rating = Rating(player=player, card_type=card_type, rate=new_rate)
        rating.save()
    else:
        logging.logger.warning(f"Invalid rating attempt by player {player} for card type {card_type}: {new_rate}")


def is_rating_completed(game):
    return Player.objects.filter(game=game).count() == Rating.objects.filter(player_game=game).count()


def start_game(game):
    if is_rating_completed(game):
        first_rating = Rating.objects.filter(player__game=game).order_by('id').first()
        if first_rating:
            first_player = first_rating.player
            game.current_player = first_player
            game.start_date = timezone.now()
            game.save()
        else:
            pass


def extract_card_info(card_str):
    suits = {'♠': 'Spades', '♥': 'Hearts', '♦': 'Diamonds', '♣': 'Clubs', '♤': 'Spades', '♡': 'Hearts', '♢': 'Diamonds',
             '♧': 'Clubs'}
    values = {'7': '7', '8': '8', '9': '9', '10': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'}

    suit_symbol = card_str[0]
    card_value = card_str[1:]

    card_type = suits.get(suit_symbol)
    card_name = values.get(card_value)

    return card_type, card_name


if __name__ == '__main__':
    cards = ['♠7', '♥7', '♦7', '♣7', '♤7', '♡7', '♢7', '♧7', '♠8', '♥8', '♦8', '♣8', '♤8', '♡8', '♢8', '♧8', '♠9', '♥9',
             '♦9', '♣9', '♤9', '♡9', '♢9', '♧9', '♠10', '♥10', '♦10', '♣10', '♤10', '♡10', '♢10', '♧10', '♠J', '♥J',
             '♦J',
             '♣J', '♤J', '♡J', '♢J', '♧J', '♠Q', '♥Q', '♦Q', '♣Q', '♤Q', '♡Q', '♢Q', '♧Q', '♠K', '♥K', '♦K', '♣K', '♤K',
             '♡K', '♢K', '♧K', '♠A', '♥A', '♦A', '♣A', '♤A', '♡A', '♢A', '♧A']
    for card_str in cards:
        card_type, card_name = extract_card_info(card_str)
