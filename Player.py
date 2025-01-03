import random
import numpy as np
import copy
from Octobus import Octobus
from copy import deepcopy

class Player:
    def __init__(self, strategy = None):
        self.strategy = strategy

    def make_move(self, game):
        if self.strategy == 'random':
            move, target = self.algorithm_random(game)
        elif self.strategy == 'simple':
            move, target = self.algorithm_simple(game)
        elif self.strategy == 'defect':
            move, target = self.algorithm_defect(game)
        elif self.strategy == 'simu':
            move, target = self.algorithm_simu(game)
        elif self.strategy == 'switch':
            move, target = self.algorithm_switch(game)
        else:
            raise Exception("Invalid player algorithm selected")
        
        # Checks for legal move
        if game.cards_left[target] == 0:
            move, target = self.algorithm_good(game)
            raise Exception("Invalid player selected, target has no cards left")
        if game.current_player == target and np.count_nonzero(game.cards_left) > 1:
            raise Exception("Invalid player selected, target is the current player with other targets available")
        return move, target

    def algorithm_random(self, game):
        "Ramdom player, i.e. random move and random target"
        move = random.choice(['higher', 'lower'])
        indices = np.where((game.cards_left > 0) & (np.arange(len(game.cards_left)) != game.current_player))[0]

        if len(indices) == 0:
            target = game.current_player
        else:
            target = random.choice(indices)
        return move, int(target)
    
    def algorithm_simple(self, game):
        "Simple player: chooses higher/lower based on value and chooses target with the highest total probability of succes "
        if game.current_card < 7:
            move = 'higher'
        else:
            move = 'lower'

        # Choose target with highest probability of succes, but only players that havecards left and are not the current player
        if np.count_nonzero(game.cards_left) == 1:
            target = game.current_player
        else:
            potential_targets = np.arange(game.N)[(game.cards_left > 0) & (np.arange(game.N) != game.current_player)]
            target = random.choice(potential_targets[game.p[potential_targets] == np.max(game.p[potential_targets])])

        
        return move, int(target)
    
    def algorithm_defect(self, game):
        "Simple defector, tries to prevent himself from advancing"
        if game.current_card > 7:
            move = 'higher'
        else:
            move = 'lower'

        # Choose target with lowest probability of succes, but only players that havecards left and are not the current player
        if np.count_nonzero(game.cards_left) == 1:
            target = game.current_player
        else:
            potential_targets = np.arange(game.N)[(game.cards_left > 0) & (np.arange(game.N) != game.current_player)]
            target = random.choice(potential_targets[game.p[potential_targets] == np.min(game.p[potential_targets])])
        
        return move, target


    def algorithm_switch(self, game):
        "Waits until a certain number of cards is left, then switches from defect to good"
        switch_value = 20

        if np.sum(game.cards_left) > switch_value:
            move, target = self.algorithm_defect(game)
        else:
            move, target = self.algorithm_simple(game)
        return move, target


    def algorithm_simu(self, game):
        "Simulate in the future and choose the move with best expected score"
        simul = copy.deepcopy(game)
        max_rounds = 10
        number_of_simulations = 100
        depth = 1
        
        for i in range(number_of_simulations):
            simul_copy = copy.deepcopy(simul)
            for j in range(max_rounds*self.N*self.K):
                if simul_copy.is_game_over():
                    break
                move, target = self.algorithm_simple(simul_copy)
                simul_copy.DoMove(move, target)




