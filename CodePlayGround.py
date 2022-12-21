# ---------- Just for experimentation ---------- #
# matching function
# For the grammar:
# exp --> factor addop factor
# factor --> (number)


def DeclareError():
    global error_state
    error_state = True


def CheckSyntax():
    global error_state
    if(error_state == True):
        return "SYNTAX ERROR!"
    else:
        return "ALL GOOD!"


def match(str):
    # meaning: expect str
    global index, ip_string
    if(ip_string[index] == str):
        # consume and advance
        index += 1
    else:
        DeclareError()


def fact(str):
    # expect factor
    global index, ip_string
    match("(")
    while(str[index].isnumeric()):
        index += 1
    if(str[index == ')']):
        match(")")
    else:
        DeclareError()
    # match(")")


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


# Main
index = 0
error_state = False
# ip_string = input("Please input the string to be parsed: ")


# # Testing
# exp(ip_string)
# CheckSyntax()  # No syntax errors detected

# # Debuggging
# print(f"The parser cursor arrived at {index}!")
# print("\nTokens traversed: ")
# for i in range(index):
#     print(ip_string[i])
