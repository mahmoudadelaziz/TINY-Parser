# Some helper functions
cursor = 0  # global cursor (points to the current token)
error_flag = False  # SyntaxError flag


def DeclareError():
    global error_flag
    error_flag = True


def CheckSyntax():
    global error_flag
    if(error_flag == True):
        print("SYNTAX ERROR!")
    else:
        print("ALL GOOD!")


def Match(expectedToken):
    global cursor, token, error_flag
    # note: token is the current tokens[index] the parser's global cursor is pointing at
    if(token == expectedToken):
        cursor += 1         # Keep moving forward!
    else:
        DeclareError()


def MulOp():
    # mul_op --> * | /
    if(token == '*'):
        Match('*')
    elif(token == '/'):
        Match('/')
    # else: DeclareError()


def AddOp():
    # add_op --> + | -
    if(token == '+'):
        Match('+')
    elif(token == '-'):
        Match('-')


def ComparisonOp():
    # comparison_op --> < | =
    if(token == '<'):
        Match('<')
    elif(token == '>'):
        Match('>')



def Factor():
    # factor --> (exp) | number | ID


def Term():
    # term --> factor [mul_op factor]


def SimpleExp():
    # simple_exp --> term [add_op term]


def Exp():
    # exp --> simple_exp [ComparisonOp simple_exp]


def WriteStmt():
    # write_stmt --> write identifier


def ReadStmt():
    # read_stmt --> read identifier


def IfStmt():
    # if_stmt --> if exp then stmt_seq [else stmt_seq] end


def RepeatStmt():
    # repeat_stmt --> repeat stmt_seq until exp


def AssignStmt():
    # assign_stmt --> identifier := exp


def Stmt():
    # statement --> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt


def StmtSequence():
    # stmt_seq --> statement {;statement}


def Program():
    # Program --> stmt_seq
