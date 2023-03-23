from tkinter import *
from functools import partial
import csv
import random

class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window)
        root.withdraw()


class Play:

    def __init__(self, num_rounds):

        self.play_box = Toplevel()

        # if users press cross at top, closes help and
        # 'releases' help button
        self.play_box.protocol("WM_DELETE_WINDOW", partial(self.close_play))

        # variables to work out statistics (when game ends)
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(num_rounds)

        # initially set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # lists to hold computer and user score(s)
        user_scores = []
        computer_scores = []

        # get all colours from .csv file for use in game
        self.all_colours = self.get_all_colours()

        rounds_heading = "Choose - Round 1 of {}".format(num_rounds)
        self.rounds_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold"))
        self.rounds_heading.grid(row=0)

        play_instructions_text = "Choose one of the colours below. When you choose" \
                                 " a colour, the computer's choice and the results of" \
                                 " the round will be revealed."
        self.play_instructions = Label(self.play_frame, text=play_instructions_text,
                                       wraplength=300, justify="left")
        self.play_instructions.grid(row=1)

        self.choice_frame = Frame(self.play_frame, padx=10, pady=10)
        self.choice_frame.grid(row=2)

        for item in range(6):
            self.choice_button = Button(self.choice_frame, text="Choice {}".format(item+1),
                                        width=12, bg="#2aa7c7")
            # set up grid of multiple buttons with 3 columns and 2 rows
            if item < 3:
                self.choice_button.grid(row=0, column=item, padx=5, pady=5)
            else:
                self.choice_button.grid(row=1, column=item-3, padx=5, pady=5)

        computer_choice = "The Computer's choice will appear here"
        self.computer_choice = Label(self.play_frame, text=computer_choice, bg="#c4c4c4",
                                     width=42)
        self.computer_choice.grid(row=3, padx=5, pady=5)

        self.rounds_frame = Frame(self.play_frame, padx=10, pady=10)
        self.rounds_frame.grid(row=4)

        self.round_info = Label(self.rounds_frame, text="Round 3: User -     Computer: -",
                                bg="#d5e8d4")
        self.round_info.grid(row=0, column=0, padx=5)

        self.next_round = Button(self.rounds_frame, text="Next Round",
                                 width=12, bg="#008BFC")
        self.next_round.grid(row=0, column=1, padx=5)

        self.total_stats = Label(self.play_frame, text="Totals:    User: -     Computer: -",
                                 bg="#f8cecc")

        self.control_frame = Frame(self.play_frame, padx=10)
        self.control_frame.grid(row=5)

        self.help_button = Button(self.control_frame, width=12, bg="#d6b11e",
                                  text="Help")
        self.help_button.grid(row=0, column=0, padx=5, pady=5)

        self.help_button = Button(self.control_frame, width=12, bg="#2e378f",
                                  text="Statistics")
        self.help_button.grid(row=0, column=1, padx=5, pady=5)

        self.help_button = Button(self.control_frame, width=12, bg="#9c9c9c",
                                  text="Start Over")
        self.help_button.grid(row=0, column=2, padx=5, pady=5)

    def close_play(self):
        # reshow root (choose round) and destroy current box
        # to allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def get_all_colours(self):
        csv_reader = csv.reader("00_colour_list_hex_v3.csv", delimiter=',')


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
