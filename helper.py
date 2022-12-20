import re

# Some helper functions
cursor = 0  # global cursor (points to the current token)
error_flag = False  # SyntaxError flag


def DeclareError():
    global error_flag
    error_flag = True


def CheckSyntax():
    global error_flag
    if(error_flag == True):
        print("SYNTAX ERROR!\n")
    else:
        print("ALL GOOD!\n")


def Match(expectedToken):
    global cursor, tokens
    # note: token is the current tokens[index] the parser's global cursor is pointing at
    if(tokens[cursor][0] == expectedToken):
        cursor += 1         # Keep moving forward!
    else:
        DeclareError()


def MulOp():
    # mul_op --> * | /
    if(tokens[cursor][0] == '*'):
        Match('*')
    elif(tokens[cursor][0] == '/'):
        Match('/')
    # else: DeclareError()


def AddOp():
    # add_op --> + | -
    if(tokens[cursor][0] == '+'):
        Match('+')
    elif(tokens[cursor][0] == '-'):
        Match('-')


def ComparisonOp():
    # comparison_op --> < | =
    if(tokens[cursor][0] == '<'):
        Match('<')
    elif(tokens[cursor][0] == '>'):
        Match('>')


def Factor():
    # factor --> (exp) | number | ID
    # QUESTION! What can we do about balancing parenthesis? Did our scanner already handle that?
    # For now, I shall assume that (exp) is simply equivalent to exp
    if(re.search("^\\d+$", tokens[cursor][0])):
        Match(tokens[cursor][0])
    elif(re.search("^[a-zA-Z]", tokens[cursor][0])):
        Match(tokens[cursor][0])  # if identifier, match and move on
    elif(tokens[cursor][0] == '('):
        Match('(')
        Exp()  # ?
        Match(')')
    else:
        DeclareError()


def Term():
    # term --> factor [mul_op factor]
    Match(Factor)
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
    if((tokens[cursor][0] == '<') | (tokens[cursor][0] == '>')):
        ComparisonOp()
        SimpleExp()


def WriteStmt():
    # write_stmt --> write identifier
    Match("write")
    Match(tokens[cursor][0])  # Identifier's string value


def ReadStmt():
    # read_stmt --> read identifier
    Match("read")
    Match(tokens[cursor][0])  # Identifier's string value


def IfStmt():
    # if_stmt --> if exp then stmt_seq [else stmt_seq] end
    Match("if")
    Exp()
    Match("then")
    StmtSequence()
    if(tokens[cursor][0] == "else"):
        StmtSequence()
    Match("end")


def RepeatStmt():
    # repeat_stmt --> repeat stmt_seq until exp
    Match("repeat")
    StmtSequence()
    Match("until")
    Exp()


def AssignStmt():
    # assign_stmt --> identifier := exp
    if(re.search("^[a-zA-Z]", tokens[cursor][0])):
        Match(tokens[cursor][0])
        Match(":=")
        Exp()
    else:
        DeclareError()


def Stmt():
    # statement --> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
    if(tokens[cursor][0] == "if"):
        IfStmt()
    if(tokens[cursor][0] == "repeat"):
        RepeatStmt()
    if(re.search("^[a-zA-Z]", tokens[cursor][0])):
        AssignStmt()
    if(tokens[cursor][0] == "read"):
        ReadStmt()
    if(tokens[cursor][0] == "write"):
        WriteStmt()


def StmtSequence():
    # stmt_seq --> statement {;statement}
    Stmt()
    if(tokens[cursor][0] == ';'):
        Match(';')
        Stmt()


def Program():
    # Program --> stmt_seq
    StmtSequence()


if __name__ == "__main__":

    # Taking input
    print("Please Enter the name of the tokens list file (with extension, like tokens.txt): ")
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
    Program()
    CheckSyntax()

    # Debugging
    print(f"Number of tokens = {len(tokens)}\n")

    #print(f"All tokens:\n{tokens}\n")

    print(f"Cursor arrived at: {cursor}\n")

    print(f"Current token: {tokens[cursor]}\n")

    print("Tokens matched successfully:")
    for i in range(cursor):
        print(f"{i}: {tokens[i]}")
