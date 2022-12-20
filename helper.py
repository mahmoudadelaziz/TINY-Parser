import re

# Some helper functions
cursor = 0  # global cursor (points to the current token)
error_flag = False  # SyntaxError flag
no_errors = 0  # Number of errors detected


def DeclareError():
    global error_flag, no_errors
    error_flag = True
    no_errors += 1

    # Where was the cursor?
    print(f"Error at cursor = {cursor}")


def CheckSyntax():
    global error_flag
    if(error_flag == True):
        print("SYNTAX ERROR(S) DETECTED!\n")
    else:
        print("ALL GOOD!\n")


def Match(expectedToken):
    global cursor
    # note: token is the current tokens[index] the parser's global cursor is pointing at
    if(tokens[cursor][1] == expectedToken):
        cursor += 1         # Keep moving forward!
    elif(tokens[cursor][0] == expectedToken):
        cursor += 1
    else:
        DeclareError()


def MulOp():
    # mul_op --> * | /
    if(tokens[cursor][0] == '*'):
        Match('MULT')
    elif(tokens[cursor][0] == '/'):
        Match('DIV')
    else:
        print("Failed to match Mul-Operator!")


def AddOp():
    # add_op --> + | -
    if(tokens[cursor][0] == '+'):
        Match('PLUS')
    elif(tokens[cursor][0] == '-'):
        Match('MINUS')
    else:
        print("Failed to match Add-Operator!")


def ComparisonOp():
    # comparison_op --> < | =
    if(tokens[cursor][0] == '<'):
        Match('LESSTHAN')
    elif(tokens[cursor][0] == '='):
        Match('EQUAL')
    else:
        print("Failed to match Comp-Operator!")


def Factor():
    # factor --> (exp) | number | ID
    # QUESTION! What can we do about balancing parenthesis? Did our scanner already handle that?
    # For now, I shall assume that (exp) is simply equivalent to exp
    if(re.search("^\\d+$", tokens[cursor][0])):
        Match("NUMBER")
    elif(re.search("^[a-zA-Z]", tokens[cursor][0])):
        Match("IDENTIFIER")  # if identifier, match and move on
    elif(tokens[cursor][0] == '('):
        Match('OPENBRACKET')
        Exp()
        Match('CLOSEDBRACKET')
    # else:
    #     DeclareError()
    #     print(f"Failed to match Factor at index {cursor}: {tokens[cursor]}")


def Term():
    # term --> factor [mul_op factor]
    # Match(Factor) #?
    Factor()
    if((tokens[cursor][0] == '*') | (tokens[cursor][0] == '/')):
        MulOp()
        Factor()


def SimpleExp():
    # simple_exp --> term [add_op term]
    Term()
    if((tokens[cursor][0] == '+') | (tokens[cursor][0] == '-')):
        AddOp()
        Term()


def Exp():
    # exp --> simple_exp [ComparisonOp simple_exp]
    SimpleExp()
    if((tokens[cursor][0] == '<') | (tokens[cursor][0] == '=')):
        ComparisonOp()
        SimpleExp()


def WriteStmt():
    # write_stmt --> write exp
    print("!----------HOORAH!----------")
    Match("WRITE")
    Exp()


def ReadStmt():
    # read_stmt --> read identifier
    Match("READ")
    Match("IDENTIFIER")  # Identifier's string value


def IfStmt():
    # if_stmt --> if exp then stmt_seq [else stmt_seq] end
    Match("IF")
    Exp()
    Match("THEN")
    StmtSequence()
    if(tokens[cursor][0] == "else"):
        StmtSequence()
    Match("END")


def RepeatStmt():
    # repeat_stmt --> repeat stmt_seq until exp
    Match("REPEAT")
    StmtSequence()
    Match("UNTIL")
    Exp()
    if(cursor < (len(tokens) - 1)):
        # Ad-hoc solution to the problem (Check later if error)
        Match("SEMICOLON")


def AssignStmt():
    # assign_stmt --> identifier := exp
    if(tokens[cursor][1] == "IDENTIFIER"):
        Match("IDENTIFIER")
        Match("ASSIGN")
        Exp()


def Stmt():
    # statement --> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
    if((tokens[cursor][1] == "IDENTIFIER") & (tokens[cursor+1][1] == "ASSIGN")):
        print(f"At #{cursor} HEY ASSIGN!")
        AssignStmt()
    elif(tokens[cursor][1] == "IF"):
        print(f"At #{cursor} HEY IF!")
        IfStmt()
    elif(tokens[cursor][1] == "REPEAT"):
        print(f"At #{cursor} HEY REPEAT!")
        RepeatStmt()
    elif(tokens[cursor][1] == "READ"):
        print(f"At #{cursor} HEY READ!")
        ReadStmt()
    elif(tokens[cursor][1] == "WRITE"):
        # THE PROBLEM NOW: THE CODE DOES NOT ENTER THIS CONDITION BODY
        print(f"At #{cursor} HEY WRITE!")
        WriteStmt()
    else:
        print(f"Stmt() FAILED at cursor #{cursor}")


def StmtSequence():
    # stmt_seq --> statement {; statement}
    Stmt()
    #print("STATEMENT PRINTED!")
    if(tokens[cursor][1] == "SEMICOLON"):  # The problem here?! YES, Most likely
        Match("SEMICOLON")
        Stmt()
        print(f"STATEMENT SEQUENCE MATCH ENDED AT #{cursor}!")  # Debugging
    else:
        # THE PROBLEM IS HERE IN THIS FUNCTION
        print(f"StmtSequence() Failed at cursor #{cursor}")


def Program():
    # Program --> stmt_seq
    StmtSequence()


if __name__ == "__main__":

    # Taking input
    # print("Please Enter the name of the tokens list file (with extension, like tokens.txt): ")
    # input_name = input()
    input_name = "input.txt"
    Source_Code = open(input_name, 'r')
    # Read the file line by line (and insert each line in the list)
    Lines = Source_Code.readlines()
    # Now we have a list of lines (as strings), we can close the file
    Source_Code.close()
    # organizing tokens as a long list of lists [[stringValue, type], [stringValue1, type1], etc.]
    tokens = [line.split(r',') for line in Lines]
    # cleaning up the tokens list (of spaces and new line chars, etc.)
    tokens = [[item[0].strip(), item[1].strip()] for item in tokens]

    # Testing
    print("**" * 75)
    Program()
    CheckSyntax()

    # Debugging
    print(f"Number of tokens = {len(tokens)}")
    #print(f"All tokens:\n{tokens}\n")
    print(f"Cursor arrived at: {cursor}")
    print(f"Number of errors detected = {no_errors}")
    print(f"Current token: {tokens[cursor]}")

    # print("--" * 40)
    # print("Tokens matched successfully:")
    # for i in range(cursor):
    #     print(f"{i}: {tokens[i]}")

    outFile = open("TokensMatched.txt", "w")
    for i in range(cursor):
        outFile.write(f"{tokens[i][0]}, {tokens[i][1]}\n")
    outFile.close()

    print("**" * 75)
