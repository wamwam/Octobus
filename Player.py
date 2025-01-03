import random
import numpy as np
import copy

class Player:
    def __init__(self, strategy = None):
        self.strategy = strategy

    def make_move(self, game_state):
        if self.strategy == 'random':
            move, target = self.algorithm_random(game_state)
        elif self.strategy == 'simple':
            move, target = self.algorithm_simple(game_state)
        else:
            raise Exception("Invalid player algorithm selected")
        
        # Checks for legal move
        if game_state.cards_left[target] == 0:
            move, target = self.algorithm_good(game_state)
            raise Exception("Invalid player selected, target has no cards left")
        if game_state.current_player == target and np.count_nonzero(game_state.cards_left) > 1:
            raise Exception("Invalid player selected, target is the current player with other targets available")
        return move, target

    def algorithm_random(self, game_state):
        move = random.choice(['higher', 'lower'])
        indices = np.where((game_state.cards_left > 0) & (np.arange(len(game_state.cards_left)) != game_state.current_player))[0]

        if len(indices) == 0:
            target = game_state.current_player
        else:
            target = random.choice(indices)
        return move, target
    
    def algorithm_simple(self, game_state):
        if game_state.current_card < 7:
            move = 'higher'
        else:
            move = 'lower'

        # Set own probability to 0, then choose the target with the highest probability
        p_copy = copy.copy(game_state.p)
        p_copy[game_state.current_player] = 0
        target = np.argmax(p_copy)
        if np.count_nonzero(game_state.cards_left) == 1:
            target = game_state.current_player
        return move, target

