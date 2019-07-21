import random

from enum import Enum, IntEnum
from functools import total_ordering


class FourPlayerGame(Enum):
    DECK = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    PLAYER_3 = 3
    PLAYER_4 = 4


class Suit(Enum):
    BLANK = 0
    HEARTS = 1
    SPADES = 2
    DIAMONDS = 3
    CLUBS = 4
    JOKER = 5


class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    SMALL_JOKER = 14
    BIG_JOKER = 15

    def __str__(self):
        return self.name


RANK_EXCLUDE_JOKER = list(Rank)[:-2]

SUITS_EXCLUDE_BLANK_JOKER = list(Suit)[1:-1]

FOUR_PLAYER_TEAM_1 = [FourPlayerGame.PLAYER_1, FourPlayerGame.PLAYER_3]
FOUR_PLAYER_TEAM_2 = [FourPlayerGame.PLAYER_2, FourPlayerGame.PLAYER_4]


# One Card
@total_ordering
class Card:
    def __init__(self, rank, suit, owner, is_in_hand=False):
        self.rank = rank
        self.suit = suit
        self.owner = owner
        self.is_in_hand = is_in_hand

    def __str__(self):
        return '[{}\'s card, {} {}, is_in_hand: {}]'.format(
            self.owner, self.suit, self.rank, self.is_in_hand)

    def __eq__(self, other):
        return ((self.rank, self.suit) == (other.rank, other.suit))

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return ((self.rank, self.suit) < (other.rank, other.suit))

    def get_owner(self, player):
        self.owner = player
        self.is_in_hand = True

    def play(self):
        if self.is_in_hand:
            self.is_in_hand = False
        else:
            raise Exception(
                '{} tried to play the card that is not in hand', self.owner)

    # returns true if this card is larger than the other card's rank
    def compare_rank(self, other):
        return self.rank >= other.rank

    @classmethod
    def get_joker_cards(cls):
        return [cls(Rank.SMALL_JOKER, Suit.JOKER), cls(Rank.BIG_JOKER, Suit.JOKER)]


# Deck of 52/54 Cards
class Deck:
    def __init__(self, with_joker, card_class=Card):
        self.cards = [card_class(rank, suit) for rank in RANK_EXCLUDE_JOKER
                      for suit in SUITS_EXCLUDE_BLANK_JOKER]
        if with_joker:
            self.cards += card_class.get_joker_cards()

    def get_cards(self):
        return self.cards

    def __str__(self):
        return str([str(card) for card in self.cards])


# All the cards used in one game
class GameDeck:
    def __init__(self, cards, num_players):
        self.cards = cards
        self.num_players = num_players

    def shuffle(self):
        return random.shuffle()

    def pop(self):
        return self.cards.pop()

    def __str__(self):
        return str([str(card) for card in self.cards])


class Player:
    def __init__(self, name, player, hand_cards):
        self.name = name
        self.player = player
        self.hand_cards = hand_cards

    def draw(self, game_deck):
        card = game_deck.pop()
        card.get_owner(self)
        self.hand_cards.append(card)

    def __str__(self):
        return '[{}: {}, hand_cards: {}]'.format(
            self.owner, self.name, self.hand_cards)


class Game:
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck
        self.new_rounds = []
        self.played_rounds = []


class GameSet:
    def __init__(self):
        self.games = []
