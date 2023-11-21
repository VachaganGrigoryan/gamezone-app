from bazarblot.models import Rating,Player
import logging
from django.utils import timezone
def is_valid_rate_action(new_rate,current_rate):
    if current_rate >= new_rate:
        return False
    if current_rate=="contra" and new_rate not in ("recontra","pass"):
        return False
    else:
        return True

def add_rating(player,card_type,new_rate,current_rate):
    if  is_valid_rate_action(player,card_type,new_rate,current_rate):
        rating=Rating(player=player,card_type=card_type,rate=new_rate)
        rating.save()
    else:
        logging.logger.warning(f"Invalid rating attempt by player {player} for card type {card_type}: {new_rate}")

def is_rating_completed(game):
    return  Player.objects.filter(game=game).count()==Rating.objects.filter(player_game=game).count()

def start_game(game):
    if is_rating_completed(game):
        first_rating= Rating.objects.filter(player__game=game).order_by('id').first()
        if first_rating:
            first_player=first_rating.player
            game.current_player = first_player
            game.start_date = timezone.now()
            game.save()
        else:
            pass

def extract_card_info(card_str):
    suits = {'♠': 'Spades', '♥': 'Hearts', '♦': 'Diamonds', '♣': 'Clubs', '♤': 'Spades', '♡': 'Hearts', '♢': 'Diamonds', '♧': 'Clubs'}
    values = {'7': '7', '8': '8', '9': '9', '10': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'}

    suit_symbol=card_str[0]
    card_value=card_str[1:]

    card_type=suits.get(suit_symbol)
    card_name=values.get(card_value)

   

    return card_type,card_name
cards = ['♠7', '♥7', '♦7', '♣7', '♤7', '♡7', '♢7', '♧7', '♠8', '♥8', '♦8', '♣8', '♤8', '♡8', '♢8', '♧8', '♠9', '♥9', '♦9', '♣9', '♤9', '♡9', '♢9', '♧9', '♠10', '♥10', '♦10', '♣10', '♤10', '♡10', '♢10', '♧10', '♠J', '♥J', '♦J', '♣J', '♤J', '♡J', '♢J', '♧J', '♠Q', '♥Q', '♦Q', '♣Q', '♤Q', '♡Q', '♢Q', '♧Q', '♠K', '♥K', '♦K', '♣K', '♤K', '♡K', '♢K', '♧K', '♠A', '♥A', '♦A', '♣A', '♤A', '♡A', '♢A', '♧A']


