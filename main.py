from Octobus import Octobus
from Arena import Arena
from Player import Player


def main():
    N = 5
    K = 3
    nr_games = 1000
    game = Octobus(N, K)
    players = [Player('switch') for i in range(int(1))] + [Player('simple') for i in range(int(N-1))]
    #players = [Player('defect') for i in range(N)]

    arena = Arena(game, players)
    final_score = arena.playGames(nr_games, verbose=False)
    print("Final score:",final_score)
    print("Average score:",final_score/nr_games)

if __name__ == "__main__":
    main()