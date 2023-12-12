
import tkinter as tk # Gui 
import pickle 
from enviorment import Game, QPlayer 

for i in range(1, 9):
    print(i)

    # Q-Learning
    root = tk.Tk()
    epsilon =  i/10 # epsilon = 0 -> wenig Exploration, epsilon = 1 ->  viel Exploration
    player1 = QPlayer(mark="X",epsilon = epsilon)
    player2 = QPlayer(mark="O",epsilon = epsilon)
    game = Game(root, player1, player2)

    # Train des Q
    N_episodes = 100
    for episodes in range(N_episodes):
        game.play()
        game.reset()

    Q = game.Q

    # speichern der Q
    filename = f"epsilon_{epsilon}_Episoden_{N_episodes}.p".format(N_episodes) # Ist der Name der Datei
    pickle.dump(Q, open(filename, "wb"))
