import numpy as np
import tkinter as tk
import copy
import pickle as pickle   
import pandas as pd 

class Game:
    def __init__(self, master, player1, player2, Q_learn=None, Q={}, alpha=0.3, gamma=0.9):
        frame = tk.Frame() 
        frame.grid()
        self.master = master
        master.title("Tic Tac Toe")
        self.player1 = player1         # Spieler 1: Macht den ersten Zug
        self.player2 = player2       # Spieler 2: Macht den zweiten Zug
        self.current_player = player1   # Der Spieler, der gerade an der Reihe ist
        self.other_player = player2    
        self.empty_text = ""        # Text, der auf den Buttons angezeigt wird, bevor sie angeklickt werden
        self.board = Board()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]    # 3x3 Buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(frame, height=3, width=3, text=self.empty_text, command=lambda i=i, j=j: self.callback(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j)

        self.reset_button = tk.Button(text="Reset", command=self.reset) 
        self.reset_button.grid(row=3)    # Reset Button
        #  Q-learning
        self.Q_learn = Q_learn
        if self.Q_learn:
            self.Q = Q                  # Action value   
            self.alpha = alpha          # Learning rate
            self.gamma = gamma          # Discount rate
            self.share_Q_with_players()

    @property
    def Q_learn(self):             # Q-learning
        if self._Q_learn is not None:      
            return self._Q_learn            
        if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
            return True

    @Q_learn.setter
    def Q_learn(self, _Q_learn): 
        self._Q_learn = _Q_learn

    def share_Q_with_players(self):             # The action value table Q is shared with the QPlayers to help them make their move decisions
        if isinstance(self.player1, QPlayer):
            self.player1.Q = self.Q
        if isinstance(self.player2, QPlayer):
            self.player2.Q = self.Q

    # The callback method is called whenever a button is pressed. It is responsible for updating the GUI,
    def callback(self, button):
        if self.board.over():
            pass                # Do nothing if the game is already over
        else:
            if isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, HumanPlayer):
                if self.empty(button):
                    move = self.get_move(button)
                    self.handle_move(move)
            elif isinstance(self.current_player, HumanPlayer) and isinstance(self.other_player, ComputerPlayer):
                computer_player = self.other_player
                if self.empty(button):
                    human_move = self.get_move(button)
                    self.handle_move(human_move)
                    if not self.board.over():               # Trigger the computer's next move
                        computer_move = computer_player.get_move(self.board)
                        self.handle_move(computer_move)


    def empty(self, button):    
        return button["text"] == self.empty_text

    def get_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))                # Get move coordinates from the button's metadata
        return move

    def handle_move(self, move):
        if self.Q_learn:
            self.learn_Q(move)
        i, j = move         # Get row and column number of the corresponding button
        self.buttons[i][j].configure(text=self.current_player.mark)     # Change the label on the button to the current player's mark
        self.board.place_mark(move, self.current_player.mark)           # Update the board
        if self.board.over():
            self.declare_outcome()
        else:
            self.switch_players()


    # Gewinner ausgeben
    list_of_results = []
    def declare_outcome(self):
        if self.board.winner() is None:
            print("Unentschieden")
            self.list_of_results.append("Unentschieden")

        else:
            print(("Spielende. Spieler {mark} hat gewonnen!".format(mark=self.current_player.mark)))
            self.list_of_results.append(self.current_player.mark)
        #print(self.list_of_results)
        #liste als dataframe speichern
        df = pd.DataFrame(self.list_of_results)
        df.to_csv("results_of_.csv", index=False, header=False)
    


    # Reset:  Buttons und Board zurücksetzen
    def reset(self):
        print("Resetting...")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty_text)
        self.board = Board(grid=np.ones((3,3))*np.nan)
        self.current_player = self.player1
        self.other_player = self.player2
        # np.random.seed(seed=0)      # Random einstellen
        self.play()

    # Switch players: Wechseln der Spieler
    def switch_players(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.other_player = self.player1
        else:
            self.current_player = self.player1
            self.other_player = self.player2


    # Play: Starten des Spiels    
    def play(self):
        if isinstance(self.player1, HumanPlayer) and isinstance(self.player2, HumanPlayer):
            pass        # For human vs. human, play relies on the callback from button presses
        elif isinstance(self.player1, HumanPlayer) and isinstance(self.player2, ComputerPlayer):
            pass
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, HumanPlayer):
            first_computer_move = player1.get_move(self.board)      
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer) and isinstance(self.player2, ComputerPlayer):
            while not self.board.over():        
                self.play_turn()

    # Play turn:
    def play_turn(self):
        move = self.current_player.get_move(self.board)
        self.handle_move(move)


    # Q-learning
    def learn_Q(self, move):  
        # Update the Q value 
        state_key = QPlayer.make_and_maybe_add_key(self.board, self.current_player.mark, self.Q) # current state
        next_board = self.board.get_next_board(move, self.current_player.mark) # next state
        reward = next_board.give_reward() # reward
        next_state_key = QPlayer.make_and_maybe_add_key(next_board, self.other_player.mark, self.Q) # next state key
        if next_board.over():
            expected = reward
        else:
            next_Qs = self.Q[next_state_key]     #  nächste Q-Werte 
            if self.current_player.mark == "X":
                expected = reward + (self.gamma * min(next_Qs.values()))        
            elif self.current_player.mark == "O":
                expected = reward + (self.gamma * max(next_Qs.values()))        
        change = self.alpha * (expected - self.Q[state_key][move])    #  Q-Wert-Update mit der Q-Lernregel
        self.Q[state_key][move] += change     #  Aktualisieren Sie den Q-Wert für den aktuellen Zustand und die ausgewählte Aktion


# The Board class is responsible for keeping track of the state of the game 
class Board:
    def __init__(self, grid=np.ones((3,3))*np.nan):
        self.grid = grid

    def winner(self):
        rows = [self.grid[i,:] for i in range(3)]
        cols = [self.grid[:,j] for j in range(3)]
        diag = [np.array([self.grid[i,i] for i in range(3)])]
        cross_diag = [np.array([self.grid[2-i,i] for i in range(3)])]
        lanes = np.concatenate((rows, cols, diag, cross_diag))      

        any_lane = lambda x: any([np.array_equal(lane, x) for lane in lanes])   # Returns true if any lane is equal to the input argument "x"
        if any_lane(np.ones(3)):
            return "X"
        elif any_lane(np.zeros(3)):
            return "O"

    def over(self):             # Returns true if the game is over (either because someone has won or because the board is full)
        return (not np.any(np.isnan(self.grid))) or (self.winner() is not None)

    def place_mark(self, move, mark):       # Place a mark on the board
        num = Board.mark2num(mark)
        self.grid[tuple(move)] = num

    @staticmethod
    def mark2num(mark):  
        d = {"X": 1, "O": 0}
        return d[mark]
    


    
    def available_moves(self):
        return [(i,j) for i in range(3) for j in range(3) if np.isnan(self.grid[i][j])]

    def get_next_board(self, move, mark):
        next_board = copy.deepcopy(self)
        next_board.place_mark(move, mark)
        return next_board

    def make_key(self, mark):# For Q-learning, returns a 10-character string representing the state of the board and the player whose turn it is
        fill_value = 9
        filled_grid = copy.deepcopy(self.grid)
        np.place(filled_grid, np.isnan(filled_grid), fill_value)
        return "".join(map(str, (list(map(int, filled_grid.flatten()))))) + mark

    # Reward: Gibt den Reward für das aktuelle Board zurück
    def give_reward(self):      
        if self.over():
            if self.winner() is not None:
                if self.winner() == "X":
                    return 1.0                      # Player X won -> positive reward
                elif self.winner() == "O":
                    return -1.0                     # Player O won -> negative reward
            else:
                return 0.5                          # A smaller positive reward for a unentschieden
        else:
            return 0.0                              # No reward = not yet finished

# The Player class is the parent class of HumanPlayer and ComputerPlayer
class Player(object):
    def __init__(self, mark):
        self.mark = mark

    @property
    def opponent_mark(self):
        if self.mark == 'X':
            return 'O'
        elif self.mark == 'O':
            return 'X'
        else:
            print("The player's mark must be either 'X' or 'O'.")

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    pass

class RandomPlayer(ComputerPlayer):
    @staticmethod
    def get_move(board):
        moves = board.available_moves()
        if moves:   
            return moves[np.random.choice(len(moves))]    

class THandPlayer(ComputerPlayer):
    def __init__(self, mark):
        super(THandPlayer, self).__init__(mark=mark)

    def get_move(self, board):
        moves = board.available_moves()
        if moves:
            for move in moves:
                if THandPlayer.next_move_winner(board, move, self.mark):
                    return move
                elif THandPlayer.next_move_winner(board, move, self.opponent_mark):
                    return move
            else:
                return RandomPlayer.get_move(board)

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.get_next_board(move, mark).winner() == mark


class QPlayer(ComputerPlayer):
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(QPlayer, self).__init__(mark=mark)
        self.Q = Q
        self.epsilon = epsilon

    def get_move(self, board):
        if np.random.uniform() < self.epsilon:              
            return RandomPlayer.get_move(board)
        else:
            state_key = QPlayer.make_and_maybe_add_key(board, self.mark, self.Q)
            Qs = self.Q[state_key]

            if self.mark == "X":
                return QPlayer.stochastic_argminmax(Qs, max)
            elif self.mark == "O":
                return QPlayer.stochastic_argminmax(Qs, min)

    @staticmethod
    def make_and_maybe_add_key(board, mark, Q):     # Make a dictionary key for the current state (board + player turn) 
        default_Qvalue = 1.0       #  exploration Modus
        state_key = board.make_key(mark)
        if Q.get(state_key) is None:
            moves = board.available_moves()
            Q[state_key] = {move: default_Qvalue for move in moves} 
        return state_key

    @staticmethod
    # exploration Modus
    def stochastic_argminmax(Qs, min_or_max):       
        min_or_maxQ = min_or_max(list(Qs.values()))
        if list(Qs.values()).count(min_or_maxQ) > 1:     
            best_options = [move for move in list(Qs.keys()) if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move
