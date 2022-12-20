# Some helper functions
index = 0  # global cursor (points to the current token)
error_state = False


def DeclareError():
    global error_state
    error_state = True


def CheckSyntax():
    global error_state
    if(error_state == True):
        print("SYNTAX ERROR!")
    else:
        print("ALL GOOD!")


def Match(expectedToken):
    global index, token
    # note: token is the current tokens[index] the parser's global cursor is pointing at
    if(token == expectedToken):
        # consume and advance
        index += 1
    else:
        DeclareError()
