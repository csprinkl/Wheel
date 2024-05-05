import tkinter as tk
from tkinter import messagebox
import random
import json

class WeightedRandom:
    def __init__(self, items):
        self.items = items
        self.weights = [1] * len(items)
        self.last_winner = None

    def load_weights(self, filename):
        try:
            with open(filename, "r") as file:
                self.weights = json.load(file)
        except FileNotFoundError:
            pass  # If file not found, weights will remain as default

    def save_weights(self, filename):
        with open(filename, "w") as file:
            json.dump(self.weights, file)

    def choose(self):
        if self.last_winner is not None:
            remaining_items = [item for item in self.items if item != self.last_winner]
        else:
            remaining_items = self.items

        total_weight = sum(self.weights)
        threshold = random.uniform(0, total_weight)
        weight_sum = 0

        for i, weight in enumerate(self.weights):
            if self.items[i] in remaining_items:
                weight_sum += weight
                if weight_sum >= threshold:
                    self.last_winner = self.items[i]
                    return self.items[i]

    def adjust_weights(self, chosen_item):
        for i, item in enumerate(self.items):
            if item == chosen_item:
                self.weights[i] = max(1, self.weights[i] // 2)  # Decrease weight
            else:
                self.weights[i] *= 2  # Increase weight

class WheelOfNamesApp:
    def __init__(self, master, names, weights_filename):
        self.master = master
        self.names = names
        self.weights_filename = weights_filename
        self.weighted_random = WeightedRandom(names)
        self.weighted_random.load_weights(self.weights_filename)

        self.wheel_frame = tk.Frame(self.master)
        self.wheel_frame.pack()

        self.winner_label = tk.Label(self.wheel_frame, text="Winner:")
        self.winner_label.pack()

        self.spin_button = tk.Button(self.wheel_frame, text="Spin Wheel", command=self.spin_wheel)
        self.spin_button.pack()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def spin_wheel(self):
        winner = self.weighted_random.choose()
        if winner:
            self.weighted_random.adjust_weights(winner)
            self.winner_label.config(text="Winner: " + winner)
            messagebox.showinfo("Winner", f"The winner is: {winner}")
            self.weighted_random.save_weights(self.weights_filename)
        else:
            messagebox.showinfo("No Winner", "All names have been picked. Resetting for the next round.")

    def on_closing(self):
        self.weighted_random.save_weights(self.weights_filename)
        self.master.destroy()

def main():
    # List of names
    names = ["Branden", "Caleb", "Kelly", "Kevin", "Nikita", "Surya", "Shayne", "Max", "Zoey", "Nick"]
    weights_filename = "weights.json"

    # Create GUI window
    root = tk.Tk()
    root.title("Wheel of in Office Pain")

    # Create and run the application
    app = WheelOfNamesApp(root, names, weights_filename)
    root.mainloop()

if __name__ == "__main__":
    main()