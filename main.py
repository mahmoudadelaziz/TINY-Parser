# Imports
from helper import * # some helper functions and variables

# Taking input
print("Please Enter the name of the tokens list file (with extension, like tokens.txt): ")
input_name = input()
Source_Code = open(input_name, 'r')
# Read the file line by line (and insert each line in the list)
Lines = Source_Code.readlines()
# Now we have a list of lines (as strings), we can close the file
Source_Code.close()
# organizing tokens as a long list of lists [[stringValue, type], [stringValue1, type1], etc.]
tokens = [line.split(r',') for line in Lines]
# cleaning up the tokens list (of spaces and new line chars, etc.)
tokens = [[item[0].strip(), item[1].strip()] for item in tokens]

# Define the current token
number_of_tokens = len(tokens)
token = tokens[cursor][0]
# When (cursor == number_of_tokens & error_state = False) this means the given tokens
# correspond to a syntactically valid TINY Language code.

# Debugging
print(tokens)
print("--"*40)
print(f"The current parser index is {cursor}")
print(f"The current token is {token}")