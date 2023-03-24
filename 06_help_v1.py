from tkinter import *
from functools import partial
import csv
import random


class ChooseRounds:

    def __init__(self):
        # invoke play class with 3 rounds for testing purposes
        self.to_play(3)

    # sends user to the play window
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

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        self.control_frame = Frame(self.play_frame, padx=10)
        self.control_frame.grid(row=6, padx=10, pady=10)

        # list to hold the control buttons so that text of 'start over'
        # button can easily be changed to 'game over'
        self.control_button_ref = []

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        for item in range(3):
            self.make_control_button = Button(self.control_frame, width=15,
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))

            self.control_button_ref.append(self.make_control_button)

            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

        self.to_help_button = self.control_button_ref[0]

    # sends user to function needed based on button pressed
    def to_do(self, action):
        if action == "get help":
            self.get_help()
        elif action == "get stats":
            self.get_stats()
        else:
            self.close_play()

    # directs user to table of statistics
    def get_stats(self):
        print("You chose to get the statistics")

    # directs user to help window
    def get_help(self):
        # disable help button (prevents multiple instances of help window occurring)
        self.to_help_button.config(state=DISABLED)
        Help(self)

    # function closes play window and shows initial choose rounds window
    def close_play(self):
        # reshow root (choose round) and destroy current box
        # to allow new game to start
        root.deiconify()
        self.play_box.destroy()


class Help:

    def __init__(self, partner):

        self.help_box = Toplevel()
        self.help_box.protocol("WM_DELETE_WINDOW", partial(self.close_help,
                                                           partner))

        self.help_frame = Frame(self.help_box, padx=10, pady=10, bg="#FFE6CC")
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame, text="Help / Hints",
                                  font=("Arial", "16", "bold"),
                                  bg="#FFE6CC", justify="left")
        self.help_heading.grid(row=0, padx=5, pady=5)

        help_instructions = "Your goal in this game is to beat the computer and you" \
                            " have an advantage - you get to choose your colour first." \
                            " The points associated with the colours are based on hte colour's" \
                            " hex code. The higher the value of the colour, the greater your score.\n\n" \
                            "To see your statistics, click on the 'Statistics' button. Win the game by" \
                            " scoring more than the computer overall. Don't be discouraged if you don't win" \
                            " every round, it's your overall score that counts.\n\nGood luck! Choose carefully."

        self.help_instructions = Label(self.help_frame, text=help_instructions,
                                       wraplength=350, justify="left", bg="#FFE6CC")
        self.help_instructions.grid(row=1, padx=5, pady=5)

        self.close_help_button = Button(self.help_frame, text="Dismiss",
                                        fg="#FFFFFF", bg="#CC6600",
                                        command=lambda: self.close_help(partner),
                                        width=15)
        self.close_help_button.grid(row=2, padx=5, pady=5)

    # function closes help window
    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
