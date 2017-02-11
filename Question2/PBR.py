'''
Created by Hannah Greer, Mike Kennelly, and Hillary Elrick
For CISC 352, Winter 2017

Assignment 2 - Proof by Refutation
'''

import re, glob

def loadTextfile(textfile):
    with open(textfile) as f:
        lines = f.read().splitlines()
    return lines


'''
# We may need to read in from the stdin input?
def readInput():
    # until the therefore is read, just grab each item and send to CNF
    end = False
    while end == False:
        theInput = raw_input(">")
        match = re.match(r'therefore(.*)', theInput.lower())
        if match: # If the input contains the Therefore statement
            # stop taking input
'''

# Convert the string returned from the CNF function to the
def cnfToList(cnfStr):
    noSquigMatch = re.match(r'\{(.*)\}', cnfStr)
    noSquig = noSquigMatch.group(1)
    splitArr = re.findall(r'\(([^)]*)\)', noSquig)
    for i in range(0,len(splitArr)):
        splitArr[i] = splitArr[i].split(',')
    return splitArr
        

# Conclusion is a string with a "Therefore, " statement (any case)
def convertConclusion(conclusion):
    conclusion = conclusion.lower()
    conclusion.replace("therefore, ", "")
    return conclusion

#coded by other group
#notes to other group:
# return as lowercase plz
# no whitespace
# individual atoms in brackets
# i.e.) {(a,b),(c,!d),(a)}
def CNF(predicate):
    return

def dpll(F):
    F = unit_propagate(F)
    if len(F)==1 and F[0]==[]:
        return False
    else:
        return True
    l = F[0][0]
    FsubL = remove_unit(F,l)
    if len(l)==2:
        negL = l[1]
    else:
        negL = "!"+l
    FsubNL = remove_unit(F,negL)
    return dpll(FsubL) or dpll(FsubNL)


def unit_propagate(F):
    l = ""
    hasUnit = True
    while hasUnit:
        for i in range(0,len(F)):
            if len(F[i]) == 1:
                l = F[i][0]
                break
            elif i == (len(F) - 1):
                hasUnit = False
        if(hasUnit):
            remove_unit(F,l)
    return F

def remove_unit(F,l):
    outF = []
    if len(l) > 1:
        negL = l[1]
    else:
        negL = '!' + l
    for clause in F:
        if l not in clause and negL not in clause:
            outF = outF.append(clause)
        elif negL in clause:
            clause[:] = [x for x in clause if x != negL]
            if(clause != []):
                outF.append(clause)
    return outF

def main():
    txtFiles = glob.glob('./*.txt')
    fileIn = txtFiles[0]
    predicates = loadTextfile(fileIn)
    finalCNF = []
    for i in range(0, len(predicates)):
        if i == (len(predicates)-1):
            predicates[i] = convertConclusion(predicates[i])
        finalCNF += CNF(predicates[i])
    sat = dpll(finalCNF)



if __name__ == "__main__":
    main()