from tkinter import *


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

        self.round_button = Button(self.button_frame, text="3 Rounds",
                                   width=12, bg="#f52a20")
        self.round_button.grid(row=0, column=0, padx=5, pady=5)

        self.round_button_2 = Button(self.button_frame, text="5 Rounds",
                                     width=12, bg="#15e631")
        self.round_button_2.grid(row=0, column=1, padx=5, pady=5)

        self.round_button_3 = Button(self.button_frame, text="10 Rounds",
                                     width=12, bg="#3027db")
        self.round_button_3.grid(row=0, column=2, padx=5, pady=5)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Game")
    ChooseRounds()
    root.mainloop()
