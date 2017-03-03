
"""
Cisc 352 Assignment 2
CNF Part written by:
-Justin Gerolami
- Anna Ilina
- Emerson Wang
- Kyle Delaney
"""


def removeWhitespace(sentence):
  i = 0
  stack, out, s = [], [], []
  precedence = {'!': 4, '^': 3, 'v': 2, '->': 1, '<->': 0}
  sentence = sentence.replace(' ', '')
  newSentence = ""
  if (sentence[0] == '('):
    return sentence
  while (i < len(sentence)):
    if (sentence[i] not in precedence and sentence[i] not in {'<', '-'}):
      newSentence += sentence[i]
      i += 1
    elif (sentence[i] == '-'):
      newSentence += ' '
      newSentence += '->'
      i += 2
      newSentence += ' '
    elif (sentence[i] == '<'):
      newSentence += ' '
      newSentence += '<->'
      i += 3
      newSentence += ' '
    elif (sentence[i] in precedence):
      newSentence += ' '
      newSentence += sentence[i]
      i += 1
      newSentence += ' '
  s = newSentence.split()
  for token in s:
    if (token not in precedence):
      out.append(token)
    else:
      while (stack and precedence[token] <= precedence[stack[0]]):
        out.append(stack.pop(0))
      stack.insert(0, token)
  while (stack):
    out.append(stack.pop(0))
  return out


def groupByOperatorPrecedence(str):
  stack, out, ops = [], [], ['!', '^', 'v', '->', '<->']
  for token in str:
    if (token not in ops):
      stack.append(token)
    else:
      if (token == '!'):
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
  if (str[0] != '('):
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

#
# def findRightmostClause(string):
#   length = len(string)
#
#   # if rightmost element is a close bracket, return the bracketed term
#   if string(length - 1) == ")":
#     countBrackets = 1
#
#     for i in range(length - 2, -1, -1):
#       if string[i] == "(":
#         countBrackets -= 1
#         if countBrackets == 0:
#           # we have found the open bracket corresponding to the last
#           # close bracket
#           clauseStartIndex = i
#           return string[clauseStartIndex: length]
#       if string[i] == ")":
#         # there are nested brackets
#         countBrackets += 1
#
#     # should have returned in loop above, otherwise error
#     print("***ERROR in findRightmostClause function")
#
#   # else, return the entire string as a clause
#   else:
#     return string
#
#
# def findLeftmostClause(string):
#   length = len(string)
#
#   # if rightmost element is a close bracket, return the bracketed term
#   if string(0) == "(":
#     countBrackets = 1
#
#     for i in range(length):
#       if string[i] == ")":
#         countBrackets -= 1
#         if countBrackets == 0:
#           # we have found the close bracket corresponding to the
#           # first open bracket
#           clauseEndIndex = i
#           return string[0: clauseEndIndex + 1]
#       if string[i] == "(":
#         # there are nested brackets
#         countBrackets += 1
#
#     # should have returned in loop above, otherwise error
#     print("***ERROR in findLeftmostClause function")
#   # else, return the entire string as a clause
#   else:
#     return string
#
#
# # if index is in a bracketed clause, return the clause (it may be part of a larger expression)
# # else, return None


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
    #print("***ERROR in checkIfSurroundedByBrackets")
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
      # print("A = " + A)
      # print("B = " + B)

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
  # this will be used to store the letters of each word
  word = ""
  # loop through the sequence provided (in between brackets)
  for i in range(len(input)):
    # If the character is not a symbol, add it to our list
    # if input[i] != "(" and input[i] != ")" and input[i] != "^" and input[i] != "v" and input[i] != "!":
    # If we have and or or, or we are at the end of the expression, add the word we built
    if input[i] == "v" or input[i] == "^" or i == (len(input) - 1):
      # print("added: " + word)
      notList.append(word)
      word = ""
    # It is a letter or atom, store it in the word
    elif input[i] != "(" and input[i] != ")" and input[i] != "!":
      word += input[i]

  # print(notList)

  # loop through the atoms in our list that need an ! added
  for i in range(len(notList)):
    # replace the atom with !atom (A into !A)
    input = input.replace(notList[i], "!" + notList[i])
  # return
  return input


def doubleNegationRule(input):
  input = input.replace("!!", "")
  return input

def isClause(input):
  #hoping everything will be in proper bracket format
  if input.startswith('(') and findCorrespondingCloseBracket(input, 0) == len(input) - 1:
    return True

  if '(' not in input and ')' not in input and '^' not in input and 'v' not in input:
    return True

  return False

def isAndMainOperatorInClause(string, clauseStart, clauseEnd):
  #returns the index of AND if it is the main operator in clause, otherwise returns None
  #print("is and main operator in clause...")
  #print("string = " + string)
  #print (clauseStart)
  #print (clauseEnd)

  numAndsInClause = string[clauseStart: clauseEnd+1].count('^')
  #print (numAndsInClause)

  if numAndsInClause == 0:
    return None

  lastAndIndexChecked = clauseStart
  andIndex = None
  leftOfAnd = None
  rightOfAnd = None

  for i in range(numAndsInClause):
    andIndex = string.find('^', lastAndIndexChecked, clauseEnd+1)
    #print ("andIndex")
    #print(andIndex)
    lastAndIndexChecked = andIndex
    leftOfAnd = string[clauseStart+1:andIndex]
    rightOfAnd = string[andIndex+1:clauseEnd]
    #print ("leftOfAnd: ", leftOfAnd)
    #print ("rightOfAnd: ", rightOfAnd)
    if isClause(leftOfAnd) and isClause(rightOfAnd):
      return andIndex

  return None

def distributeOrRule(input):

  #rule: A v (B ^ C) = (A v B) ^ (A v C)

  indexLastOrChecked = -1

  while(True):

    usedRule = False

    #check if of form Av(B^C)
    orIndex = input.find("v(", indexLastOrChecked + 1, len(input))
    #orIndex = input.find("v(")

    if orIndex != -1:
      #indexLastOrChecked = orIndex
      orInClause = checkIfSurroundedByBrackets(input, orIndex)
      left = "" #leftOfClause
      right = "" #rightOfClause
      leftOuterBracket = -1
      rightOuterBracket = len(input)
      if orInClause != None:
        leftOuterBracket = orInClause[0]
        rightOuterBracket = orInClause[1]
        left = input[:leftOuterBracket]
        right = input[rightOuterBracket + 1 :]

      rightClauseCloseBracket = findCorrespondingCloseBracket(input, orIndex+1)
      mainAndIndex = isAndMainOperatorInClause(input, orIndex+1, rightClauseCloseBracket)

      if mainAndIndex == None: # right side is not of form (B^C); look at next or
        #print ("and is not main operator in clause")
        pass
      else:
        #it's of form Av(B^C)

        A = input[leftOuterBracket + 1:orIndex]
        B = input[orIndex+2:mainAndIndex]
        C = input[mainAndIndex + 1: rightClauseCloseBracket]

        input = left + "(((" + A + ")v(" + B + "))^((" + A + ")v(" + C + ")))" + right
        usedRule = True


    #check if of form left+((B^C)vA)+right
    orIndex2 = input.find(")v", indexLastOrChecked + 1, len(input))
    #orIndex2 = input.find(")v")

    if orIndex2 != -1:
      orIndex2 = orIndex2 + 1 #to get rid of bracket
      #indexLastOrChecked = orIndex2

      orInClause = checkIfSurroundedByBrackets(input, orIndex2)
      left = "" #leftOfClause
      right = "" #rightOfClause
      leftOuterBracket = -1
      rightOuterBracket = len(input)
      if orInClause != None:
        leftOuterBracket = orInClause[0]
        rightOuterBracket = orInClause[1]
        left = input[:leftOuterBracket]
        right = input[rightOuterBracket + 1 :]


      leftClauseOpenBracket = findCorrespondingOpenBracket(input, orIndex2 - 1)
      mainAndIndex = isAndMainOperatorInClause(input, leftClauseOpenBracket, orIndex2-1)
      #print(leftClauseOpenBracket)
      #print(orIndex2 - 1)

      if mainAndIndex == None: # right side is not of form (B^C); look at next or
        #print ("and is not main operator in clause")
        pass
      else:
        #it's of form left+((B^C)vA)+right

        A = input[orIndex2 + 1 : rightOuterBracket]
        B = input[leftClauseOpenBracket + 1:mainAndIndex]
        C = input[mainAndIndex + 1: orIndex2-1]

        input = left + "(((" + A + ")v(" + B + "))^((" + A + ")v(" + C + ")))" + right
        usedRule = True

    print(orIndex)
    print(orIndex2)
    print (usedRule)
    print("")
    if orIndex == -1 and orIndex2 == -1:
      break
    elif usedRule == False and (orIndex == -1 or orIndex2 == -1) :
      indexLastOrCheck near ted = max(orIndex, orIndex2)
    elif orIndex == orIndex2 and usedRule == False:
      indexLastOrChecked = orIndex
    else: #usedRule == True:
      indexLastOrChecked = -1 #reset

    #print ("test: " + input)
    input = cleanupBrackets(input)
    #print ("after cleanup brackets: " + input)

  #once more after loop
  #print ("test: " + input)
  input = cleanupBrackets(input)
  #print ("after cleanup brackets: " + input)

  return input



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
          # loop through from i to end, checking if there are any other expressions in the ()
          for j in range(i, len(cnf)):
            # if there is another expression we can add brackets
            if cnf[j] == "v" and opened == False:
              output += "("
              opened = True
            # no other expressions, remove brackets
            elif cnf[j] == ")":
              pass
              # output += "("
              # opened = True

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
  while (input[0] == "(" and input[-1] == ")" and input[1] == "(" and input[-2] == ")"):
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

  # if ")^(" in input:
  #   input = andResolution(input)

  if "v(" in input or ")v" in input:

    #for i in range(5):

    input = cleanupBrackets(input)
    #print ("after cleaning up brackets: " + input)

    input = "(" + distributeOrRule(input) + ")"
    print ("result after distribute or rule: " + input)

  return input



def findCorrespondingCloseBracket(string, openBracketIndex):
  length = len(string)
  index = openBracketIndex
  correspondingCloseBracketIndex = None

  # check for close bracket right of index
  countOpenBrackets = 0
  for i in range(index + 1, length):
    if string[i] == "(":
      countOpenBrackets += 1  # checking for nested brackets
    if string[i] == ")":
      countOpenBrackets -= 1
      if countOpenBrackets < 0:
        correspondingCloseBracketIndex = i
        break

  return correspondingCloseBracketIndex

def findCorrespondingOpenBracket(string, closeBracketIndex):
  length = len(string)
  index = closeBracketIndex
  correspondingOpenBracketIndex = None

  # check for close bracket right of index
  countCloseBrackets = 0
  for i in range(index -1, -1, -1):
    if string[i] == ")":
      countCloseBrackets += 1  # checking for nested brackets
    if string[i] == "(":
      countCloseBrackets -= 1
      if countCloseBrackets < 0:
        correspondingOpenBracketIndex = i
        break

  return correspondingOpenBracketIndex


#removes outside brackets if whole input is in matching brackets ( ..input.. ) and also double bracket ((..))
def cleanupBrackets(input):
  if len(input) < 1:
    return input
  #check if there are unnecessary brackets around whole expression; clean up outer brackets
  #ie something like (((AvB))) becomes AvB
  while (True):
    if input.startswith('(') == False:
      break
    correspondingCloseBracketIndex = findCorrespondingCloseBracket(input, 0)
    if correspondingCloseBracketIndex == len(input)-1:
      input = input[1:len(input)-1]
    else:
      break
  # extra outer brackets should now be removed

  # now remove double brackets, ie something like ((AvB))^C becomes (AvB)^C
  i = 0
  correspondingCloseBracketFirst = None
  correspondingCloseBracketSecond = None
  while (True):
    if len(input[i:]) < 2:
      break
    if input[i] == '(' and input[i+1] == '(':
      correspondingCloseBracketSecond = findCorrespondingCloseBracket(input, i)
      correspondingCloseBracketFirst = findCorrespondingCloseBracket(input, i+1)
      if correspondingCloseBracketSecond == correspondingCloseBracketFirst + 1:
        #then these are redundant double brackets
        input = input[:i] + input[i+1:correspondingCloseBracketFirst] + input[correspondingCloseBracketSecond:]
        i = i-1

    i = i+1

  return input

def convertToClauseWithBrackets(cnf):
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
        # Adds bracket
        else:
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
        # if we are adding an atom and havent added a bracket, add one
        if opened == False:
          output += "("
          opened = True

        # If we are opened and the next char is ^ or the end, add )
        if opened and (i == len(cnf) - 1 or cnf[i + 1] == "^"):
          output += cnf[i] + ")"
          opened = False

        else:
          # add the atom
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
  # print(expression)
  expression = cleanupBrackets(expression)
  print(expression)

  outputFormula = convertToCNF(expression)
  CNF = convertToClause("(" + outputFormula + ")")
  print("Output formula: " + CNF + "\n")

  # for the map problem - add brackets to single atoms
  outputFormula = convertToClauseWithBrackets(outputFormula)
  # print(outputFormula)
  return outputFormula


if __name__ == "__main__":
  main()
