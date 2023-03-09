from tkinter import *


class ChooseRounds:

    def __init__(self):

        intro_frame = Frame()
        intro_frame.grid()

        round_button = Button(width=12)
        round_button.grid(intro_frame)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    ChooseRounds()
    root.mainloop()
