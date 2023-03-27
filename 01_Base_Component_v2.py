from tkinter import *
from functools import partial
import csv
import random


# takes in how many rounds the user wants
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
                                       wraplength=350, justify="left")
        self.play_instructions.grid(row=1)

        # get colours for buttons for the round
        self.button_colours_list = self.get_round_colours(self.all_colours)

        # list to hold instances of different buttons
        self.choice_button_ref = []

        self.choice_frame = Frame(self.play_frame, padx=10, pady=10)
        self.choice_frame.grid(row=2)

        for item in range(6):
            self.choice_button = Button(self.choice_frame, text=self.button_colours_list[item][0],
                                        width=15, bg=self.button_colours_list[item][0],
                                        fg=self.button_colours_list[item][2],
                                        command=lambda i=item: self.to_compare(self.button_colours_list[i]))

            # add button to reference list for later configuration
            self.choice_button_ref.append(self.choice_button)

            # set up grid of multiple buttons with 3 columns and 2 rows
            if item < 3:
                self.choice_button.grid(row=0, column=item, padx=5, pady=5)
            else:
                self.choice_button.grid(row=1, column=item - 3, padx=5, pady=5)

        computer_choice = "The Computer's choice will appear here"
        self.comp_choice_label = Label(self.play_frame, text=computer_choice, bg="#c4c4c4",
                                       width=50)
        self.comp_choice_label.grid(row=3, padx=5, pady=5)

        self.rounds_frame = Frame(self.play_frame, padx=10, pady=10)
        self.rounds_frame.grid(row=4)

        self.round_info = Label(self.rounds_frame, text="Round 1: User -     Computer: -",
                                bg="#fffdd1", width=35)
        self.round_info.grid(row=0, column=0, padx=5)

        self.next_round = Button(self.rounds_frame, text="Next Round",
                                 width=12, bg="#008BFC", state=DISABLED,
                                 command=lambda: self.new_round())
        self.next_round.grid(row=0, column=1, padx=5)

        # at start, get 'new round'
        self.new_round()

        self.total_stats = Label(self.play_frame, text="Total Score: User: - \tComputer: -",
                                 bg="#fffdd1", width=50)
        self.total_stats.grid(row=5, padx=5, pady=5)

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

        # initiate help and stats buttons as variables to make calling buttons easier
        self.to_help_button = self.control_button_ref[0]
        self.to_stats_button = self.control_button_ref[1]

        # disable statistics button when no rounds are played
        self.to_stats_button.config(state=DISABLED)

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
        Statistics(self, self.user_scores, self.comp_scores)

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

    # updates gui to show a new round
    def new_round(self):

        # disable next button (re-enabled at end of the round)
        self.next_round.config(state=DISABLED)

        # get new colours for buttons
        self.button_colours_list = self.get_round_colours(self.all_colours)

        # set button bg, fg and text
        count = 0
        for item in self.choice_button_ref:
            item['fg'] = self.button_colours_list[count][2]
            item['bg'] = self.button_colours_list[count][0]
            item['text'] = self.button_colours_list[count][0]
            item['state'] = NORMAL

            count += 1

        # retrieve numbers of rounds wanted / played
        # and update heading
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)

        new_heading = "Choose: Round {} out of {}".format(current_round, how_many)

        self.rounds_heading.config(text=new_heading)

    # alter information, stats and colour buttons
    def to_compare(self, user_choice):

        how_many = self.rounds_wanted.get()

        # increase the rounds played by one
        current_round = self.rounds_played.get()

        self.rounds_played.set(current_round)

        # disable colour buttons
        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        # enable statistics button
        self.to_stats_button.config(state=NORMAL)

        # set up background colours
        win_colour = "#D5E8D4"
        lose_colour = "#F8CECC"
        tie_colour = "#FFFFFF"

        # retrieve user score, make it into an integer
        # and add to list for stats
        current_user_score = int(user_choice[1])
        self.user_scores.append(current_user_score)

        # remove user choice from button colours list (for computer choice)
        remove_colour = self.button_colours_list.index(user_choice)
        self.button_colours_list.remove(self.button_colours_list[remove_colour])

        # get computer choice and add to list for stats,
        # change to integer before appending when getting score
        comp_choice = random.choice(self.button_colours_list)
        current_comp_score = int(comp_choice[1])

        self.comp_scores.append(current_comp_score)

        comp_announce = "The computer chose {}".format(comp_choice[0])
        self.comp_choice_label.config(text=comp_announce,
                                      bg=comp_choice[0],
                                      fg=comp_choice[2])

        # get colours and show results
        if current_user_score > current_comp_score:
            round_results_bg = win_colour
        elif current_user_score < current_comp_score:
            round_results_bg = lose_colour
        else:
            round_results_bg = tie_colour

        rounds_outcome_txt = "Round {}: User {} \tComputer {}".format(current_round,
                                                                      current_user_score,
                                                                      current_comp_score)

        self.round_info.config(bg=round_results_bg,
                               text=rounds_outcome_txt)

        # get total scores for user and computer
        total_user_score = sum(self.user_scores)
        total_comp_score = sum(self.comp_scores)

        # get colours and show results for total game
        if total_user_score > total_comp_score:
            round_results_bg = win_colour
            status = "You Win!"
        elif total_user_score < total_comp_score:
            round_results_bg = lose_colour
            status = "You Lose!"
        else:
            round_results_bg = tie_colour
            status = "You Tied!"

        total_outcome_txt = "Total Score: User {} \tComputer {}".format(total_user_score,
                                                                        total_comp_score)

        self.total_stats.config(text=total_outcome_txt,
                                bg=round_results_bg)

        # if the game is over, disable all buttons and change text
        # of "next" button to either "You Win" or "You Lose" and
        # disable all buttons
        if current_round == how_many:
            # disable 'next' button and change text based on if user won or lost
            self.next_round.config(text=status,
                                   state=DISABLED)

            # update 'start over' button to 'play again'
            start_over_button = self.control_button_ref[2]
            start_over_button.config(text="Play Again",
                                     bg="#009900")

            # change all colour choice backgrounds to light gray
            for item in self.choice_button_ref:
                item['bg'] = "#C0C0C0"

        else:
            self.next_round.config(state=NORMAL)


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

    def __init__(self, partner, user_scores, comp_scores):

        stats_bg_colour = "#a7d5f2"

        self.row_details_column = ["", "Total", "Best Score", "Worst Score", "Average Score"]
        self.user_score_list = self.get_stats(user_scores, "User")
        self.comp_score_list = self.get_stats(comp_scores, "Computer")

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

        rounded_average = round(average_score, 1)

        return [entity, total_score, best_score, worst_score, rounded_average]

    def close_stats(self, partner):
        partner.to_stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
