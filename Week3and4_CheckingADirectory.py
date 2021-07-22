"""
Title: Checking the TR Directories
Description: Checks each directory to see if the files have been received for a given date
Author: Nick Lombardi
Date: June 30, 2021

USAGE: Call check_list with the comparison list and the date formatted as YYYYMMDD
"""

import os
import pandas as pd
import smtplib
import ssl
from datetime import datetime, timedelta
import re

# Define the date that we need match the format of the files in the directory
today = datetime.today()
lag = timedelta(2)
check_date = (today-lag).strftime("%Y%m%d")

# Define directories of files and list for comparison
cme_dir = "D:\\CME\\CME_FTP"  # Need to change drive letter to where you have it mapped
ice_dir = "S:\\ICE\\ICE_FTP"  # Need to change drive letter to where you have it mapped
ddr_dir = "V:\\"  # Need to change drive letter to where you have it mapped
list_of_files = os.environ['USERPROFILE'] + "\\PycharmProjects\\Python Bootcamp\\Week 3\\report_names.csv"

# Read the list of files to compare with
compare_list = pd.read_csv(list_of_files)
compare_list = compare_list['File name'].tolist()  # Assigns the file names to a list


def strip_filename(file):
    # ReGex query to find the letters and symbols (group 1) and date (group 2) for a file
    name_to_confirm = re.search(r"([A-Za-z]+[^0-9]+)([0-9]+)", file)
    # If the filename is not as needed to match it will raise an AttributeError
    try:
        name = [name_to_confirm.group(1), name_to_confirm.group(2)]
    except AttributeError:
        name = None
    return name


def check_dir(file_name, date_to_compare, tr_dir, ddr=False):
    confirmed_file_count = 0  # binary to check if the file is there
    missing_file = []  # placeholder to store the files that are missing

    file = file_name + date_to_compare

    # Loop through all the files in the directory for the given TR
    for dir_file in tr_dir:
        check_file = strip_filename(dir_file)  # Assign the result of strip_filename
        if check_file:  # If result of strip_filename is None, returns False and below code won't run
            if ddr:
                if file == check_file[0][:-1] + check_file[1]:  # Checks to see if the item is in the directory
                    confirmed_file_count = 1  # If it is we add one to the confirmed count
            else:
                if file == check_file[0] + check_file[1]:  # Checks to see if the item is in the directory
                    confirmed_file_count = 1  # If it is we add one to the confirmed count

    if confirmed_file_count == 0:
        missing_file = file  # If it is not we add the item to the missing files list

    return confirmed_file_count, missing_file


def check_list(list_to_compare, date_to_compare):
    # Define placeholders for each TR
    ice_count, ddr_count, cme_count = 0, 0, 0
    ice_mis_files, ddr_mis_files, cme_mis_files = [], [], []
    ice_list, ddr_list, cme_list = os.listdir(ice_dir), os.listdir(ddr_dir), os.listdir(cme_dir)
    if ice_list and ddr_list and cme_list:
        print("Directories Scanned!")
    else:
        print("Check your directories, not all files scanned!")

    print("Checking files..")

    for file_name in list_to_compare:  # loop through all the items in the comparison list
        file_tr = file_name[:3]  # Takes the first three letters to see which TR the file is from
        if file_tr == "ICE":
            check = check_dir(file_name, date_to_compare, ice_list)  # Calls check_dir for ICE
            ice_count += check[0]  # If the file is found adds 1, else 0
            if check[1]:  # If the file is missing appends the filename
                ice_mis_files.append(check[1])

        elif file_tr == "DDR":
            pass
            date_to_compare1 = date_to_compare[2:]
            check = check_dir(file_name, date_to_compare1, ddr_list, ddr=True)  # Calls check_dir for DDR
            ddr_count += check[0]
            if check[1]:
                ddr_mis_files.append(check[1])

        elif file_tr == "CME":
            date_to_compare1 = date_to_compare[2:]
            check = check_dir(file_name, date_to_compare1, cme_list)  # Calls check_dir for CME
            cme_count += check[0]
            if check[1]:
                cme_mis_files.append(check[1])

    # Creates a dictionary with all the values for each TR
    tr_files_check = {'TR': ["ICE", "DDR", "CME"],
                      'COUNT': [ice_count, ddr_count, cme_count],
                      'MISSING': [ice_mis_files, ddr_mis_files, cme_mis_files]}
    return tr_files_check


# Call the function to get the results for the search for today's date lagged two days
checked_files = check_list(compare_list, check_date)

for i in range(3):
    print("TR: ", checked_files['TR'][i],
          "\nFILES FOUND: ", checked_files['COUNT'][i],
          "\nMISSING: ", checked_files['MISSING'][i])
    print("\n")

# Email the missing files
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "SENDER_EMAIL"  # Enter your address
receiver_email = "RECEIVER_EMAIL"  # Enter receiver address
password = "PASSWORD_FOR_SENDER_EMAIL"
message = f"""\
Subject: Missing Files List

    Today's file scan:

    TR: {checked_files['TR'][0]}
    FILES FOUND: {checked_files['COUNT'][0]}
    MISSING: {checked_files['MISSING'][0]}

    TR: {checked_files['TR'][1]}
    FILES FOUND: {checked_files['COUNT'][1]}
    MISSING: {checked_files['MISSING'][1]}

    TR: {checked_files['TR'][2]}
    FILES FOUND: {checked_files['COUNT'][2]}
    MISSING: {checked_files['MISSING'][2]}

"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
