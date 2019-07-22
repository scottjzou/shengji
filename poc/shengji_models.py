import logging

from collection import OrderedDict

from enum import IntEnum

from functools import total_ordering

from generic_models import ALL_FOUR_PLAYERS, Card, Deck, EQUAL, FOUR_PLAYER_TEAM_1, FOUR_PLAYER_TEAM_2, \
    FourPlayerGame, Game, GameDeck, LOSING, Player,\
    Round, SUITS_EXCLUDE_BLANK, SUITS_EXCLUDE_BLANK_JOKER, Suit, WINNING

logging.basicConfig(level=logging.DEBUG)


class ShengJiRank(IntEnum):
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
    ACE = 14
    DOMINANT = 15
    TRUMP_DOMINANT = 16
    SMALL_JOKER = 17
    BIG_JOKER = 18

    def __str__(self):
        return self.name

SHENG_JI_RANK_EXCLUDE_JOKER = list(ShengJiRank)[:13]
SHENG_JI_SCORE_RANKS = {ShengJiRank.FIVE: 5, ShengJiRank.TEN: 10, ShengJiRank.KING: 10}

SHENG_JI_PLAYER_SIZE = 4


@total_ordering
class ShengJiCard(Card):
    def __init__(self, rank, suit=Suit.BLANK, actual_rank=None, owner=FourPlayerGame.DECK,
                 is_in_hand=False):
        super().__init__(rank, suit, owner, is_in_hand)
        if self.rank in SHENG_JI_SCORE_RANKS.keys():
            self.score = SHENG_JI_SCORE_RANKS[self.rank]
        else:
            self.score = 0
        self.actual_rank = actual_rank if actual_rank is not None else rank

    def __eq__(self, other):
        return ((self.rank, self.suit) == (other.rank, other.suit))

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.actual_rank < other.actual_rank

    def __cmp__(self, other):
        return cmp(self.actual_rank, other.actual_rank)

    def __str__(self):
        return ('[{}\'s card, {} {}, is_in_hand: {}, score: {}, actual_rank: {}]').format(
            self.owner, self.suit, self.rank, self.is_in_hand, self.score, self.actual_rank)

    # def set_trump(self, is_trump_suit):
    #     self.is_trump_suit = is_trump_suit
    #     self.is_trump = True if self.is_trump_suit else False
    #     if self.is_dominant:
    #         self.is_trump = True
    #         if self.is_trump_suit:
    #             self.actual_rank = ShengJiRank.TRUMP_DOMINANT
    #         else:
    #             self.actual_rank = ShengJiRank.DOMINANT

    @classmethod
    def get_joker_cards(cls):
        return [
            cls(ShengJiRank.SMALL_JOKER, Suit.JOKER),
            cls(ShengJiRank.BIG_JOKER, Suit.JOKER)
        ]

    @classmethod
    def get_dominant_cards(cls, dominant_rank):
        return [cls(dominant_rank, suit, actual_rank=ShengJiRank.DOMINANT) for suit in SUITS_EXCLUDE_BLANK_JOKER]

    @staticmethod
    # validate if all suits in play cards is the same:
    def validate_cards_suit(cards):
        cards = cardss[0]
        play_suit = play_card.suit
        for card in play_cards[1:]:
            if card.suit != play_suit:
                return False
        return True


class ShengJiDeck(Deck):
    def __init__(self, dominant_rank=ShengJiRank.TWO):
        rank_exclude_dominant = SHENG_JI_RANK_EXCLUDE_JOKER
        rank_exclude_dominant.remove(dominant_rank)
        self.cards = [ShengJiCard(rank, suit) for rank in rank_exclude_dominant
                      for suit in SUITS_EXCLUDE_BLANK_JOKER]
        self.cards += ShengJiCard.get_joker_cards()
        self.cards += ShengJiCard.get_dominant_cards(dominant_rank)


class ShengJiGameDeck(GameDeck):
    def __init__(self, dominant_rank):
        shengji_cards = 2 * ShengJiDeck(dominant_rank).get_cards()
        super().__init__(shengji_cards, 4)
        self.kitty_size = 8

    def is_drawable(self):
        return len(self.cards) > self.kitty_size


class ShengJiPlayer(Player):
    def __init__(self, name, player, hand_cards, dominant_rank=ShengJiRank.TWO):
        super().__init__(self, name, player, hand_cards)
        self.dominant_rank = dominant_rank
        self.hand_cards = {}
        for suit in SUITS_EXCLUDE_BLANK:
            self.hand_cards[suit] = []

    def draw(self, game_deck):
        card = game_deck.pop()
        card.get_owner(self)
        self.hand_cards[card.suit].append(card)

    def __str__(self):
        return '[{}: {}, current dominant_rank: {}, hand_cards: {}]'.format(
            self.owner, self.name, self.dominant_rank, self.hand_cards)

    def get_dominant_rank(self):
        return self.dominant_rank

    def call_trump(self, cards, trump_strength, dominant_rank):
        if not len(cards) in [1, 2]:
            return False
        if cards[0] != cards[1]:
            return False
        if cards.suit = suit.JOKER and len(cards) == 2:
            return True

        if len(cards) > trump_strength:
            if len(cards) == 2 and (not cards[0] == cards[1]):
                return False

                if cards[0].rank == dominant_rank or
                return True
        return False

    def pick_cards(self, round_suit):
        # place holder func
        cards = list(self.hand_cards.pop())
        while not self.validate_play_card(cards, round_suit):
            cards = self.pick_cards()
        return cards

    def validate_play_cards(self, cards, round_suit):
        # have that suit, must play that suit
        pickable_cards = self.hand_cards[round_suit]
        if len(pickable_cards) == 0:
            pickable_cards = self.hand_cards
        return True

    def play(self, round_length, round_suit):
        cards = self.pick_cards(round_suit, round_length)
        card = cards[0]
        if card.is_in_hand:
            card.is_in_hand = False
            score = card.score
            return card, score
        else:
            raise Exception(
                '{} tried to play the card that is not in hand', self.name)


class ShengJiRound(Round):
    def __init__(self, game, id, last_winner, players_in_order=ALL_FOUR_PLAYERS):
        super.__init__(id, players_in_order)
        self.round_suit = Suit.BLANK
        last_winner_index = self.players_in_order.index(last_winner)
        self.players_in_order = self.players_in_order[last_winner_index:] + self.players_in_order[:last_winner_index]

    def play(self):
        if len(self.players_in_order) == SHENG_JI_PLAYER_SIZE:
            first_player = self.players_in_order[0]
            winner_cards, round_score = first_player.play(-1, self.round_suit)
            round_length = len(winner_cards)
            round_suit = winner_cards[0].suit
            for player in self.players_in_order[1:]:
                new_cards, score = player.play(round_length, round_suit)
                round_score += score
                winner_cards, winner = self.game.compare(new_cards, winner_cards, round_suit)
                return winner, round_score
        else:
            raise Exception(
                'Round {} does not have {} players', self.id, SHENG_JI_PLAYER_SIZE)
        return None, 0


class ShengJiGame(Game):
    def __init__(self, players, dealer):
        self.dealer = dealer
        self.dominant_rank = self.dealer.get_dominant_rank()
        super().__init__(players, ShengJiGameDeck(self.dominant_rank))
        self.trump_suit = Suit.BLANK
        self.trump_strength = 0

    def dealer_team(self):
        if self.dealer in FOUR_PLAYER_TEAM_1:
            return FOUR_PLAYER_TEAM_1
        elif self.dealer in FOUR_PLAYER_TEAM_2:
            return FOUR_PLAYER_TEAM_2

    def validate_trump(self, player, cards):
        if len(cards) < 1 or len(cards) <= self.trump_strength:
            return False
        if cards[0].rank != self.dominant_rank \
            and cards[0].rank != ShengJiRank.BIG_JOKER \
                and cards[0].rank != ShengJiRank.SMALL_JOKER:
            return False
        if len(cards) == 1:
            return True
        elif len(cards) == 2:
            if cards[0] != cards[1]:
                raise Exception(
                    '{} tried to call trump with two different card {}, {} ', player, cards[0], cards[1])
            return True
        return False

    def play(self):
        if len(self.new_rounds) > 0:
            round = self.new_rounds.pop()
            round.play()
            self.played_rounds.append(round)
            return True
        return False

    def init(self):
        while self.deck.is_drawable():
            for player in self.players:
                player.draw(self.deck)
                cards = player.pick_cards(Suit.BLANK)
                call_trump = player.call_trump(cards, self.trump_strength, self.dominant_rank)
                if call_trump:
                    self.trump_suit = cards[0].suit
                    self.trump_strength = len(cards)

    def is_trump(self, card):
        return card.suit == self.trump_suit

    # 1 means play_card wins, 0 means no one wins by suit, -1 means winner_card wins
    def compare_trump(self, play_cards, winner_cards, playing_suit):
        if len(play_cards) < 1:
            raise Exception('Cannot played less than one card')
        elif len(play_cards) > 1:
            if not validate_cards_suit(play_cards):
                return LOSING
        play_card = play_cards[0]
        winner_card = winner_cards[0]

        if self.is_trump(play_card):
            if self.is_trump(winner_card):
                return EQUAL
            else:
                return WINNING
        else:
            if self.is_trump(winner_card):
                return LOSING
            # neither is trump suit, compare trump status by if is playing_suit
            else:
                if play_card.suit == playing_suit:
                    if winner_card.suit == playing_suit:
                        return EQUAL
                    else:
                        return WINNING
                else:
                    if winner_card.suit == playing_suit:
                        return LOSING
                    else:
                        return EQUAL
        return EQUAL

    # returns True if this card is larger than the other card
    # self is the first card that gets played
    def compare(self, play_cards, winner_cards, playing_suit, is_debug=True):
        def compare_rank(winner_cards, play_cards):
            winner_cards = winner_cards.sort()
            play_cards = play_cards.sort()
            cmp_index = 0
            winner_top_card = winner_cards.get(cmp_index)
            play_top_card = play_cards.get(cmp_index)
            while cmp_index < len(winner_cards):
                cmp_status = cmp(winner_top_card, play_top_card)
                if cmp_status == 0:
                    cmp_index += 1
                    winner_top_card = winner_cards.get(cmp_index)
                    play_top_card = play_cards.get(cmp_index)
                else:
                    return cmp_status >= 0
            return True

        if is_debug:
            print(play_cards)
            print(winner_cards)
            print(playing_suit)
        trump_status = self.compare_trump(play_cards, winner_cards, playing_suit)
        if is_debug:
            print(trump_status)
        if trump_status == WINNING:
            return play_cards, play_cards[0].player
        elif trump_status == LOSING:
            return winner_cards, winner_cards[0].player
        if not compare_rank(winner_cards, play_cards):
            return play_cards, play_cards[0].player
        return winner_cards, winner_cards[0].player
