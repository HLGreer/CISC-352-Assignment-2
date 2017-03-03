
def removeWhitespace(sentence):
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



def groupByOperatorPrecedence(str):
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
    s = stack[0]
    if s[0] == "(" and s[-1] == ")":
        s = s[1:-1]
    return s

# Adds precedence brackets to an infix sentence


def initiate(filename):
    with open(filename) as f:
        sentence = f.readlines()
    sentence = sentence[0].strip()
    str = removeWhitespace(sentence)
    if(str[0] != '('):
        s = groupByOperatorPrecedence(str)
        return s
    else:
        return str

# can't assume that no double negation

# order of precedence greatest to least: ! , ^ , v , -> , <->

# Any wff can be converted to CNF by using the following equivalences:
# 1. A <-> B = (A->B) ^ (B->A)
# 2. A -> B = !A v B
# 3. !(A ^ B) = !A v !B
# 4. !A v B) = !A ^ !B
# 5. !!A = A
# 6. A v (B ^ C) = (A v B) ^ (A v C)

# # returns first index of occurrences of non-overlapping substrings in  string
# def findAllSubstrings(string, substring):
#   index = 0
#   substringFirstIndices = []
#   while True:
#     index = string.find(substring, index)
#     if index == -1: #no substring
#       return substringFirstIndices
#     else:
#       substringFirstIndices += [index]
# index += len(substring) # since we're not searching for overlapping
# occurrences


def findRightmostClause(string):
    length = len(string)

    # if rightmost element is a close bracket, return the bracketed term
    if string(length - 1) == ")":
        countBrackets = 1

        for i in range(length - 2, -1, -1):
            if string[i] == "(":
                countBrackets -= 1
                if countBrackets == 0:
                    # we have found the open bracket corresponding to the last
                    # close bracket
                    clauseStartIndex = i
                    return string[clauseStartIndex: length]
            if string[i] == ")":
                # there are nested brackets
                countBrackets += 1

        # should have returned in loop above, otherwise error
        print("***ERROR in findRightmostClause function")

    # else, return the entire string as a clause
    else:
        return string


def findLeftmostClause(string):
    length = len(string)

    # if rightmost element is a close bracket, return the bracketed term
    if string(0) == "(":
        countBrackets = 1

        for i in range(length):
            if string[i] == ")":
                countBrackets -= 1
                if countBrackets == 0:
                    # we have found the close bracket corresponding to the
                    # first open bracket
                    clauseEndIndex = i
                    return string[0: clauseEndIndex + 1]
            if string[i] == "(":
                # there are nested brackets
                countBrackets += 1

        # should have returned in loop above, otherwise error
        print("***ERROR in findLeftmostClause function")
    # else, return the entire string as a clause
    else:
        return string

# if index is in a bracketed clause, return the clause (it may be part of a larger expression)
# else, return None


def checkIfSurroundedByBrackets(string, index):
    length = len(string)

    clauseStartIndex = None
    clauseEndIndex = None

    # check for open bracket left of index
    countCloseBrackets = 0
    for i in range(index - 1, -1, -1):
        if string[i] == ")":
            countCloseBrackets += 1  # checking for nested brackets
        if string[i] == "(":
            countCloseBrackets -= 1
            if countCloseBrackets < 0:
                clauseStartIndex = i
                break

    # check for close bracket right of index
    countOpenBrackets = 0
    for i in range(index + 1, length):
        if string[i] == "(":
            countOpenBrackets += 1  # checking for nested brackets
        if string[i] == ")":
            countOpenBrackets -= 1
            if countOpenBrackets < 0:
                clauseEndIndex = i
                break

    if clauseStartIndex != None and clauseEndIndex != None:
        return [clauseStartIndex, clauseEndIndex]
    elif clauseStartIndex == None and clauseEndIndex == None:
        return None
    else:
        print("***ERROR in checkIfSurroundedByBrackets")
        return


# rule: A <-> B = (A->B) ^ (B->A)
def iffRule(input):
    # for i in range(numIffOccurrences): # do the iffRule for each "<->" found
    while (input.count("<->") > 0):
        # check if "<->" is in its own bracket set (in a clause)
        operatorIndex = input.find("<->")

        operatorInClause = checkIfSurroundedByBrackets(input, operatorIndex)

        if operatorInClause == None:  # if not in brackets:
            # print("iff is not surrounded by brackets")
            A = input[0: operatorIndex]
            # since "<->" is 3 chars long
            B = input[operatorIndex + 3: len(input)]
            input = "(" + A + "->" + B + ")^(" + B + "->" + A + ")"

        else:  # iff in brackets; apply rule to just that clause
            # print("iff is in clause")
            # clause includes brackets
            clauseStartIndex = operatorInClause[0]
            clauseEndIndex = operatorInClause[1]
            leftOfClause = input[0: clauseStartIndex]
            rightOfClause = input[clauseEndIndex + 1: len(input)]
            # don't include bracket
            A = input[clauseStartIndex + 1: operatorIndex]
            # since "<->" is 3 chars long # don't include bracket
            B = input[operatorIndex + 3: clauseEndIndex]

            # print ("leftOfClause = " + leftOfClause)
            # print ("rightOfClause = " + rightOfClause)
            # print("A = " + A)
            # print("B = " + B)

            input = leftOfClause + \
                "((" + A + "->" + B + ")^(" + B + "->" + A + "))" + rightOfClause

    return input


def implicationRule(input):

    # for i in range(numIffOccurrences): # do the iffRule for each "<->" found
    while (input.count("->") > 0):
        # check if "<->" is in its own bracket set (in a clause)
        operatorIndex = input.find("->")

        operatorInClause = checkIfSurroundedByBrackets(input, operatorIndex)

        if operatorInClause == None:  # if not in brackets:
            # print("implication is not surrounded by brackets")
            A = input[0: operatorIndex]
            
            # since "<->" is 3 chars long
            B = input[operatorIndex + 2: len(input)]
            input = "!(" + A + ")v(" + B + ")"

        else:  # iff in brackets; apply rule to just that clause
            # print("implication is in clause")
            # clause includes brackets
            clauseStartIndex = operatorInClause[0]
            clauseEndIndex = operatorInClause[1]
            leftOfClause = input[0: clauseStartIndex]
            rightOfClause = input[clauseEndIndex + 1: len(input)]
            # don't include bracket
            A = input[clauseStartIndex + 1: operatorIndex]
            # since "<->" is 3 chars long # don't include bracket
            B = input[operatorIndex + 2: clauseEndIndex]

            # print ("leftOfClause = " + leftOfClause)
            # print ("rightOfClause = " + rightOfClause)
            #print("A = " + A)
            #print("B = " + B)

            input = leftOfClause + "(!(" + A + ")v(" + B + "))" + rightOfClause

    return input


def propagateNot(input):
    # while there are still nots needing to be propagated
    while (input.count("!(") > 0):
        # setup a counter for brackets
        count = 0
        # get the location of the first one
        location = input.find("!(")

        # remove the not before the bracket, keep the bracket
        input = input[0:location] + input[location + 1] + \
            input[location + 2:len(input)]

        # loop through the open bracket, starting at the location of !(
        for i in range(location, len(input)):
            # if we open more brackets, add to the count
            if input[i] == "(":
                count += 1

            # if we close a bracket, remove from the count
            elif input[i] == ")":
                count -= 1

                # if we have no more brackets we are done with this iteration
                # store the end location so we know how far to add negations
                if count == 0:
                    endLocation = i
                    # make the input equal to:
                    # the start to the first !( +
                    # add "!" to the first bracket section +
                    # add the end (which may contain more !(, dealt with in
                    # following iterations of while loop
                    input = input[0:location] + addNot(input[location:endLocation + 1]) + input[
                        endLocation + 1:len(input)]
                    # break the loop and go back to the while loop
                    break

            # If there is an ^, change it to v
            elif input[i] == "^":
                input = input[0] + input[1:i] + "v" + input[i + 1:len(input)]

            # If there is an v, change it to ^
            elif input[i] == "v":
                input = input[0] + input[1:i] + "^" + input[i + 1:len(input)]

    return input


def addNot(input):
    # create a list for storing atoms
    notList = []
    #this will be used to store the letters of each word
    word = ""
    # loop through the sequence provided (in between brackets)
    for i in range(len(input)):
        # If the character is not a symbol, add it to our list
        #if input[i] != "(" and input[i] != ")" and input[i] != "^" and input[i] != "v" and input[i] != "!":
        #If we have and or or, or we are at the end of the expression, add the word we built
        if input[i] == "v" or input[i] == "^" or i == (len(input)-1):
            #print("added: " + word)
            notList.append(word)
            word=""
        #It is a letter or atom, store it in the word
        elif input[i] != "(" and input[i] != ")" and input[i] != "!":
                word += input[i]
                
    #print(notList)

    # loop through the atoms in our list that need an ! added
    for i in range(len(notList)):
        # replace the atom with !atom (A into !A)
        input = input.replace(notList[i], "!" + notList[i])
    # return
    return input


def doubleNegationRule(input):
    input = input.replace("!!", "")
    return input



def distributeOrRule(input):
  
  while(input.count("v") > 0):
    i = 0
    for character in input:
      if character == 'v':
        operatorIndex = i
        operatorInClause = checkIfSurroundedByBrackets(input, operatorIndex)
        #print(operatorIndex)
        if operatorInClause == None: #if not in brackets:
          A = input[0 : operatorIndex]
          B = input[operatorIndex + 1 : len(input)]
          if input[operatorIndex - 1] == ')' and input[operatorIndex + 1] == '(':
            A = convertToCNF(A)
            B = convertToCNF(B)
            A = A[1 : -1]
            B = B[1:-1]
            #print(A)
            #print(B)
            if (A.count("^") == 0 and B.count("^") == 0):
              output = "(" + A + "v" + B + ")"
            elif (A.count("^") == 0 and B.count("^") > 0):
              output = ""
              while(B.count("^") > 0):
                output = output + "(" + A + "v" + B[0:B.find("^")] + ")" + "^"
                B = B[(B.find("^"))+1:]
              output = output + "(" + A + "v" + B + ")"
            elif (A.count("^") > 0 and B.count("^") == 0):
              output = ""
              while(A.count("^") > 0):
                output = output + "(" + A[A.find("^")-1] + "v" + B + ")" + "^"
                A = A[(A.find("^"))+1:]
              output = output + "(" + A + "v" + B + ")"
            elif (A.count("^") > 0 and B.count("^") > 0):
              output = ""
              while(A.count("^") > 0):
                temp = B
                while(temp.count("^") > 0):
                  output = output + "(" + A[0:A.find("^")] + "v" + temp[0:temp.find("^")] + ")" + "^"
                  temp = temp[(temp.find("^"))+1:]
                output = output + "(" + A[0:A.find("^")] + "v" + temp + ")" + "^"
                A = A[(A.find("^"))+1:] #A reaches one last
              #output = output + "^"
              while(B.count("^") > 0):
                output = output + "(" + A + "v" + B[0:B.find("^")] + ")" + "^"
                B = B[(B.find("^"))+1:]
              output = output + "(" + A + "v" + B + ")" 
            return output
          elif input[operatorIndex - 1] == ')' and input[operatorIndex + 1] != '(':
            A = A[1 : -1]
            A = convertToCNF(A)
            output = ""
            while (A.count("^") > 0):
              operatorIndex2 = A.find("^")
              output = output + "(" + A[0:operatorIndex2] + "v" + B + ")" + "^"
              A = A[operatorIndex2 + 1: len(A)]
            output = output + "(" + A + "v" + B + ")"
            return output
          elif input[operatorIndex - 1] != ')' and input[operatorIndex + 1] == '(':
            B = B[1 : -1]
            #print(B)
            B = convertToCNF(B)
            #print(B)
            output = ""
            while (B.count("^") > 0):
              operatorIndex2 = B.find("^")
              output = output + "(" + A + "v" + B[0:operatorIndex2] +  ")" + "^"
              B = B[operatorIndex2 + 1: len(B)]
            output = output + "(" + A + "v" + B + ")"
            return output
          else:
            i = i + 1
            continue
        else:
          #input = input[1:-1]
          i = i + 1
          continue
      else:
        i = i + 1
        continue

  return input


def andResolution(input):
    i = 0
    for character in input:
      if character == '^':
        operatorIndex = i
        operatorInClause = checkIfSurroundedByBrackets(input, operatorIndex)
        #print(operatorIndex)
        if operatorInClause == None: #if not in brackets:
            A = input[0 : operatorIndex]
            B = input[operatorIndex + 1 : len(input)]
            if input[operatorIndex - 1] == ')' and input[operatorIndex + 1] == '(':
                #print(A)
                #print(B)
                A = A[1 : -1]
                B = B[1:-1]
                A = convertToCNF(A)
                B = convertToCNF(B)
                #print(A)
                #print(B)
                output = A + "^" + B 

            elif input[operatorIndex - 1] == ')' and input[operatorIndex + 1] != '(':
                A = A[1 : -1]
                A = convertToCNF(A)
                
                output  = "(" + A + ")" + "^" + B

            elif input[operatorIndex - 1] != ')' and input[operatorIndex + 1] == '(':
                B = B[1 : -1]
                B = convertToCNF(B)
                
                output =  A + "^" + "(" + B + ")"

            else:
                i = i + 1
            continue
        else:
          #input = input[1:-1]
          i = i + 1
          continue
      else:
        i = i + 1
        continue
    return output


# converts to clause form
def convertToClause(cnf):
    # flag
    opened = False
    # initial {
    output = "{"
    # loop through the expression
    for i in range(len(cnf)):
        # if it isnt v or ^, check for brackets or add atom
        if cnf[i] != "v" and cnf[i] != "^":
            # if it is an open bracket, check if we should include it
            if cnf[i] == "(":
                # check if we already opened a bracket or if the next element is a bracket
                if opened or cnf[i + 1] == "(":
                    # skip this one, we dont want 2
                    pass
                # Checks if the expression is in the form: (A), skips bracket
                else:
                    #loop through from i to end, checking if there are any other expressions in the ()
                    #for j in range(i,len(cnf)):
                        #if there is another expression we can add brackets
                     #   if cnf[j] == "v" and opened == False:
                      #      output += "("
                       #     opened = True
                        #no other expressions, remove brackets
                        #elif cnf[j] == ")":
                         #   pass
                    output += "("
                    opened = True

            # Check for closed brackets
            elif cnf[i] == ")":
                # If we opened a bracket and we are at the end, or at an ^ add
                # it
                if opened and (i == len(cnf) - 1 or cnf[i + 1] == "^"):
                    output += ")"
                # otherwise we dont want it
                else:
                    pass
            # Adds the atoms
            else:
                output += cnf[i]
        # it is v make it a comma but dont change flags as we are inside the
        # brackets
        elif cnf[i] == "v":
            output += ","
        # it is an ^, we can add a comma and reset brackets
        else:
            output += ","
            opened = False
    # add last } and return
    output += "}"

    return output

            
def convertToCNF(input):
    while(input[0] == "(" and input[-1] == ")" and input[1] == "(" and input[-2] == ")"):
        input = input[1:-1]
        
    if "<->" in input:
        input = iffRule(input)
        print ("result after iff rule: " + input)

    if "->" in input:
        input = implicationRule(input)
        print ("result after implication rule: " + input)
    
    if "!(" in input:
        input = propagateNot(input)
        print ("result after not propagation: " + input)
    
    if "!!" in input:
        input = doubleNegationRule(input)
        print ("result after double negation rule: " + input)
        
    
    if ")^(" in input:
        input = andResolution(input)

    if "v(" in input or ")v" in input:
        input = "("+ distributeOrRule(input) + ")"
        print ("result after distribute or rule: " + input)

    return input

def cleanupBrackets(input):
    operatorInClause = checkIfSurroundedByBrackets(input,1)
    if operatorInClause !=None:
        return (input[0:operatorInClause[0]] + input[operatorInClause[0]+1:operatorInClause[1]] + input[operatorInClause[1]+1:])
    else: return input
        

def main():
    """
    while True:
        inputFormula = input("Input formula: ")
        if inputFormula == "quit":
            print("Ending program.")
            break
        inputFormula = cleanupBrackets(inputFormula)
        print(inputFormula)
        outputFormula = convertToCNF(inputFormula)
        outputFormula = convertToClause("(" + outputFormula + ")")
        print("Output formula: " + outputFormula + "\n")
    """     
    

    expression = initiate('cnf.txt')
    print(expression)
    expression = cleanupBrackets(expression)
    print(expression)
    outputFormula = convertToCNF(expression)
    outputFormula = convertToClause("(" + outputFormula + ")")
    print("Output formula: " + outputFormula + "\n")
    return outputFormula
    
if __name__ == "__main__":
    main()

