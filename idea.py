def Program(tokens):
    # program --> stmt-sequence
    if (len(tokens) > 1):
        if (tokens[-1][0] == ';'):
            print("SyntaxError: The last statement ends with a semicolon!")
            return False  # ?

        return stmt_seq(tokens)

    else:
        print("Nothing to Parse! The minimum number of tokens was not met.")
        return False  # ?


def stmt_seq(token):
    # stmt-sequence --> stmt-sequence ; statement | statement
    if statement(token):
        if token[0].value is ";":
            token.remove(token[0])
            return statement(token)
    else:
        return False


def statement(token):
    # statement --> if- stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
    if if_stmt(token):
        return True
    elif repeat_stmt(token):
        return True
    elif assign_stmt(token):
        return True
    elif read_stmt(token):
        return True
    elif write_stmt(token):
        return True
    else:
        return False


def if_stmt(token):
    if token[0].value == "IF":
        token.remove(token[0])
        exp(token)
        if token[0].value == "THEN":
            token.remove(token[0])
            stmt_seq(token)
            if token[0].value is "END":
                token.remove(token[0])
                return True
            elif token[0].value is "ELSE":
                token.remove(token[0])
                stmt_seq(token)
                if token[0].value is "END":
                    token.remove(token[0])
                    return True
                else:
                    return False
        else:
            return False
    else:
        return False


def repeat_stmt(l):
    if l[0].value is not "REPEAT":
        return False
    else:
        l.remove(l[0])
        return True


def assign_stmt(l):
    if l[0].type == 'var' and len(l) > 1:
        if l[1].value == ":=":
            l.remove(l[0])
            l.remove(l[1])
            # return exp(l)
            return True

        return False


def read_stmt(l):
    if l[0].value == 'READ' and len(l) > 1:
        if l[1].type is "var":
            l.remove(l[0])
            l.remove(l[1])
            return True
        else:
            print("ERROR is in read in line " + str(l[0].line_no))
            return False

    else:
        return False


def write_stmt(l):
    if l[0].value == "WRITE":
        l.remove(l[0])
        # return exp(l)
        return True
    return False


def exp(l):
    # for wa7da in list(tokens.queue):
    #     print(wa7da.value, ", ", wa7da.type, "  in line ", wa7da.line_no)
    # print("________")
    if simple_exp(l):
        if comparison_op(l) and simple_exp(l):
            return True
    return False


def comparison_op(l):
    print("compaaaaare "+l[0].value)
    if l[0].value is "<" or l[0].value is ">" or l[0].value is "=":
        l.remove(l[0])
        return True
    else:
        print("ERROR is in comparison in line " + str(l[0].line_no))
        return False


def simple_exp(l):
    if l[0].value is "+" or l[0].value is "-":
        return term(1)
        return True #?
    else:
        return False

def add_op(l):
    if l[0].value is "+" or l[0].value is "-":
        l.remove(l[0])
        return True
    else:
        print("ERROR is in add in line "+str(l[0].line_no))
        return False


def term(l):
    if l[0].value is "*" or l[0].value is "/":
        mul_op(1)
        return True
    return factor(l)
    # if factor(l):
    #     if mul_op(l):
    #         return factor(l)
    #     return True
    # else:
    #     return False


def mul_op(l):
    if l[0].value is "*" or l[0].value is "/":
        l.remove(l[0])
        return True
    else:
        print("ERROR is in mul in line "+str(l[0].line_no))
        return False


def factor(l):
    print(l[0].value)
    if l[0].value == "(":
        l.remove(l[0])
        exp(l)
        if l[0].value == ")":
            l.remove(l[0])
            return True

    elif l[0].type == "num":
        l.remove(l[0])
        return True
    elif l[0].type == "var":
        l.remove(l[0])
        return True
    else:
        print("ERROr is in factor in line "+str(l[0].line_no))
        return False


# #####main
# tokens = scanner3.tagheez("res.txt").tokenz
# for wa7da in tokens:
#     print(wa7da.value, ", ", wa7da.type, "  in line ", wa7da.line_no)

# print(program(tokens))
