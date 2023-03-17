from tkinter import *
from functools import partial
import csv
import random


class ChooseRounds:

    def __init__(self):
        self.intro_frame = Frame()
        self.intro_frame.grid()

        self.start_title = Label(self.intro_frame, text="Colour Quest",
                                 font=("Arial", "16", "bold"))
        self.start_title.grid(row=0, padx=5, pady=5)

        start_instructions_text = "In each round you will be given six different colours" \
                                  " to choose from. Pick a colour and see if you can beat the" \
                                  " computer's score!\n\nTo begin, choose how many rounds you'd" \
                                  " like to play..."

        self.start_instructions = Label(self.intro_frame, text=start_instructions_text,
                                        wraplength=400, justify="left")
        self.start_instructions.grid(row=1, padx=5, pady=5)

        self.button_frame = Frame(self.intro_frame)
        self.button_frame.grid(row=2)

        button_fg = "#FFFFFF"

        round_button_properties = [
            ["#f52a20", 3],
            ["#15e631", 5],
            ["#3027db", 10]
        ]

        # create round buttons
        for item in range(3):
            self.round_button = Button(self.button_frame, text=f"{round_button_properties[item][1]} Rounds",
                                       width=12, bg=round_button_properties[item][0], fg=button_fg,
                                       command=lambda i=item: self.to_play(round_button_properties[i][1]))
            self.round_button.grid(row=0, column=item, padx=5, pady=5)

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

        # get all colours for use in game
        self.all_colours = self.get_all_colours()

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

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

        # get colours for buttons for the round
        button_colours_list = self.get_round_colours(self.all_colours)

        self.choice_frame = Frame(self.play_frame, padx=10, pady=10)
        self.choice_frame.grid(row=2)

        for item in range(6):
            self.choice_button = Button(self.choice_frame, text=button_colours_list[item][0],
                                        width=15, bg=button_colours_list[item][0],
                                        fg=button_colours_list[item][2],
                                        command=lambda i=item: self.to_compare(button_colours_list[i][1]))
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

    # function closes play window and shows initial choose rounds window
    def close_play(self):
        # reshow root (choose round) and destroy current box
        # to allow new game to start
        root.deiconify()
        self.play_box.destroy()

    # get all colour data from csv file
    def get_all_colours(self):

        # open csv file and create reader
        csv_file = open("00_colour_list_hex_v3.csv")
        colour_data = list(csv.reader(csv_file, delimiter=','))

        # remove first entry in list (header row)
        colour_data.pop(0)

        # add all colour data from csv file to list
        return colour_data

    # function gets the colours to be used in the round (no duplicate scores
    # or colours)
    def get_round_colours(self, all_colours):
        colour_scores = []
        round_colour_list = []

        while len(round_colour_list) < 6:

            colour_choice = random.choice(all_colours)

            if colour_choice[1] not in colour_scores:

                round_colour_list.append(colour_choice)
                colour_scores.append(colour_choice[1])

            all_colours.remove(colour_choice)

        return round_colour_list

    def to_compare(self, user_score):
        print("Your score is:", user_score)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
