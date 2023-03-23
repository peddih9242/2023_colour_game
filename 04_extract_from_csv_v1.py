import csv


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

# output all colour data from list
for colour in all_colours:
    print(colour)
