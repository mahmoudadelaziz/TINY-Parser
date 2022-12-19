# matching function
# For the grammar:
# exp --> factor addop factor
# factor --> (number)

index = 0
ip_string = "(3)+(5)"


def error():
    print("SYNTAX ERROR!")


def match(str):
    # meaning: expect str
    global index, ip_string
    if(ip_string[index] == str):
        # consume and advance
        index += 1
    else:
        error()


def fact(str):
    # expect factor
    global index, ip_string
    match("(")
    if(str[index].isnumeric()):
        index += 1
    else:
        error()
    match(")")


def op(str):
    global index, ip_string
    if(str == '+'):
        match('+')
    elif(str == '-'):
        match('-')


def exp(str):
    global index, ip_string
    # Expect an expression:
    # exp --> factor addop factor
    # factor --> (number)
    fact(str)
    op(str[index])
    fact(str)


# Testing
exp(ip_string)
print("ALL GOOD!")  # No syntax errors detected

# Debuggging
print(f"The parser cursor arrived at {index}!")
print("\nTokens traversed: ")
for i in range(index):
    print(ip_string[i])
