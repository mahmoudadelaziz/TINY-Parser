# matching function
# For the grammar:
# exp --> factor addop factor
# factor --> (number)

index = 0
scanner_output = "(5)"


def match(str):
    global index, scanner_output
    if(scanner_output[index] == str):
        #consume and advance
        index = index + 1
    else:
        # error
        print("SYNTAX ERROR!")


def fact(str):
    global index
    match("(")
    if(str[index].isnumeric()):
        index = index + 1
    else:
        print("SYNTAX ERROR!")
    match(")")


fact(scanner_output)
print(f"The parser cursor arrived at {index}!")
print("ALL GOOD!")
