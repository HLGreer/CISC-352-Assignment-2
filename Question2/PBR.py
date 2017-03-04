'''
Created by Hannah Greer, Mike Kennelly, and Hillary Elrick
For CISC 352, Winter 2017

Assignment 2 - Proof by Refutation
'''

import re, glob

def loadTextfile(textfile):
    with open(textfile) as f:
        lines = f.read().splitlines()
    for line in lines:
        line = line.lower()
    return lines

# Convert the string returned from the CNF function to list
def cnfToList(cnfStr):
    noSquigMatch = re.match(r'\{(.*)\}', cnfStr)
    noSquig = noSquigMatch.group(1)
    splitArr = re.findall(r'\(([^)]*)\)', noSquig)
    for i in range(0,len(splitArr)):
        splitArr[i] = splitArr[i].split(',')
    return splitArr

#import function from Question 1
def CNF(predicate):
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Question1'))
    from convertToCNF import convertToCNF
    output = convertToCNF(predicate)
    #ensures atoms are put in parentheses
    if len(output) > 4:
        return '{' + convertToClause_PBR('(' + output + ')') + '}'
    elif len(output) == 4:
        return '{' + output + '}'
    return '{' + '(' + output + ')' + '}'


def negateL(l):
    if "!" in  l:
        negL = l[1:]
    else:
        negL = '!' + l
    return negL

def unit_propagate(F):
    hasUnit = True
    while hasUnit:
        l=""
        for i in range(0,len(F)):
            if len(F[i]) == 0:
                continue
            if len(F[i]) == 1:
                l = F[i][0]
                break
        if l == "":
            hasUnit = False
        if(hasUnit):
            F = remove_unit(F,l)
    return F

def remove_unit(F,l):
    outF = []
    negL = negateL(l)
    for clause in F:
        if l not in clause and negL not in clause:
            outF.append(clause)
        elif negL in clause:
            clause[:] = [x for x in clause if x != negL]
            outF.append(clause)
    return outF

def dpll(F):
    print F
    F = unit_propagate(F)
    if len(F)==1 and F[0]==[]:
        return False
    elif F==[]:
        return True
    elif [] in F:
        return False
    flag = True
    '''for x in range(0, len(F)):
        if F[x] is []:
            F.remove(F[x])
    if F==[]:
        return False'''
    print F[0]
    l = None

    for x in F:
        if len(x) > 0:
            l = x[0]
            break
    if l == None:
        return True

    negL = negateL(l)
    FsubL = remove_unit(F,l)
    FsubNL = remove_unit(F,negL)
    return dpll(FsubL) or dpll(FsubNL)

'''
def dpll(F):
    F = unit_propagate(F)
    if len(F)==1 and F[0]==[]:
        return False
    elif F==[]:
        return True
    l = F[0][0]
    negL = negateL(l)
    FsubL = remove_unit(F,l)
    FsubNL = remove_unit(F,negL)
    return dpll(FsubL) or dpll(FsubNL)
'''

#convert to clause modified from Question 1
def convertToClause_PBR(cnf):
    # flag
    opened = False
    # initial {
    output = ""
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
                    for j in range(i,len(cnf)):
                        #if there is another expression we can add brackets
                        if cnf[j] == "v" and opened == False:
                            output += "("
                            opened = True
                        #no other expressions, remove brackets
                        elif cnf[j] == ")":
                            pass
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
    return output

def main():
    txtFiles = glob.glob('./*.txt') #imports any file in directory with .txt extension
    if './out.txt' in txtFiles:
        txtFiles.remove('./out.txt') #removes if file called out.txt
    fileIn = txtFiles[0]
    predicates = loadTextfile(fileIn)
    finalCNF = []
    concRE = re.compile('Therefore\,\s+(.*)\.')
    print(predicates)
    for i in range(0, len(predicates)):
        conclusion = concRE.match(predicates[i]) #check if matches regex for conclusion.
        if conclusion:
            predicates[i] = "!(" + conclusion.group(1) + ")" #Negate the conclusion
        predicates[i].replace(" ","")
        print(predicates[i] + " after: " + CNF(predicates[i]))
        finalCNF += cnfToList(CNF(predicates[i]))
        print(finalCNF)

    print(finalCNF)
    sat = dpll(finalCNF) #runs the dpll algorithm
    outFile = open("out.txt","w")
    if sat:
        outFile.write("The conclusion does not follow logically from the premises.")
    else:
        outFile.write("The conclusion follows logically from the premises.")
    outFile.close()
    print "Result stored in out.txt"

if __name__ == "__main__":
    main()
