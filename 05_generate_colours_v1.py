import csv
import random

def get_all_colours():
    # open csv file and create reader
    csv_file = open("00_colour_list_hex_v3.csv")
    csv_reader = csv.reader(csv_file, delimiter=',')

    # set up list to hold colour data and skip first row (has headers)
    colour_data = []
    next(csv_reader)

    # add all colour data from csv file to list
    for item in csv_reader:
        colour_data.append(item)

    return colour_data


# main routine
all_colours = get_all_colours()

# generate 3 rounds of 6 different colours, each colour having a different score
# in the same round and being different colours (no duplicates)
print(f"Initial length: {len(all_colours)}")
for i in range(3):
    colour_scores = []
    round_colour_list = []
    for i in range(6):

        colour_choice = random.choice(all_colours)

        if colour_choice[1] not in colour_scores:

            round_colour_list.append(colour_choice)
            colour_scores.append(colour_choice[1])

        all_colours.remove(colour_choice)

    print("Round Colours: ", round_colour_list)
    print("Colour List Length: ", len(all_colours))

