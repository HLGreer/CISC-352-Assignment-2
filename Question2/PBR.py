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

# Convert the string returned from the CNF function to the
def cnfToList(cnfStr):
    noSquigMatch = re.match(r'\{(.*)\}', cnfStr)
    noSquig = noSquigMatch.group(1)
    splitArr = re.findall(r'\(([^)]*)\)', noSquig)
    for i in range(0,len(splitArr)):
        splitArr[i] = splitArr[i].split(',')
    return splitArr

#coded by other group
#notes to other group:
# return as lowercase plz
# no whitespace
# individual atoms in brackets
# i.e.) {(a,b),(c,!d),(a)}
def CNF(predicate):
    return

def negateL(l):
    if len(l) > 1:
        negL = l[1]
    else:
        negL = '!' + l
    return negL

def unit_propagate(F):
    hasUnit = True
    while hasUnit:
        l=""
        for i in range(0,len(F)):
            if len(F[i]) == 1:
                l = F[i][0]
                print l
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
            outF = outF.append(clause)
        elif negL in clause:
            clause[:] = [x for x in clause if x != negL]
            outF.append(clause)
    return outF

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

def main():
    txtFiles = glob.glob('./*.txt')
    fileIn = txtFiles[0]
    predicates = loadTextfile(fileIn)
    finalCNF = []
    concRE = re.compile('Therefore\,\s+(.*)\.')
    for i in range(0, len(predicates)):
        conclusion = concRE.match(predicates[i]) #check if matches regex for conclusion.
        if conclusion:
            predicates[i] = "!(" + conclusion.group(1) + ")" #Negate the conclusion
        finalCNF += CNF(predicates[i])
    sat = dpll(finalCNF)
    outFile = open("out.txt","w")
    if sat:
        outFile.write("The conclusion does not follow logically from the premises.")
    else:
        outFile.write("The conclusion follows logically from the premises.")
    outFile.close()
    print "Result stored in out.txt"


if __name__ == "__main__":
    main()