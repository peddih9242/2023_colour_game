from tkinter import *
from functools import partial
import csv
import random


# takes in how many rounds the user wants
class ChooseRounds:

    def __init__(self):
        # invoke play class with 3 rounds for testing purposes
        self.to_play(3)

    # sends user to the play window
    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window)
        root.withdraw()


# play component, where the user plays the game
class Play:

    def __init__(self, num_rounds):

        self.rounds_wanted = IntVar()
        self.rounds_played = IntVar()

        self.rounds_wanted.set(num_rounds)
        self.rounds_played.set(0)

        self.user_scores = []
        self.comp_scores = []

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
        self.to_stats_button = self.control_button_ref[1]

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
        self.to_stats_button.config(state=DISABLED)
        Statistics(self)

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


# shows user instructions to play the game
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
                                        width=15, activebackground="#e8a664")
        self.close_help_button.grid(row=2, padx=5, pady=5)

    # function closes help window
    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# statistics window
class Statistics:

    def __init__(self, partner):

        rounds_played = 10
        stats_bg_colour = "#a7d5f2"

        # set up hard coded score lists to be used as statistics
        self.user_scores = [20, 14, 14, 13, 14, 11, 20, 10, 20, 11]
        self.comp_scores = [12, 4, 6, 20, 20, 14, 10, 14, 16, 12]

        self.row_details_column = ["", "Total", "Best Score", "Worst Score", "Average Score"]
        self.user_score_list = self.get_stats(self.user_scores, "User")
        self.comp_score_list = self.get_stats(self.comp_scores, "Computer")

        # background formatting for heading, odd and even rows
        head_back = "#FFFFFF"
        odd_rows = "#C9D6E8"
        even_rows = stats_bg_colour

        row_formats = [head_back, odd_rows, even_rows, odd_rows, even_rows]

        # data for labels (one label / sub list)
        all_labels = []

        count = 0
        for item in range(0, len(self.user_score_list)):
            all_labels.append([self.row_details_column[item], row_formats[count]])
            all_labels.append([self.user_score_list[item], row_formats[count]])
            all_labels.append([self.comp_score_list[item], row_formats[count]])
            count += 1

        # set up statistics window with working table
        self.stats_box = Toplevel()
        self.stats_box.protocol("WM_DELETE_WINDOW", partial(self.close_stats,
                                                            partner))

        self.stats_frame = Frame(self.stats_box, padx=10, pady=10, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.stats_heading = Label(self.stats_frame, text="Statistics",
                                   font=("Arial", "16", "bold"), bg=stats_bg_colour)
        self.stats_heading.grid(row=0, padx=5, pady=5)

        self.stats_label = Label(self.stats_frame, text="Here are your game statistics...",
                                 font=("Arial", "16"), bg=stats_bg_colour, justify="left")
        self.stats_label.grid(row=1, padx=5, pady=5)

        self.data_frame = Frame(self.stats_frame, padx=10, pady=10, bg=stats_bg_colour,
                                borderwidth=1, relief="solid")
        self.data_frame.grid(row=2)

        # make table with statistics of game
        for item in range(len(all_labels)):

            self.data_label = Label(self.data_frame, width=10, bg=all_labels[item][1],
                                    height=2, padx=5, text=all_labels[item][0])
            self.data_label.grid(row=item // 3, column=item % 3, padx=0, pady=0)

        self.close_stats_button = Button(self.stats_frame, bg="#004C99",
                                         fg="#FFFFFF", width=15, text="Dismiss",
                                         command=lambda: self.close_stats(partner),
                                         activebackground="#1b6dbf", height=2)
        self.close_stats_button.grid(row=3, padx=5, pady=5)

    # function calculates needed statistics (best, worst, total, average scores)
    def get_stats(self, score_list, entity):
        best_score = max(score_list)
        worst_score = min(score_list)
        total_score = sum(score_list)
        average_score = total_score / len(score_list)

        return [entity, total_score, best_score, worst_score, average_score]

    def close_stats(self, partner):
        partner.to_stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
