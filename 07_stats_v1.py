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

        # set up background colours
        win_colour = "#D5E8D4"
        lose_colour = "#F8CECC"

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
        else:
            round_results_bg = lose_colour

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
        else:
            round_results_bg = lose_colour
            status = "You Lose!"

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

    def __init__(self, partner):

        self.stats_box = Toplevel()
        self.stats.protocol("WM_DELETE_WINDOW", partial(self.close_help,
                                                           partner))
    def close_stats(self, partner):
        partner.to_stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
