from tkinter import *
from functools import partial


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

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        rounds_heading = "Choose - Round 1 of {}".format(num_rounds)
        self.rounds_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold"))
        self.rounds_heading.grid(row=0)

        self.choice_frame = Frame(self.play_box, padx=10, pady=10)
        self.choice_frame.grid(row=1)

        for item in range(6):
            pass

    def close_play(self):
        # reshow root (choose round) and destroy current box
        # to allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
