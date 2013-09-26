#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Python script testing randomness of numbers
#   
#  Author: Lars Egholm Pedersen (egholm@nbi.dk)
#  Date:   19/9 2013
#
#  Run by: ./RandomDigitsTest.py
#
# ----------------------------------------------------------------------------------- #

# Load modules here
from ROOT import *

# ----------------------------------------------------------------------------------- #
# Define your functions here
# ----------------------------------------------------------------------------------- #

#Calculate the sqr of a function
def sqr( a ) : return a*a


# ----------------------------------------------------------------------------------- #
# Define and get input
# ----------------------------------------------------------------------------------- #

# Write extensive output
verbose = True

# Define list of input files
infiles = ["./data_RandomDigits2013A.txt" ]
#           "./data_RandomDigits2011.txt" , #Add these when you got a good feeling
#           "./data_RandomDigits2012.txt" ] #what is going on in the 2013 case

# List containing all numbers
numbers = []

# Loop over input files open them in read mode
for ifile in infiles : 
    with open( ifile, "r" ) as current_file : 
        # Extract current file info : loop through each line in the file, loop through each character
        # in the line, demand character is not empty ("") and convert the result to an integer
        # Finally add result to the numbers list
        numbers += [int(char) for line in current_file for char in line.strip() if char is not ""]

# Print out your numbers, to see everything works correctly
if verbose : 
    for i, inumb in enumerate( numbers ) : 
        print "%d"%(inumb),
        if (i%50 == 0 and i > 0) : print ""

print
print "The total number of digits is ", len(numbers)





# ----------------------------------------------------------------------------------- #
# 
# First look at the random digits, and see if you see any patterns? Probably rarely, mostly
# because there are many numbers, and patterns are not that visible. So, you will have to
# work a bit...  with statistical tests.
# 
# Before even looking at the above program, think about what statistical tests you
# could submit the sample to. Then consider, how to actually carry out these tests.
# We will try in class to compile and discuss a list, before we start working on it!!!
# 
# 
# 
# Questions:
# ----------
# 1) Are each digit represented roughly equally many times? Are there as many
#    even as odd numbers? And do people have a tedency to choose an even number
#    after an odd and vice versa? How about high vs. low numbers?
# 
# 2) Are people "afraid" of putting the same digit twice in a row? And how about three
#    or four identical digits in a row?
# 
# 3) Try to count, which digits follows which digits. That should be 100 counts in total.
#    If the numbers were truly random, what would you expect then? Is that what you
#    observe?
#    Can you test this for example with a Chi-Square (think about how many numbers you
#    expect in each bin) and/or a likelihood?
# 
# 4) Were the students of 2011 and 2012 better or worse at picking random numbers?
# 
# ----------------------------------------------------------------------------------- #
