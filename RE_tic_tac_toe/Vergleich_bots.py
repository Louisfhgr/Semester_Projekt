import numpy as np
import tkinter as tk
import copy
import pickle as pickle    # cPickle is available in Python 2.x only, otherwise use pickle

from enviorment import Game, HumanPlayer, QPlayer, RandomPlayer



# Laden der Q aus dem Training
bot_training_Eingabe_epsilon = 0.7

bot_training_Eingabe_Nepisodes = 10000



Q = pickle.load(open(f"epsilon_{bot_training_Eingabe_epsilon}_Episoden_{bot_training_Eingabe_Nepisodes}.p", "rb"))


# Gui initialisieren
root = tk.Tk()
player1 = RandomPlayer(mark="X")
player2 = QPlayer(mark="O", epsilon=0)
# Spiel starten
game = Game(root, player1, player2, Q=Q)

for i in range(1000):

    game.play()
    game.reset()

