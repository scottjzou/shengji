import logging

from enum import IntEnum

from generic_models import Card, Deck, FourPlayerEnum, GameDeck, \
    RANK_EXCLUDE_JOKER, SUITS_EXCLUDE_BLANK_JOKER, Suit

logging.basicConfig(level=logging.DEBUG)


class TrumpStatus(IntEnum):
    VICE = 0
    PLAYED = 1
    TRUMP = 2


class ShengJiRank(IntEnum):
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
    DOMINANT = 14
    TRUNP_DOMINANT = 15
    SMALL_JOKER = 16
    BIG_JOKER = 17

    def __str__(self):
        return self.name


class ShengJiCard(Card):
    def __init__(self, rank, suit=Suit.BLANK, owner=FourPlayerEnum.DECK,
                 is_in_hand=False, is_score=False, is_dominant=False, is_trump_suit=False):
        super().__init__(rank, suit, owner, is_in_hand)
        self.is_score = is_score
        self.is_dominant = is_dominant
        self.actual_rank = self.rank
        self.is_trump_suit = is_trump_suit
        self.is_trump = False

    def __str__(self):
        return ('[{}\'s card, {} {}, is_in_hand: {}, is_score: {}, is_trump: {},'
                'is_trump_suit: {}, is_dominant: {}, actual_rank: {}]').format(
            self.owner, self.suit, self.rank, self.is_in_hand, self.is_score, self.is_trump,
            self.is_trump_suit, self.is_dominant, self.actual_rank)

    def set_trump(self, is_trump_suit):
        self.is_trump_suit = is_trump_suit
        self.is_trump = True if self.is_trump_suit else False
        if self.is_dominant:
            self.is_trump = True
            if self.is_trump_suit:
                self.actual_rank = ShengJiRank.TRUNP_DOMINANT
            else:
                self.actual_rank = ShengJiRank.DOMINANT

    @classmethod
    def get_joker_cards(cls):
        return [
            cls(ShengJiRank.SMALL_JOKER, Suit.JOKER, is_trump_suit=True),
            cls(ShengJiRank.BIG_JOKER, Suit.JOKER, is_trump_suit=True)
        ]

    @classmethod
    def get_dominant_cards(cls, dominant_rank):
        return [cls(dominant_rank, suit, is_dominant=True) for suit in SUITS_EXCLUDE_BLANK_JOKER]

    def compare_trump(self, other, playing_suit):
        if self.is_trump == other.is_trump:
            if not self.is_trump:
                if self.suit == playing_suit:
                    return 1
                elif other.suit == playing_suit:
                    return -1
            return 0
        elif self.is_trump and not other.is_trump:
            return 1
        elif not self.is_trump and other.is_trump:
            return -1
        return 0

    def compare_rank(self, other, is_debug=True):
        if is_debug:
            print('rank comparison: ' + self.actual_rank >= other.actual_rank)
        return self.actual_rank >= other.actual_rank

    # returns True if this card is larger than the other card
    # self is the first card that gets played
    def compare(self, other, playing_suit, is_debug=True):
        if is_debug:
            print(self)
            print(other)
            print(playing_suit)
        trump_status = self.compare_trump(other, playing_suit)
        if is_debug:
            print(trump_status)
        if trump_status != 0:
            return trump_status > 0
        return self.compare_rank(other)


class ShengJiDeck(Deck):
    def __init__(self, dominant_rank=ShengJiRank.TWO):
        rank_exclude_dominant = RANK_EXCLUDE_JOKER
        rank_exclude_dominant.remove(dominant_rank)
        self.cards = [ShengJiCard(rank, suit) for rank in rank_exclude_dominant
                      for suit in SUITS_EXCLUDE_BLANK_JOKER]
        self.cards += ShengJiCard.get_joker_cards()
        self.cards += ShengJiCard.get_dominant_cards(dominant_rank)


class ShengJiGameDeck(GameDeck):
    def __init__(self):
        shengji_cards = 2 * ShengJiDeck().get_cards()
        super().__init__(shengji_cards, 4)
