import random
from utils import *

def possible_successor(state):
    """
    return all possible states of simulation
    """
    raise NotImplementedError

def current_state(self, state, player):
    return state

def max_full_value(state, alpha, beta):
        if terminate(state):
            return current_state(state, player)
        v = -infinity
        for (a, s) in possible_successors(state):
            v = max(v, min_full_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

def min_full_value(state, alpha, beta):
        if terminate(state):
            return current_state(state, player)
        v = infinity
        for (a, s) in possible_successors(state):
            v = min(v, max_full_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

def alphabeta_full_search(state, game):
    player = to_move(state)
    action, state = argmax(possible_successors(state), lambda ((a, s)): min_full_value(s, -infinity, infinity))
    return action



