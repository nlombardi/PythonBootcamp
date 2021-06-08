"""
Series: Python Bootcamp
Week: 2
Title: Try and Except Clauses
Author: Nick Lombardi
Date: June 4, 2021
"""

import os
import requests
from requests import ConnectionError

# Define the directory where the data is stored
path = os.environ['ONEDRIVE'] + f"\\Documents\\Data\\2021\\BIS\\"


"""
Try and Except Clauses: help function and list of subclasses of the Exception class
"""
help(Exception)
print(Exception.__subclasses__())
help(NameError)


"""EG. 1: Div by 0"""


def divide_numbers(num1: int, num2: int):  # this function takes two integers as inputs
    try:  # we try to print the division of the two integers
        print(num1/num2)
    except ZeroDivisionError as e:  # If the second integer is 0, we will get a divide by zero error
        print("You tried to divide by zero, please enter another number: ")
        # After handling the error we redirect them to input another number
        divide_numbers(num1, int(input("Enter a second number: ")))


# Calls the divide_numbers function and asks the user to input two numbers, we transform them to integers..
    # Will get a value error if you try and input a letter or string instead of a number we address in the next part
divide_numbers(int(input("Enter a number:")), int(input("Enter a second number:")))


def get_numbers():  # This function handles the value error of a user inputting a letter instead of a number for above
    try:  # We try and get the input of the two numbers then call the divide_numbers function
        num1 = int(input("Enter a number: "))
        num2 = int(input("Enter a second number: "))
        divide_numbers(num1, num2)
    except ValueError as e:  # If the user inputs a letter instead we will get a value error which we handle below
        print("You entered a non-number! Please try again.")
        # After stating that they did not input a number we recall this function again
        get_numbers()


# Calls the get_numbers function
get_numbers()


""" EG. 2: Requests and Library Defined Exceptions"""


def get_url(urls):  # Function takes urls as input and tries to get the url for each
    for url in urls:  # Loops through the urls
        try:  # Try and get the url
            req = requests.get(url)  # Calls request library to get the url
        except ConnectionError as e:  # A connection error is raised from the requests library if it fails to get url
            print("Failed to connect")  # We handle by telling the user it failed and break the for loop
            break
        finally:  # This always runs regardless if our above code works or fails
            print("Get url completed, regardless if connection error occurs")
        # If we have the statement outside of our finally clause, and a connection error occurs, it will not print below
        print("Get url completed, only when no connection error occurs")


# Calls the function get_url with two examples one that raises a connection error the other does not
get_url(["http://www.google.ca", "http://www.dsfagasdh.com"])
get_url(["http://www.google.ca", "http://www.learncpp.com"])


""" EG. 3: Redirection and raising an error"""


def make_list():  # The function makes a list from all the files in a path
    print("Getting all the files in the defined path")
    files = os.listdir(path)  # Uses the OS library to get the files in a directory (path)
    return files


def print_list(file_list):  # The fn takes a file_list and checks to see if there are items, if not raise ValueError
    try:  # Try and see if the file_list has any files
        if not file_list:
            raise ValueError  # If there are no files (above statement returns False) we raise a ValueError (can be any)
        else:
            for file in file_list:  # If there are files, print each file
                print(file)
    except ValueError:  # Once we raise the ValueError an exception will be triggered and the below code will run
        print("List was not generated, redirecting to get the list..")
        print_list(make_list())  # Calls the get_list fn again with by passing the returned list of the make_list fn
    return None  # This function does not return anything because it just prints the list of files


files = []  # Defines files as an empty list
print_list(files)  # Calls print_list with an empty list
files_2 = ["File 1", "File 2"]  # Defines another list with two files
print_list(files_2)  # Call print_list with the files_2 list, will not raise the ValueError because the list isn't empty
