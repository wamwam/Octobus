import random
import numpy as np


class Octobus:
    """ The full game of Ocotobus

    The game state can be defined by:
    Cards on the table belonging to players
    Centre card
    The current player
    The move number
    The chosen target

    Added for easy of calculation:
    Current card value
    Probability array p
    Number of cards left per player
    """
    def __init__(self, N, K=3):
        # N = number of players
        # K = number of cards per player
        self.N = N
        self.K = K
        self.ranks = ['-', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def reset(self):
        """ Reset the game state to the initial state """
        self.target = 0
        self.current_player = 0
        self.move_number = 0
        self.target = 0
        self.p = np.ones(self.N)
        self.score = np.zeros(self.N)

        self.cards_left = self.K * np.ones(self.N, dtype=np.uint8) 
        self.cards = np.zeros([self.N, self.K], dtype=np.int8)
        self.center_card = self.draw_random_card()
        for i in range(self.N):
            for j in range(self.K):
                self.cards[i, j] = self.draw_random_card()
            self.p[i] = self.calculate_p(i)

        self.current_card = self.cards[self.current_player, self.move_number]


    def DoMove(self, move, target):
        " Perform a move and update the game state"
        new_card = self.draw_random_card()
        correct = self.higherorlower(self.current_card, new_card, move)

        # Lay down next card and update probability
        if self.move_number < self.K:
            self.cards[self.current_player, self.move_number] = new_card
            self.p[self.current_player] = self.calculate_p(self.cards[self.current_player,:])
        elif self.move_number == self.K:
            # Target can be selected when correctly guessing the centre card
            self.target = target
            self.center_card = new_card
        else:
            self.cards[self.target, self.move_number - self.K - 1] = new_card
            self.p[self.target] = self.calculate_p(self.cards[self.target,:])

        if correct:
            self.move_number += 1
            # Check if end reached: final card or next card not existing (=1)
            if self.move_number == (2*self.K+1) or (self.move_number > self.K and self.cards[self.target, self.move_number - self.K - 1] == 0):
                self.update_score()
                self.remove_card()
                self.next_player()
        else:
            self.next_player()

        self.read_next_card()


    def read_next_card(self):
        "Get value of next card to play"
        if self.move_number < self.K:
            self.current_card = self.cards[self.current_player, self.move_number]
        elif self.move_number == self.K:
            self.current_card = self.center_card
        else:
            self.current_card = self.cards[self.target, self.move_number - self.K - 1]

    def remove_card(self):
        "Remove a card from the game for a player"
        self.cards_left[self.current_player] -= 1
        self.cards[self.current_player, self.K - self.cards_left[self.current_player] - 1] = 0
        self.p[self.current_player] = self.calculate_p(self.cards[self.current_player,:])
        self.target = None
        # If out of game, set p to 0
        if self.cards_left[self.current_player] == 0:
            self.p[self.current_player] = 0

    def update_score(self):
        self.score[self.target] += 1

    def next_player(self):
        "Set the next player and his starting move number"
        next_player = self.current_player
        while True:
            next_player = (next_player + 1) % self.N
            if self.cards_left[next_player] > 0:
                self.move_number = self.K - self.cards_left[next_player]
                self.current_player = next_player
                break
            elif next_player == self.current_player:
                # All players have no cards left
                break

    def draw_random_card(self):
        return random.randint(1, 13)

    def is_game_over(self):
        if np.all(self.cards == 0):
            if np.sum(self.score) != self.K*self.N:
                raise Exception("Game over, but not all points have been distributed")
            return True

    def higherorlower(self, card1, card2, move):
        if move == "higher":
            return card2 > card1
        elif move == "lower":
            return card2 < card1
        
    def calculate_p(self, cards):
        p = (abs(cards - 7) + 6) / 13
        return np.prod(p)
    
    def display_state(self, move):
        print("Current player: ", self.current_player)
        print("Move number: ", self.move_number)
        print("Target: ", self.target)
        print("Current card: ", self.ranks[self.current_card])
        print("Move: ", move )
        print("Cards left: ", self.cards_left)
        print("Probability: ", self.p)
        print("Score: ", self.score)
        print("Center card: ", self.ranks[self.center_card])
        self.display_cards()
        print("\n")

    def display_cards(self):
        for i in range(self.N):
            print("Player ", i, end="        ")
            for j in range(self.K):
                print(self.ranks[self.cards[i,j]],"\t",end="")
            print("")