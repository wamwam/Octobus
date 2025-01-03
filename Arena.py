import numpy as np
from tqdm import tqdm

class Arena:
    """
    A general class where any number of agents can be pit against each other.
    """
    def __init__(self, game, players, display=None):
        self.players = players
        self.game = game


    def playGame(self, verbose=False):
        G = self.game
        G.reset()
        while not G.is_game_over():
            player = self.players[G.current_player]
            move, target = player.make_move(G)
            if verbose:
                G.display_state(move)
            G.DoMove(move, target)
        return G.score

    def playGames(self, num, verbose=False):
        G = self.game
        total_score = np.zeros(G.N)
        
        for i in tqdm(range(num)):
            score = self.playGame(verbose=verbose)
            total_score += score

        return total_score