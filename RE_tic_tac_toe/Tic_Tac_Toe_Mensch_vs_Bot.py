import numpy as np
import tkinter as tk
import copy
import pickle as pickle    # cPickle is available in Python 2.x only, otherwise use pickle

from enviorment import Game, HumanPlayer, QPlayer

# Laden der Q aus dem Training
bot_training_Eingabe_epsilon = input("Bitte geben Sie den Epsilon-Wert ein: ")
bot_training_Eingabe_Nepisodes = input("Bitte geben Sie die Anzahl der Episoden ein:")



Q = pickle.load(open(f"epsilon_{bot_training_Eingabe_epsilon}_Episoden_{bot_training_Eingabe_Nepisodes}.p", "rb"))
#Q = pickle.load(open(f"Q_epsilon_{bot_training_Eingabe_epsilon}_Nepisodee_{bot_training_Eingabe_Nepisodes}.p", "rb"))

# Gui initialisieren
root = tk.Tk()
player1 = HumanPlayer(mark="X")
player2 = QPlayer(mark="O", epsilon=0)
# Spiel starten
game = Game(root, player1, player2, Q=Q)

game.play()
root.mainloop()