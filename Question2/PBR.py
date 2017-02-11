'''
Created by Hannah Greer, Mike Kennelly, and Hillary Elrick
For CISC 352, Winter 2017

Assignment 2 - Proof by Refutation
'''

import re

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
    pass

# Conclusion is a string with a "Therefore, " statement (any case)
def convertConclusion(conclusion):
    conclusion = conclusion.lower()
    conclusion.replace("therefore, ", "")
    return conclusion

