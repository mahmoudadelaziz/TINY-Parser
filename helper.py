# Some helper functions
import re

cursor = 0  # global cursor (points to the current token)
error_state = False


def DeclareError(errorMessage):
    global error_state
    error_state = True
    print(errorMessage)


def CheckSyntax():
    global error_state
    if(error_state == True):
        print("SYNTAX ERROR!")
    else:
        print("ALL GOOD!")


def Match(expectedToken):
    global cursor, token
    # note: token is the current tokens[index] the parser's global cursor is pointing at
    if(token == expectedToken):
        # consume and advance
        cursor += 1
    else:
        DeclareError()


def Factor():
    # factor --> (exp) | number | identifier
    global cursor, token
    if(re.search("^\\d+$", token)):
        # it is a constant number
        # this is an ultimate base case
        cursor += 1
    elif(token.isalpha()):
        # It is an identifier
        # this is another ultimate base case
        cursor += 1
    # TO BE CONTINUED


def ComparisonOp():
    # comparison-op --> < | =
    global cursor, token
    if(token == '<'):
        Match('<')
    elif(token == '>'):
        Match('>')
    else:
        DeclareError()


def AddOp():
    # add-op --> + | -
    global cursor, token
    if(token == '+'):
        Match('+')
    elif(token == '-'):
        Match('-')
    else:
        DeclareError()


def MulOp():
    # add-op --> *
    global cursor, token
    if(token == '*'):
        Match('*')
    elif(token == '/'):
        Match('/')
    else:
        DeclareError()
