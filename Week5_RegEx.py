"""
Series: Python Bootcamp
Week: 5
Title: RegEx Basics
Author: Nick Lombardi
Date: July 9, 2021
Libraries Used: re
"""

import re


def search_text(pattern, text):
    match = re.search(pattern, text)
    if match:
        print("Found match: ", match.group())
    else:
        print("Match not found")
    return match.group() if match else None


def find_all(pattern, text):
    matches = re.findall(pattern, text)
    if matches:
        print("Matches found: ", matches)
    return matches


def sub_text(pattern, replacement, text):
    newText = re.sub(pattern, replacement, text)
    if newText:
        print("Text changed to: ", newText)
    return newText


def replace_white(match_obj):
    if match_obj.group(1):
        return ""
    if match_obj.group(2):
        return " "


def replace_num(match_obj):
    for i in match_obj.group():
        return replacements[i]


"""
PATTERNS
---------------------------

"([A-Za-z]+[^0-9]+)([0-9]+)"

.  -> matches any single character except newline '\n'
\w -> matches any letter/digit/ or underscore similar to [A-Za-z0-9_] | letters: [A-Za-z] | numbers: [0-9] 
\W -> matches any non-word characters ie) $, %, & | similar to: [^\w]
\s -> matches a single whitespace character (space, newline, return, tab) | newline: \n | return: \r | tab: \t
\S -> matches any non-whitespace character
\d -> matches any digit [0-9]
\b -> boundary between word and non-word
^  -> match at the start of a string
$  -> match at the end of a string
\  -> used to match special characters, ie) "." since this is a regex pattern use \. to match a period | slash: \\

REPETITION
---------------------------
+  -> 1 or more occurrences of the pattern on its left
*  -> 0 or more occurrences of the pattern on its left
?  -> match 0 or 1 occurrences of the pattern on its left
"""

"""
EG 1: Basic searches
"""
text = "Can you find the err0r?"

# Find the number in the text
pattern = r'\d'
search_text(pattern, text)

# Find a word where the number is present in the word
pattern = r'\w+\d\w'  # r'\w*\d\w*'
search_text(pattern, text)

# Find the whole phrase
pattern = r'[\w+\s]+'  # r'[\w+\s]+?' --> returns only C | r'[\w+\s]+\?' --> returns whole sentence above
search_text(pattern, text)

"""
EG 2: Finding all matches and grouping
"""
text = "Can you find the err0r in the t3xt that I am wr1ting on? The br0wn f0x jumps."

# Find the number in the text
pattern = r'\d'
search_text(pattern, text)
find_all(pattern, text)

# Find a word where the number is present in the word
pattern = r'\w+\d\w'  # r'\w*\d\w*' --> Will return the full word as it looks for 0 or more letters after the #
search_text(pattern, text)
find_all(pattern, text)

pattern = r'[\w+\s]+'
search_text(pattern, text)
find_all(pattern, text)

"""
EG 3: Substituting text for matches
"""

# Replacing whitespaces
text = "  Can you       find the err0r in the   t3xt that I am wr1ting  on?  "
pattern = r'^\s+'  # r'\?\s+$' --> replace ? and space with a .
                    # r'^\s+' --> replace space at the beginning
                    # r'^\s+|\s+$' --> replace the spaces at the beg and end
replacement = " "
sub_text(pattern, replacement, text)

# Replacing whitespaces with groups and function call
text = "  Can you   find the err0r in the   t3xt that I am wr1ting  on?  "
pattern = r'(^\s+|\s+$)|(\s+)'
sub_text(pattern, replace_white, text)

# Replacing numbers with letters
replacements = {'1': 'i', '3': 'e', '0': 'o'}
text = "Can you find the err0r in the t3xt that I am wr1ting on?"
pattern = r'(\d)'
sub_text(pattern, replace_num, text=text)

"""
EG 4: Reading from a text file and substituting language to write back to a new file
"""
