from Octobus import Octobus
from Arena import Arena
from Player import Player


def main():
    N = 2
    K = 3
    nr_games = 100
    game = Octobus(N, K)
    # Some simple players and some fully random players
    players = [Player('simple') for i in range(int(N/2))] + [Player('random') for i in range(int(N/2))]


    arena = Arena(game, players)
    final_score = arena.playGames(nr_games, verbose=False)
    print("Final score:",final_score)
    print("Average score:",final_score/nr_games)

if __name__ == "__main__":
    main()