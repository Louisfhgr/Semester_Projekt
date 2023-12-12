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
