import logging

from enum import IntEnum

from generic_models import Card, FourPlayerEnum, SUITS_EXCLUDE_BLANK_JOKER, Suit

logging.basicConfig(level=logging.DEBUG)


class TrumpStatus(IntEnum):
    VICE = 0
    PLAYED = 1
    TRUMP = 2


class ShengjiRank(IntEnum):
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


SHENGJI_RANK_EXCLUDE_JOKERS_AND_DOMINANTS = list(ShengjiRank)[:-4]


class ShengJiCard(Card):
    def __init__(self, rank, suit=Suit.BLANK, owner=FourPlayerEnum.DECK,
                 is_in_hand=False, is_score=False, is_trump=False, is_dominant=False):
        super().__init__(rank, suit, owner, is_in_hand)
        self.is_score = is_score
        self.is_trump = is_trump
        self.is_dominant = is_dominant
        self.actual_rank = self.rank
        if is_dominant:
            if is_trump:
                self.actual_rank = rank.TRUNP_DOMINANT
            else:
                self.actual_rank = rank.DOMINANT

    def compare_trump(self, other, playing_suit):
        self_trump = True if self.is_dominant else self.is_trump
        other_trump = True if other.is_dominant else other.is_trump

        if self.is_trump == other.is_trump:
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

    def compare_rank(self, other):
        return self.actual_rank >= other.actual_rank

    # returns True if this card is larger than the other card
    # self is the first card that gets played
    def compare(self, other, playing_suit):
        trump_status = self.compare_trump(other, playing_suit)
        if trump_status != 0:
            return trump_status > 0
        return self.compare_rank(other)


