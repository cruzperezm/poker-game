# Please feel free to work with your own code structure

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
#

from itertools import combinations
from collections import Counter
import random

ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
suits = ['s', 'h', 'd', 'c']

# 2 example poker hands
example_hand1 = ['Ad', '2s', '2c']
example_hand2 = ['5s', '5c', '5d']

# Randomly generate two hands of n cards

def generate_2hands(nn_card):
    """
    Return two hands of cards, each hand consists of nn_card number of cards.
    Note that there shall be no duplicates.
    
    Parameters
    ----------
    nn_card : int
            Number of cards in each hand

    Returns
    -------
    out : lists of strings
        Two lists, each corresponding to one hand
    """
    i = 0
    while i < 2:
        i += 1
        current_hand = []
        used_cards = []
        while len(current_hand) < 3:
            dealt_card = str(ranks[random.randrange(0, 13)]) + suits[random.randrange(0, 4)]
            if dealt_card in used_cards:
                continue
            current_hand.append(dealt_card)
            used_cards.append(dealt_card)
        yield current_hand
    pass

# identify hand category using IF-THEN rule
def identify_hand(hand):
    """
    Identify the type and the strength of one hand. 
    
    Notes
    ----------
    We only work with hands with three cards in this exercise, hence, there are three types available, i.e. high cards, one pair,       three of a kind.
    
    
    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : string, int
        This function should return the type, and the strength of the given hand.
    """
    ranks_eval = []
    suits_eval = []
    for c in hand:
        if c[0] == "1" and c[1] == "0":
            ranks_eval.append(10)
            suits_eval.append(c[2])
        if c[0] == "A" or c[0] == "J" or c[0] == "Q" or c[0] == "K":
            ranks_eval.append(ranks.index(c[0]) + 2)
            suits_eval.append(c[1])
        else:
            ranks_eval.append(int(c[0]))
            suits_eval.append(c[1])

    # Three of a kind
    if ranks_eval[0] == ranks_eval[1]:
        if ranks_eval[1] == ranks_eval[2]:
            return {"name" : "three of a kind", "rank" : ranks_eval[0], "suit1" : suits_eval[0], "suit2" : suits_eval[1], "suit2" : suits_eval[2]}
        return {"name":"pair", "rank" : ranks_eval[0], "suit1" : suits_eval[0], "suit2" : suits_eval[1]}
    if ranks_eval[0] == ranks_eval[2]:
        return {"name" : "pair", "rank" : ranks_eval[0], "suit1" : suits_eval[0], "suit2" : suits_eval[1]}
    if ranks_eval[1] == ranks_eval[2]:
        return {"name" : "pair", "rank" : ranks_eval[1], "suit1" : suits_eval[1], "suit2" : suits_eval[2]}
    return {"name" : "high card", "rank" : max(ranks_eval), "suit" : suits_eval[ranks_eval.index(max(ranks_eval))]}

                               
# Print out the result
def analyse_hand(hand):
    """
    Evaluates a given hand based on its type and strength, and return an integer value.
    
    Notes
    ----------
    This function should call identify_hand(...) and evaluate it based on its type and the strength.
    high cards: 1 - 13
    pairs: 14 - 26
    three-of-a-kind: 27 - 39
    
    
    Parameters
    ----------
    Hand_ : list of strings
          Player hands, a list of three strings

    Returns
    -------
    out : int
        A value refecting the overall strength of a hand.
    """
    hand_type = identify_hand(hand)
    score = 0
    if hand_type.get("name") == "high card":
        score += hand_type.get("rank") - 1 
    if hand_type.get("name") == "three-of-a-kind":
        score = 27
        score += hand_type.get("rank") - 2
    if hand_type.get("name") == "pair":
        score = 14
        score += hand_type.get("rank") - 2 
    return score


#########################
#        Agents         #
#########################

class agent:
    def __init__(self):
        self.name = "Agent"
        self.hand = None
        self.hand_strength = None
        self.total_winnings = 0
    def observe_hand(self, own_hand, other_hand=None):
        self.hand = own_hand 
        self.hand_strength = analyse_hand(own_hand)
        if other_hand:
            pass
    def observe_bid(self, own_bid, other_bid, phase):
        pass # to be overridden by the random, fixed and simple reflex agents 
    def bid_ammount(self, phase, bid_limit, other_bid=0):
        return 0 # to be overridden by the random, fixed and simple reflex agents

class randomAgent(agent):
    def __init__(self):
        super().__init__()
    def bid_ammount(self, phase):
        return random.randrange(0, 50)
class fixedAgent(agent):
    def __init__(self):
        self.current_bid = 10
        super().__init__()
    def bid_ammount(self, phase, bid_limit, other_bid=0):
        bid = self.current_bid + 10*phase
        self.current_bid = min(bid_limit, bid)
        return bid
class simpleReflexAgent(agent):
    def __init__(self):
        super().__init__()
        self.current_bid = 0
    def bid_ammount(self, phase, bid_limit, other_bid):
        """strength = self.hand_strength
        base = 0
        bid = 0
        if s >= 27: # if the hand is three of a kind 
            base = other_bid
            bid = base + (s/5)*phase 
        elif s >= 14: # if the hand is a pair 
            base = other_bid
            bid = base + (s/5)*phase
        else:
            bid = base + (s/5)*phase
        self.current_bid = bid
        return max(0, min(bid_limit, bid))"""
        self.current_bid = own_bid
        strength = self.hand_strength
        if strength >= 27: # if the hand is a three of a kind 
            if strength >= 35:     # is the hand is a strong three of a kind 
                if other_bid > 35:
                    self.current_bid = other_bid + 5
                else:
                    self.current_bid = other_bid + 15
            else:
                if other_bid > 25:
                    self.current_bid = other_bid + 5
                else:
                    self.current_bid = other_bid + 10
        elif strength >= 14:
            if strength >= 22:
                if other_bid > 20:
                    self.current_bid = other_bid + 5
                else:
                    self.current_bid = other_bid + 15
            else:
                if other_bid > 15:
                    self.current_bid = other_bid + 5
                else:
                    self.current_bid = other_bid + 10
        else:
            if strength >= 10:
                if other_bid > 10:
                    self.current_bid = other_bid + 5
                else:
                    self.current_bid = other_bid + 15
            else:
                if other_bid > 5:
                    self.current_bid = other_bid + 5
                else:
                    self.current_bid = other_bid + 10
        own_bid = self.current_bid
        return min(50, own_bid)


class reflexAgentWithMemory(agent):  # Bonus agent
    def __init__(self):
        super().__init__()
        self.last_bid = 0
    
    def bid_ammount(self, phase, bid_limit, other_bid=0):
        strength = self.hand_strength
        last_bid = self.last_bid  # Use opponent's last bid
        bid = 0
        if strength >= 27:  # Three of a kind
            if strength >= 35:  # Strong three
                bid = last_bid + 15 if last_bid <= 35 else last_bid + 5
            else:
                bid = last_bid + 10 if last_bid <= 25 else last_bid + 5
        elif strength >= 14:  # Pair
            if strength >= 22:  # Strong pair
                bid = last_bid + 15 if last_bid <= 20 else last_bid + 5
            else:
                bid = last_bid + 10 if last_bid <= 15 else last_bid + 5
        else:  # High card
            if strength >= 10:  # Strong high
                bid = last_bid + 15 if last_bid <= 10 else last_bid + 5
            else:
                bid = last_bid + 10 if last_bid <= 5 else last_bid + 5
        return min(bid_limit, max(0, bid))

#########################
#      Game flow        #
#########################

n_phases = 3
hand_bid_limit = 50
hands_per_game = 50

def play_hand(agent1, agent2):
    """
    Play one hand: deal cards, bid 3 times, showdown, update winnings.
    Returns the pot won by agent1 (negative if agent2 wins).
    """
    # Card dealing
    hand1, hand2 = generate_2hands(3)
    agent1.observe_hand(hand1)
    agent2.observe_hand(hand2)

    pot = 0
    for phase in range(1, n_phases + 1):
        # Bidding
        bid1 = agent1.bid_ammount(phase, hand_bid_limit, agent2.last_bid)
        bid2 = agent2.bid_ammount(phase, hand_bid_limit, agent1.last_bid)
        pot += bid1 + bid2
        agent1.observe_bid(bid1, bid2, phase)
        agent2.observe_bid(bid2, bid1, phase)

    # Showdown
    strength1 = agent1.hand_strength
    strength2 = agent2.hand_strength
    if strength1 > strength2:
        agent1.total_winnings += pot
        return pot
    elif strength2 > strength1:
        agent2.total_winnings += pot
        return -pot
    else:
        # Tie: split pot (but since unlimited money, just 0 diff)
        agent1.total_winnings += pot / 2
        agent2.total_winnings += pot / 2
        return 0


def play_game(agent1, agent2, hands_per_game=50):
    # play a full game (50 hands), return bankroll difference (agent1 - agent2).
    for i in range(hands_per_game):
        play_hand(agent1, agent2)
    diff = agent1.total_winnings - agent2.total_winnings
    # Reset for next game
    agent1.total_winnings = 0
    agent2.total_winnings = 0
    return diff


def run_simulations(agent1_class, agent2_class, num_games=100):
    """
    Run num_games, return list of bankroll differences.
    """
    diffs = []
    for _ in range(num_games):
        agent1 = agent1_class()
        agent2 = agent2_class()
        diff = play_game(agent1, agent2, hands_per_game)
        diffs.append(diff)
    return diffs


