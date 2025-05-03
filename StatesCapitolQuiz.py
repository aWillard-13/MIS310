# Andrew Willard 
# 20250502 

"""
This code is based off the text UI state - capitol quiz we designed in class. I gave it a GUI, 
then decided it would be more fun as a multiple choice. 
I applied my old hint system for the text one, but only the first letter, and also added 50/50. 
"""

import tkinter as tk
from tkinter import ttk
import random

states_and_capitals = {
    "Alabama": "Montgomery",
    "Alaska": "Juneau",
    "Arizona": "Phoenix",
    "Arkansas": "Little Rock",
    "California": "Sacramento",
    "Colorado": "Denver",
    "Connecticut": "Hartford",
    "Delaware": "Dover",
    "Florida": "Tallahassee",
    "Georgia": "Atlanta",
    "Hawaii": "Honolulu",
    "Idaho": "Boise",
    "Illinois": "Springfield",
    "Indiana": "Indianapolis",
    "Iowa": "Des Moines",
    "Kansas": "Topeka",
    "Kentucky": "Frankfort",
    "Louisiana": "Baton Rouge",
    "Maine": "Augusta",
    "Maryland": "Annapolis",
    "Massachusetts": "Boston",
    "Michigan": "Lansing",
    "Minnesota": "Saint Paul",
    "Mississippi": "Jackson",
    "Missouri": "Jefferson City",
    "Montana": "Helena",
    "Nebraska": "Lincoln",
    "Nevada": "Carson City",
    "New Hampshire": "Concord",
    "New Jersey": "Trenton",
    "New Mexico": "Santa Fe",
    "New York": "Albany",
    "North Carolina": "Raleigh",
    "North Dakota": "Bismarck",
    "Ohio": "Columbus",
    "Oklahoma": "Oklahoma City",
    "Oregon": "Salem",
    "Pennsylvania": "Harrisburg",
    "Rhode Island": "Providence",
    "South Carolina": "Columbia",
    "South Dakota": "Pierre",
    "Tennessee": "Nashville",
    "Texas": "Austin",
    "Utah": "Salt Lake City",
    "Vermont": "Montpelier",
    "Virginia": "Richmond",
    "Washington": "Olympia",
    "West Virginia": "Charleston",
    "Wisconsin": "Madison",
    "Wyoming": "Cheyenne"
}


class CapitalQuizApp:

    def __init__(self, root):
        self.root = root
        self.root.title("U.S. State Capitals Quiz")
        self.root.configure(bg="#1E1E1E")
        window_width, window_height = 400, 400

        self.root.geometry(f"{window_width}x{window_height}")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.states = list(states_and_capitals.keys())
        random.shuffle(self.states)

        self.index = 0
        self.mode = tk.StringVar(value="Multiple Choice")

        self.correct = 0
        self.incorrect = 0

        self.revealed_chars = 0
        self.mc_hint_used = 0

        tk.Label(root, text="Choose Mode:", bg="#1E1E1E", fg="white").pack()

        self.mode_combo = ttk.Combobox(root,
                                       textvariable=self.mode,
                                       values=["Multiple Choice", "Text Input"],
                                       state="readonly"
                                       )
        self.mode_combo.bind("<<ComboboxSelected>>", self.change_mode)
        self.mode_combo.pack()

        self.state_label = tk.Label(root, text="", font=("Arial", 18), bg="#1E1E1E", fg="white")
        self.state_label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14))

        self.mc_frame = tk.Frame(root, bg="#1E1E1E")
        self.mc_buttons = []
        for i in range(4):
            btn = tk.Button(self.mc_frame,
                            text="",
                            font=("Arial", 12),
                            width=30,
                            bg="gray30",
                            fg="white",
                            command=lambda e=i: self.check_mc(i)
            )

            btn.pack(pady=2)
            self.mc_buttons.append(btn)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_text)
        self.submit_button.pack(pady=5)
        self.submit_button.config(state="disabled")  # Disabled for Multiple Choice mode

        self.hint_button = tk.Button(root, text="Hint", command=self.give_hint)
        self.hint_button.pack(pady=5)

        self.feedback = tk.Label(root, text="", bg="#1E1E1E", fg="orange", font=("Arial", 12))
        self.feedback.pack(pady=5)

        self.score_label = tk.Label(root, text="Correct: 0 | Incorrect: 0", bg="#1E1E1E", fg="white")
        self.score_label.pack()

        # Pack multiple choice frame by default
        self.mc_frame.pack()
        self.load_question()


    def change_mode(self, event=None):
        self.entry.pack_forget()
        self.mc_frame.pack_forget()
        self.submit_button.config(state="normal")
        self.hint_button.config(state="normal")
        self.revealed_chars = 0
        self.mc_hint_used = 0

        if self.mode.get() == "Text Input":
            self.entry.pack(pady=5)
        else:
            self.mc_frame.pack()
            self.submit_button.config(state="disabled")

        self.load_question()


    def load_question(self):
        self.revealed_chars = 0
        self.mc_hint_used = 0
        self.entry.delete(0, tk.END)
        for btn in self.mc_buttons:
            btn.config(state="normal", bg="gray30")

        self.current_state = self.states[self.index]
        self.correct_answer = states_and_capitals[self.current_state]
        self.state_label.config(text=self.current_state)
        self.feedback.config(text="")

        if self.mode.get() == "Multiple Choice":
            all_capitals = list(states_and_capitals.values())
            choices = random.sample([c for c in all_capitals if c != self.correct_answer], 3)
            choices.append(self.correct_answer)
            random.shuffle(choices)
            for i, btn in enumerate(self.mc_buttons):
                btn.config(text=choices[i])


    def check_text(self):
        user_answer = self.entry.get().strip().lower()
        correct = self.correct_answer.lower()
        if user_answer == correct:
            self.correct += 1
            self.feedback.config(text="Correct!", fg="lightgreen")
        else:
            self.incorrect += 1
            self.feedback.config(text=f"Incorrect. The correct answer is {self.correct_answer}.", fg="tomato")
        self.update_score()
        self.next_question()


    def check_mc(self, index):
        chosen = self.mc_buttons[index].cget("text")
        if chosen == self.correct_answer:
            self.correct += 1
            self.feedback.config(text="Correct!", fg="lightgreen")
        else:
            self.incorrect += 1
            self.feedback.config(text=f"Incorrect. The correct answer is {self.correct_answer}.", fg="tomato")
        self.update_score()
        self.next_question()


    def update_score(self):
        self.score_label.config(text=f"Correct: {self.correct} | Incorrect: {self.incorrect}")


    def next_question(self):
        self.index += 1
        if self.index >= len(self.states):
            self.feedback.config(text="Quiz complete!")
            for btn in self.mc_buttons:
                btn.config(state="disabled")
            self.entry.config(state="disabled")
            self.submit_button.config(state="disabled")
            self.hint_button.config(state="disabled")
        else:
            self.load_question()


    def give_hint(self):
        if self.mode.get() == "Text Input":
            if self.revealed_chars < len(self.correct_answer):
                self.revealed_chars += 1
                self.show_hint_text()
        else:
            if self.mc_hint_used == 0:
                wrong_buttons = [btn for btn in self.mc_buttons if btn.cget("text") != self.correct_answer]
                to_disable = random.sample(wrong_buttons, 2)
                for btn in to_disable:
                    btn.config(state="disabled", bg="gray15")
                self.mc_hint_used += 1
            elif self.mc_hint_used == 1:
                self.revealed_chars += 1
                self.show_hint_text()
                self.mc_hint_used += 1


    def show_hint_text(self):
        hint_display = ""
        for i, c in enumerate(self.correct_answer):
            if i < self.revealed_chars: hint_display += c
            elif c == ' ': hint_display += '  '
            else: hint_display += "_ "
        self.feedback.config(text=f"Hint: {hint_display.strip()}", fg="orange")


if __name__ == "__main__":
    root = tk.Tk()
    app = CapitalQuizApp(root)
    root.mainloop()
