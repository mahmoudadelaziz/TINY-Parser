# This script contains some helper functions and definitions
# for our Parser code

# Imports
import re

# Global Variables
cursor = 0  # global cursor (points to the current token)
error_flag = False  # SyntaxError flag
error_message = ""

# Functions


def DeclareError(Cause):
    global error_flag, error_message
    error_flag = True
    error_message = f"{Cause} on line #{cursor + 1}"
    # Where was the cursor?
    print(f"SYNTAX ERROR on line #{cursor + 1}")  # Debugging


def Match(expectedToken):
    global cursor
    # note: token is the current tokens[index] the parser's global cursor is pointing at
    if((cursor < (len(tokens)-1))):  # index safeguard (Debugging)
        if(tokens[cursor][1] == expectedToken):
            cursor += 1         # Keep moving forward!
        elif(tokens[cursor][0] == expectedToken):
            cursor += 1
        else:
            DeclareError(f"Expected {expectedToken} ")


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
    if(tokens[cursor][1] == "NUMBER"):
        Match("NUMBER")
    elif(re.search("^[a-zA-Z]", tokens[cursor][0])):
        Match("IDENTIFIER")  # if identifier, match and move on
    elif(tokens[cursor][0] == '('):
        Match('OPENBRACKET')
        Exp()
        Match('CLOSEDBRACKET')
    else:
        DeclareError("Mismatched Factor ")
        print(f"Expected a factor ")


def Term():
    # term --> factor [mul_op factor]
    Factor()
    if((cursor < (len(tokens)-1))):  # index safeguard (Debugging)
        if((tokens[cursor][0] == '*') | (tokens[cursor][0] == '/')):
            MulOp()
            Factor()


def SimpleExp():
    # simple_exp --> term [add_op term]
    Term()
    if((cursor < (len(tokens)-1))):  # index safeguard (Debugging)
        if((tokens[cursor][0] == '+') | (tokens[cursor][0] == '-')):
            AddOp()
            Term()


def Exp():
    # exp --> simple_exp [ComparisonOp simple_exp]
    SimpleExp()
    if((cursor < (len(tokens)-1))):  # index safeguard (Debugging)
        if((tokens[cursor][0] == '<') | (tokens[cursor][0] == '=')):
            ComparisonOp()
            SimpleExp()


def WriteStmt():
    # write_stmt --> write exp
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
    StmtSequence()


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
    Match("IDENTIFIER")
    Match("ASSIGN")
    Exp()


def Stmt():
    # statement --> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
    if((cursor < (len(tokens)-1))):  # index safeguard (Debugging)
        if((tokens[cursor][1] == "IDENTIFIER") & (tokens[cursor+1][1] == "ASSIGN")):
            AssignStmt()
        elif(tokens[cursor][1] == "IF"):
            IfStmt()
        elif(tokens[cursor][1] == "REPEAT"):
            RepeatStmt()
        elif(tokens[cursor][1] == "READ"):
            ReadStmt()
        elif(tokens[cursor][1] == "WRITE"):
            # THE PROBLEM NOW: THE CODE DOES NOT ENTER THIS CONDITION BODY
            WriteStmt()
        else:
            print(f"Stmt() FAILED at cursor #{cursor}")


def StmtSequence():
    # stmt_seq --> statement {; statement}
    Stmt()
    #print("STATEMENT PRINTED!")
    if((cursor < (len(tokens)-1))):  # index safeguard (Debugging)
        if(tokens[cursor][1] == "SEMICOLON"):  # The problem here?! YES, Most likely
            Match("SEMICOLON")
            Stmt()
        elif(tokens[cursor][1] == "END"):
            Match("END")
        else:
            # THE PROBLEM IS HERE IN THIS FUNCTION
            # OR MISSING A SEMICOLON ;
            DeclareError("Semicolon missing ")
            # print(f"Semicolon missing at cursor #{cursor}")


def Program():
    # Program --> stmt_seq
    StmtSequence()


def Parse(LinesEntered):
    global tokens
    tokens = LinesEntered
    if(len(tokens) == 0):
        return "Nothing was entered!"
    elif(len(tokens) == 1):
        return "The TINY program should have at least two tokens!"
    else:
        Program()
        if(error_flag == False):
            # cursor = 0  # Reset for reuse
            # tokens = []  # Reset for reuse
            print(f"[For Parser() in helper]Cursor's final value: {cursor}")
            return "ALL GOOD!"
        else:
            return error_message


def GetPlainTextFromFile(FileName):
    # Read text from a file
    # Arg: File Name
    # Return: string containg the text read
    TokenText = open(FileName, 'r')
    Txt = TokenText.read()
    TokenText.close()
    return Txt


def GetTokensListFromPlainText(ourTokenText):
    global tokens
    # Get a list of lines (tokens list) from a plainText input string
    # Arg: PlainText string
    # Return: list of lists of strings: [[tval, ttype], [tval, ttype], [tval, ttype], ...]
    tokens = ourTokenText.splitlines()
    tokens = [item.split(r',') for item in tokens]
    tokens = [[item[0].strip(), item[1].strip()] for item in tokens]
    return tokens