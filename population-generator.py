# Author: Alyssa Lada
# Course: CS-361
# Date Created: 02/2021
# Date Last Modified: 02/14/2021
# Program Title: Population Generator
# Description:  This program creates a graphic user interface and an outfile.
# It receives state and year from the user via GUI or an input.csv file, calls the US Census API, and returns
# the total population for the state and year. The original year and state, and the retrieved population are
# exported to output.csv in the same directory.  The program runs from the command line.


from tkinter import *
from tkinter import ttk
import requests
import csv
import sys

# Instructions
print("\nFor graphic user interface, run <python3 population-generator.py> on the command line.")
print("For csv file input, run <python3 population-generator.py input.csv> on command line.")
print("Output.csv will be created in the same directory as the program for the last run query.")


def create_outfile(input_year, input_state, output_population_size):
    """Writes output.csv with year, state, and population info."""
    with open("output.csv", 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["input_year", "input_state", "output_population_size"])
        writer.writerow([input_year, input_state.upper(), output_population_size])
    print("\nOutput.csv created.")

def call_census_api(year, state_code):
    """Returns the total population for a given year (2005 - 2019) and two digit state code."""

    def convert_state_code_to_num(state_code):
        """Converts two-letter state code to API numeric code."""
        state_abbr_dict = [("01", "AL"), ("02", "AK"), ("04", "AZ"), ("05", "AR"),
                           ("06", "CA"), ("08", "CO"), ("09", "CT"), ("10", "DE"),
                           ("11", "DC"), ("12", "FL"), ("13", "GA"), ("15", "HI"),
                           ("16", "ID"), ("17", "IL"), ("18", "IN"), ("19", "IA"),
                           ("20", "KS"), ("21", "KY"), ("22", "LA"), ("23", "ME"),
                           ("24", "MD"), ("25", "MA"), ("26", "MI"), ("27", "MN"),
                           ("28", "MS"), ("29", "MO"), ("30", "MT"), ("31", "NE"),
                           ("32", "NV"), ("33", "NH"), ("34", "NJ"), ("35", "NM"),
                           ("36", "NY"), ("37", "NC"), ("38", "ND"), ("39", "OH"),
                           ("40", "OK"), ("41", "OR"), ("42", "PA"), ("44", "RI"),
                           ("45", "SC"), ("46", "SD"), ("47", "TN"), ("48", "TX"),
                           ("49", "UT"), ("50", "VT"), ("51", "VA"), ("53", "WA"),
                           ("54", "WV"), ("55", "WI"), ("56", "WY"), ("72", "PR")]

        state_num = "*"
        for tup in state_abbr_dict:
            if tup[1] == state_code.upper():
                state_num = tup[0]

        return state_num

    # create api url
    hostname = "https://api.census.gov/data/"
    data_set_name_acronym = "acs/acs1"
    key = "d19aa6beb1cd793f0c25452ff63400bbe5fb8cd6"
    state_num = convert_state_code_to_num(state_code)
    url = hostname + year + "/" + data_set_name_acronym + "?get=NAME,B01001_001E&for=state:" + state_num + "&key=" + key

    response = requests.get(url)

    # convert api response data to display format
    population = response.text.split(",")[4][1:-1]  # locate and trim population string

    return population


def create_GUI():
    """GUI to collect year and state input from user."""

    def get_population(*args):
        """Calls call_census_api and create_outfile using year and state textvariables from interface."""
        retrieved_population = call_census_api(year.get(), state.get())  # text variables auto update with tk

        population.set(retrieved_population)  # displays on gui

        # automatically create outfile
        create_outfile(year.get(), state.get(), retrieved_population)

    # set the main application window
    root = Tk()
    root.title("Population Generator")

    # create the content frame window
    mainframe = ttk.Frame(root, padding="12 12 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # input widget for year selection
    year = StringVar()
    year_entry = ttk.Entry(mainframe, width=4, textvariable=year)
    year_entry.grid(column=2, row=1, sticky=(W, E))
    ttk.Label(mainframe, text="Enter census year (2005-2019):").grid(column=1, row=1, sticky=(W, E))

    # input widget for state selection
    state = StringVar()
    state_entry = ttk.Entry(mainframe, width=2, textvariable=state)  # specify the parent that the widget will be placed inside
    state_entry.grid(column=2, row=2, sticky=(W, E))
    ttk.Label(mainframe, text="Enter state code (example: TX):").grid(column=1, row=2, sticky=(W, E))

    # get population button
    ttk.Button(mainframe, text="Get Population", command=get_population).grid(column=2, row=3, sticky=E)

    # population output screen
    population = StringVar()
    ttk.Label(mainframe, text="Population: ").grid(column=1, row=4, sticky=(E, W))
    ttk.Label(mainframe, textvariable=population).grid(column=2, row=4, sticky=(E, W))

    # pad children in mainframe
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    year_entry.focus()
    root.bind("<Return>", get_population)

    root.mainloop()


# CLI entry point
# check if command line start has valid argument
if len(sys.argv) > 1:
    try:
        with open(sys.argv[-1], "r") as in_file:
            csv_year_state = in_file.read().splitlines()[1].split(",")

            year = csv_year_state[0]
            state = csv_year_state[1]
            population = call_census_api(year, state)

            create_outfile(year, state, population)

    except IOError:
        print("Invalid argument")
else:
    create_GUI()

# Resources
# https://tkdocs.com/tutorial/firstexample.html
# https://docs.python.org/3/library/tkinter.html
# https://www.census.gov/data/developers/guidance/api-user-guide.Example_API_Queries.html
# https://www.programiz.com/python-programming/csv
# https://stackoverflow.com/questions/7033987/python-get-files-from-command-line
# https://docs.python.org/3/library/functions.html#open
