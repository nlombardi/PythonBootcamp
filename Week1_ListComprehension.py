"""
Series: Python Bootcamp
Week: 1
Title: List Comprehension
Author: Nick Lombardi
Date: May 28, 2021
"""

import pandas as pd
import os
from datetime import datetime

# Uses the datetime library to get today's date and year
full_date = datetime.today().strftime("%d-%b-%Y")
y_date = datetime.today().year

# Define the directory where the data is stored
path = os.environ['ONEDRIVE'] + f"\\Documents\\Data\\{y_date}\\BIS\\"
# Grabs all the files in the directory of the path denoted above
data_list = os.listdir(path)

"""
List Comprehension Examples
"""

"""E.G. 1: Appending file names to a list if they match the extension"""
# List Comprehension (replaces for loop)
csv = [x for x in data_list if x.split(".")[-1] == "csv"]

# For loop
csv_2 = []
for i in data_list:
    if i.split(".")[-1] == "csv":
        csv_2.append(i)


""" EG. 2: Deletes S1 and S2 from the dates and applies Jan and Jul to the end """
# Get the data for the first file (most recent) in the csv list
data = pd.read_csv(path+csv[0])
# Splice of the data set to a new dataframe holding only the notional values and corresponding dates
value_data = data.iloc[:, 30:]

# List Comprehension with Lambda Function
new_dates = [(lambda x, y: x+"-Jan" if y == "S1" else x+"-Jul")(x.split("-")[0], x.split("-")[1])
             for x in value_data.columns.tolist()]


# Function (replaced by lambda) with for loop (replaced by list comprehension)
def parse_dates(dates):
    new_dates_2 = []
    for date in dates:
        date, half = date.split("-")  # 1998-S1 or 1998-S2 1998-Jan or 1998-Jul
        date = date+"-Jan" if half == "S1" else date+"-Jul"
        new_dates_2.append(date)
    return new_dates_2


# Calls the parse_dates function and passes a list of dates from value_data
value_data_cols = parse_dates(value_data.columns.tolist())
