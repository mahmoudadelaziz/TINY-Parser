# matching function
index = 0

def match(str):
    global index
    if(token[index] == str):
        #consume and advance
        index = index + 1
    else:
        #error
        print("SYNTAX ERROR!")

def fact(str):
    global index
    match("(")
    if(str[index].isnumeric()):
        index = index + 1
    else:
        print("SYNTAX ERROR!")
    match(")")

token = "(5)"
fact(token)
print(index)