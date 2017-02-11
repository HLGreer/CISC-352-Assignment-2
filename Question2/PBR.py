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

def dpll(F, U):
    pass

def unit_propagate(F, U):
    pass

def main():
    txtFiles = glob.glob('./*.txt')
    fileIn = txtFiles[0]
    predicates = loadTextfile(fileIn)
    finalCNF = []
    for i in range(0, len(predicates)):
        if i == (len(predicates)-1):
            predicates[i] = convertConclusion(predicates[i])
        finalCNF += CNF(predicates[i])
    


if __name__ == "__main__":
    main()