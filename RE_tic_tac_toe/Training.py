from Grundaufbau import create_board, is_game_over, get_winner
import random
import numpy as np

class QLearningAgent:
    def __init__(self, alpha, epsilon, gamma):
        self.q_values = {}  # Q-Werte für Zustands-Aktionspaare
        self.alpha = alpha  # Lernrate
        self.epsilon = epsilon  # Erkundungsfaktor
        self.gamma = gamma  # Rabattfaktor

    def get_action(self, state):
        if random.random() < self.epsilon:
            # Erkundung: Zufällige Aktion auswählen (mit Wahrscheinlichkeit epsilon)
            legal_actions = [i for i, value in enumerate(state) if value == " "]
            if legal_actions:
                return random.choice(legal_actions)
        else:
            # Exploitation: Beste Aktion auswählen (mit Wahrscheinlichkeit 1 - epsilon)
            q_values_for_state = [self.q_values.get((state, a), 0) for a in range(9)]
            best_action = np.argmax(q_values_for_state)
            return best_action

    def learn(self, state, action, reward, next_state):
        # Q-Wert für den aktuellen Zustand und die ausgewählte Aktion
        current_q_value = self.q_values.get((state, action), 0)

        # Maximale Q-Wert im nächsten Zustand
        next_q_values = [self.q_values.get((next_state, a), 0) for a in range(9)]
        max_next_q_value = max(next_q_values) if next_q_values else 0

        # Q-Wert-Update mit der Q-Lernregel
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * max_next_q_value - current_q_value)

        # Aktualisieren Sie den Q-Wert für den aktuellen Zustand und die ausgewählte Aktion
        self.q_values[(state, action)] = new_q_value




def train_q_learning_bot(bot, num_episodes):
    for episode in range(num_episodes):
        print(f"Episode {episode + 1}/{num_episodes}")
        board = create_board()
        current_player = "X"

        while not is_game_over(board):
            state = tuple(board)
            action = bot.get_action(state)

            # Führen Sie den Zug basierend auf der ausgewählten Aktion aus
            # (aktualisieren Sie das Spielfeld und den aktuellen Spieler)

            next_state = tuple(board)  # Zustand nach dem Zug

            # Überprüfen Sie, ob das Spiel beendet ist und wer gewonnen hat
            if is_game_over(board):
                winner = get_winner(board)
                if winner == "X":
                    reward = 1  # Positive Belohnung, Bot 1 hat gewonnen
                elif winner == "O":
                    reward = -1  # Negative Belohnung, Bot 2 hat gewonnen
                else:
                    reward = 0  # Unentschieden, Belohnung = 0
            else:
                reward = 0  # Spiel läuft weiter, Belohnung = 0

            # Aktualisieren Sie die Q-Werte basierend auf dem Q-Lernprozess
            bot.learn(state, action, reward, next_state)

        # Implementieren Sie hier die Aktualisierung der Gewinnstatistik für den Bot.
        # Sie können die Gewinne des Bots in dieser Episode verfolgen.

        # Wechseln Sie die Spieler für das nächste Spiel
        current_player = "O" if current_player == "X" else "X"

    # Geben Sie am Ende des Trainings die Gewinnstatistik oder Fortschrittsinformation aus, wenn gewünscht.
