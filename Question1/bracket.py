
# Removes all spaces from the string and then places each character
# into an array of tokens, with multicharcacter operators (such as '->')
# being an individual token.
def shunting(sentence):
    i = 0
    stack, out, s = [], [], []
    precedence = {'!': 4, '^': 3, 'v': 2, '->': 1, '<->': 0}
    sentence = sentence.replace(' ', '')
    newSentence = ""
    if(sentence[0] == '('):
        return sentence
    while(i < len(sentence)):
        if(sentence[i] not in precedence and sentence[i] not in {'<', '-'}):
            newSentence += sentence[i]
            i += 1
        elif(sentence[i] == '-'):
            newSentence += ' '
            newSentence += '->'
            i += 2
            newSentence += ' '
        elif(sentence[i] == '<'):
            newSentence += ' '
            newSentence += '<->'
            i += 3
            newSentence += ' '
        elif(sentence[i] in precedence):
            newSentence += ' '
            newSentence += sentence[i]
            i +=1
            newSentence += ' '
    s = newSentence.split()
    for token in s :
        if(token not in precedence):
            out.append(token)
        else:
            while(stack and precedence[token] <= precedence[stack[0]]):
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
                unit = '(' + stack.pop(-2) + token + stack.pop(-1) + ')'
            stack.append(unit)
        print(stack)
    s = stack[0]
    s = s[1:-1]
    return s

# Adds precedence brackets to an infix sentence
def bracket():
    filename = 'cnf.txt'
    with open(filename) as f:
        sentence = f.readlines()
    sentence = sentence[0].strip()
    str = shunting(sentence)
    print(str)
    if(str[0] != '('):
        print(str)
        s = infix(str)
        return s
    else:
        return str

print(bracket())
