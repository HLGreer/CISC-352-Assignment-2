# Removes all spaces from the string and then places each character
# into an array of tokens, with multicharcacter operators (such as '->')
# being an individual token.
def shunting(sentence):
    stack, out, s = [], [], []
    precedence = {'!': 4, '^': 3, 'v': 2, '->': 1, '<->': 0}
    sentence = sentence.replace(' ', '')
    if(sentence[0] == '('):
        return sentence
    i = 0
    while(i < len(sentence)):
        if(sentence[i] != '-' and sentence[i] != '<'):
            s.append(sentence[i])
            i += 1
        elif(sentence[i] == '-'):
            s.append('->')
            i += 2
        elif(sentence[i] == '<'):
            s.append('<->')
            i += 3
    for token in s :
        if(token not in precedence):
            out.append(token)
        else:
            while(stack and precedence[token] < precedence[stack[0]]):
                out.append(stack.pop(0))
            stack.insert(0, token)    
    while(stack):
        out.append(stack.pop(0))
    return out

# Takes a postfix array of characters and outputs an infix sentence with brackets
# to denote the precedences
def infix(str):
    stack, out, ops = [], [], ['!', '^', 'v', '->', '<->']
    for token in str:
        if(token not in ops):
            stack.append(token)
        else:
            if(token == '!'):
                unit = token + stack.pop()
            else:
                unit = '(' + stack.pop(-2) + token + stack.pop() + ')'
            stack.append(unit)
    s = stack[0]
    return s

# Adds precedence brackets to an infix sentence
def bracket():
    filename = 'cnf.txt'
    with open(filename) as f:
        sentence = f.readlines()
    sentence = sentence[0].strip()
    str = shunting(sentence)
    if(str[0] != '('):
        s = infix(str)
        return s
    else:
        return str

print(bracket())