print ("hello")

# CLOSE_BRACKET = ")"
# OPEN_BRACKET = "("

def removeWhitespace():
  return

def groupByOperatorPrecedence():
  return

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
#     index += len(substring) # since we're not searching for overlapping occurrences


def findRightmostClause(string):
  length = len(string)

  #if rightmost element is a close bracket, return the bracketed term
  if string(length-1) == ")":
    countBrackets = 1

    for i in range(length-2, -1, -1):
      if string[i] == "(":
        countBrackets -= 1
        if countBrackets == 0:
          # we have found the open bracket corresponding to the last close bracket
          clauseStartIndex = i
          return string[clauseStartIndex : length]
      if string [i] == ")":
        # there are nested brackets
        countBrackets += 1

    #should have returned in loop above, otherwise error
    print "***ERROR in findRightmostClause function"

  # else, return the entire string as a clause
  else:
    return string


def findLeftmostClause(string):
  length = len(string)

  #if rightmost element is a close bracket, return the bracketed term
  if string(0) == "(":
    countBrackets = 1

    for i in range(length):
      if string[i] == ")":
        countBrackets -= 1
        if countBrackets == 0:
          # we have found the close bracket corresponding to the first open bracket
          clauseEndIndex = i
          return string[0 : clauseEndIndex + 1]
      if string [i] == "(":
        # there are nested brackets
        countBrackets += 1

    #should have returned in loop above, otherwise error
    print "***ERROR in findLeftmostClause function"
  # else, return the entire string as a clause
  else:
    return string

#if index is in a bracketed clause, return the clause (it may be part of a larger expression)
#else, return None
def checkIfSurroundedByBrackets(string, index):
  length = len(string)

  clauseStartIndex = None
  clauseEndIndex = None

  #check for open bracket left of index
  countCloseBrackets = 0
  for i in range(index-1, -1, -1):
    if string[i] == ")":
      countCloseBrackets += 1 # checking for nested brackets
    if string[i] == "(":
      countCloseBrackets -=1
      if countCloseBrackets < 0:
        clauseStartIndex = i
        break

  #check for close bracket right of index
  countOpenBrackets = 0
  for i in range(index+1, length):
    if string[i] == "(":
      countOpenBrackets += 1 #checking for nested brackets
    if string[i] == ")":
      countOpenBrackets -=1
      if countOpenBrackets < 0:
        clauseEndIndex = i
        break

  if clauseStartIndex != None and clauseEndIndex != None:
    return [clauseStartIndex, clauseEndIndex]
  elif clauseStartIndex == None and clauseEndIndex == None:
    return None
  else:
    print "***ERROR in checkIfSurroundedByBrackets"
    return


#rule: A <-> B = (A->B) ^ (B->A)
def iffRule(input):

  #for i in range(numIffOccurrences): # do the iffRule for each "<->" found
  while (input.count("<->") > 0):
    #check if "<->" is in its own bracket set (in a clause)
    operatorIndex = input.find("<->")

    operatorInClause = checkIfSurroundedByBrackets(input, operatorIndex)

    if operatorInClause == None: #if not in brackets:
      # print("iff is not surrounded by brackets")
      A = input[0 : operatorIndex]
      B = input[operatorIndex + 3 : len(input)] # since "<->" is 3 chars long
      input = "(" + A + "->" + B + ")^(" + B + "->" + A + ")"

    else: #iff in brackets; apply rule to just that clause
      # print("iff is in clause")
      #clause includes brackets
      clauseStartIndex = operatorInClause[0]
      clauseEndIndex = operatorInClause[1]
      leftOfClause = input[0 : clauseStartIndex]
      rightOfClause = input[clauseEndIndex + 1 : len(input)]
      A = input[clauseStartIndex + 1: operatorIndex] # don't include bracket
      B = input[operatorIndex + 3 : clauseEndIndex] # since "<->" is 3 chars long # don't include bracket

      # print ("leftOfClause = " + leftOfClause)
      # print ("rightOfClause = " + rightOfClause)
      # print("A = " + A)
      # print("B = " + B)

      input = leftOfClause + "((" + A + "->" + B + ")^(" + B + "->" + A + "))" + rightOfClause

  return input

def implicationRule(input):

  #for i in range(numIffOccurrences): # do the iffRule for each "<->" found
  while (input.count("->") > 0):
    #check if "<->" is in its own bracket set (in a clause)
    operatorIndex = input.find("->")

    operatorInClause = checkIfSurroundedByBrackets(input, operatorIndex)

    if operatorInClause == None: #if not in brackets:
      # print("implication is not surrounded by brackets")
      A = input[0 : operatorIndex]
      B = input[operatorIndex + 2 : len(input)] # since "<->" is 3 chars long
      input = "!(" + A + ")v(" + B + ")"

    else: #iff in brackets; apply rule to just that clause
      # print("implication is in clause")
      #clause includes brackets
      clauseStartIndex = operatorInClause[0]
      clauseEndIndex = operatorInClause[1]
      leftOfClause = input[0 : clauseStartIndex]
      rightOfClause = input[clauseEndIndex + 1 : len(input)]
      A = input[clauseStartIndex + 1: operatorIndex] # don't include bracket
      B = input[operatorIndex + 2 : clauseEndIndex] # since "<->" is 3 chars long # don't include bracket

      # print ("leftOfClause = " + leftOfClause)
      # print ("rightOfClause = " + rightOfClause)
      # print("A = " + A)
      # print("B = " + B)

      input = leftOfClause + "(!(" + A + ")v(" + B + "))" + rightOfClause

  return input

def propagateNot(input):
  #while there are still nots needing to be propagated
  while (input.count("!(") > 0):
    #setup a counter for brackets
    count = 0
    #get the location of the first one
    location = input.find("!(")
    
    #remove the not before the bracket, keep the bracket
    input = input[0:location] + input[location+1] + input[location+2:len(input)]
    
    #loop through the open bracket, starting at the location of !(
    for i in range(location, len(input)):
      #if we open more brackets, add to the count
      if input[i] == "(":
        count += 1

      #if we close a bracket, remove from the count
      elif input[i] == ")":
        count -=1
        
        #if we have no more brackets we are done with this iteration
        #store the end location so we know how far to add negations
        if count == 0:
          endLocation = i
          #make the input equal to:
          #the start to the first !( +
          #add "!" to the first bracket section +
          #add the end (which may contain more !(, dealt with in following iterations of while loop
          input = input[0:location] + addNot(input[location:endLocation+1]) + input[endLocation+1:len(input)]
          #break the loop and go back to the while loop
          break

      #If there is an ^, change it to v
      elif input[i] == "^":
        input = input[0]  + input[1:i] + "v" + input[i+1:len(input)]

      #If there is an v, change it to ^
      elif input[i] == "v":
        input = input[0]  + input[1:i] + "^" + input[i+1:len(input)]
  
  return input

def addNot(input):
  #create a list for storing atoms
  notList = []
  #loop through the sequence provided (in between brackets)
  for i in range(len(input)):
    #If the character is not a symbol, add it to our list
    if input[i] != "(" and input[i] != ")" and input[i] !="^" and input[i]!="v" and input[i]!= "!":
      #print (input[i])
      #append the atom to our list
      notList.append(input[i])
  #print(notList)

  #loop through the atoms in our list that need an ! added
  for i in range(len(notList)):
    #replace the atom with !atom (A into !A)
    input = input.replace(notList[i], "!" + notList[i])
  #return
  return input
  

def doubleNegationRule(input):
   #loop while there are still !! left
   while (input.count("!!") > 0):
     #find the !!
     operatorIndex = input.find("!!")
     #Replace them with nothing
     input = input[0:operatorIndex] + input[operatorIndex + 2 : len(input)]
   #return
   return input

def distributeOrRule():
  return

def convertToClausalForm():
  return

def convertToCNF(input):
  print ("input string: " + input)
  #input is string, grouped by operator precedence (with brackets) and whitespace removed

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
  return

#input1 = "((A^B)vC)->D"
#input2 = "Av(B^c)"
#input3 = "A<->B"
#input4 = "(A<->B)"
#input5 = "A<->B<->C" #would not be tested; this would be in brackets after emerson's function
#input5 = "A<->(B<->C)"
#input6 = "A->B"
#input7 = "(A->B)"

#input8 = "!!(A v !B) ^ !!B"
#input9 = "!(AvB^C^(!DvE)^!F)"
#input10 = "(!(A^B)^!C)vD"
#input11 = "((!Av!B)^!C)vD"
#input12 = "(!(A^B)^!(AvC)vD)^(!(AvB)vG)"
convertToCNF(input12)
