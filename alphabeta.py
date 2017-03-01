import random
from utils import *

# make TicTacToe Class function
def terminate(state):
    """
    return True if this is final state of simulation
    """
    raise NotImplementedError

# make TicTacToe Class function
def to_move(state):
    """
    return player who has to move next
    """
    raise NotImplementedError

# make TicTacToe Class function
def possible_successors(state):
    """
    return all possible states of simulation
    """
    raise NotImplementedError

# make TicTacToe Class function
def current_state(self, state, player):
    """
    return current state of simulation
    """
    raise NotImplementedError

def max_full_value(state, alpha, beta):
        if TicTacToe.terminate(state):
            return TicTacToe.current_state(state, player)
        v = -infinity
        for (a, s) in TicTacToe.possible_successors(state):
            v = max(v, min_full_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

def min_full_value(state, alpha, beta):
        if TicTacToe.terminate(state):
            return TicTacToe.current_state(state, player)
        v = infinity
        for (a, s) in TicTacToe.possible_successors(state):
            v = min(v, max_full_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

"""
search all the way to the leaves
"""
def alphabeta_full_search(state, game):
    player = TicTacToe.to_move(state)
    action, state = argmax(possible_successors(state), lambda ((a, s)): min_full_value(s, -infinity, infinity))
    return action

def cutoff_test(state, depth):
    cutoff_test = None
    cutoff_test = (cutoff_test or (lambda state, depth: depth>d or TicTacToe.terminate(state)))
    return cutoff_test

def eval_function(state):
    eval_fn = None
    eval_fn = eval_fn or (lambda state: TicTacToe.current_state(state, player))
    return eval_fn

def max_prune_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_function(state)
        v = -infinity
        for (a, s) in possible_successors(state):
            v = max(v, min_prune_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

def min_prune_value(state, alpha, beta, depth):
    if cutoff_test(state, depth):
        return eval_function(state)
    v = infinity
    for (a, s) in possible_successors(state):
        v = min(v, max_prune_value(s, alpha, beta, depth+1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

"""
search upto cutoff depth
"""
def alphabeta_pruning_search(state, game, d=4, cutoff_test=cutoff_test, eval_function=eval_function):
    player = TicTacToe.to_move(state)
    action, state = argmax(TicTacToe.possible_successors(state), lambda ((a, s)): min_prune_value(s, -infinity, infinity, 0))
    return action
