#!/usr/bin/env python

# Above statement tells your terminal that the script should be run in
# a python enviroment.

# --------------------------------------------------------- #
#  Script illustrating some basic python functionality
#
#  Author: Lars Egholm Pedersen (Niels Bohr Institute)
#  Date:   26/8 - 2013
#
#  Make script executable from command line: chmod +x pythonIntro.py
#
#  Run by: ./pythonIntro.py
#
#  Since output is rather long it can by recommeded to run by
#  ./pythonIntro.py | less
#
#  Which will make it possible to scroll up and down in the
#  Written output with the arrowkeys. Try to understand
#  Which part of the code prints which
#
# --------------------------------------------------------- #

#Import statements
import math, ROOT

#Tells python which modules it should load. You can now access the
#functionality of e.g. math by math.sqrt( number ) to get the square root etc.


# -------------------------------------------------------------------------------
# Variable declaration
# -------------------------------------------------------------------------------

# Declare an integer
myint = 1

# Declare a float
myfloat = 1.0

# Notice the difference in the declaration.
# Be carefull of the difference. One common error is if you want to compare
# your variables to a number:
#   myint == 1       # Is true no matter what
#   myfloat == 1.0   # Could be. myfloat is a number with ??? digits, it could be either
#   0.9999999999999999999998 or 1.000000000000000001


# Some simple rules
another_float = myint * 2.0        # int comined with float gives float

another_int   = int(myfloat + 0.5) # Rounding floats to int
                                   # When rounding, you will always get the closest int lower
                                   # than the float. Thus if you add 0.5 before rounding, you
                                   # Will always get the closest int to the original float


# One important operater you will use time and again is the modulus operator %.
# a % b returns the remainder when deviding the integer a with the integer b.
# So if you wish to find out if 9312312 is divisible by 17, you can check this
# by asking if 93112312 % 17 is zero. More on this below.

#Strings
mystring = "This is a string"      #Use strings to store strings of letters


# -------------------------------------------------------------------------------
# Printing output
# -------------------------------------------------------------------------------

# You can use the print statement to print the output of your script to the terminal:

print "This is an int", myint
print "This is a float", myfloat
print mystring

print "This is an int", another_int, ". This is a float", another_float
print "It is also possible to write",
print "ints %d, floats %5.3f and strings: '%s' like this"%(another_int, another_float, mystring)

# In the last two lines, you tell the intepreter that you don't want the line to end
# by ending the print statement in a comma.
# In the last statement you tell the print statement, that it is going to fill an integer %d (digit)
# a float with 5 characters, where three are after the decimal point %5.3f and a string %s into
# the line. The variables in the parenthesis is then filled in on the corresponding places.

print "" #Print an empty line
print "New line \n line starts here \t and is tabulated"
print "" #Print an empty line


# -------------------------------------------------------------------------------
# Lists
# -------------------------------------------------------------------------------

# Often you want to store a large number of variables together. Intead of having
# to declare them one by one. The list offers a simple way of organisation

simplelist = [0.0, 0.0, 0.0, 0.0, 0.0]   # List of 5 floating point zeros

simplelist[2] = 13.0   # Assign the '2' entry to 13.0.

# NOTE, as in most modern programming languages, you count from zero:
# Entry number : 0    1    2    3    4
# simplelist = [0.0, 0.0, 0.0, 0.0, 0.0]

# If you now want to append some number to your list you can use the append function:
simplelist.append( 1.0 )
simplelist.append( 5.0 )
simplelist.append( 3.0 )

# One good thing to remember with python lists is that they are cyclical, which means
# you can also acess the numbers in the following way

# Entry number  -8   -7   -6   -5   -4   -3   -2   -1
# simplelist = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 5.0, 3.0]

# The reason this is smart is that if you use the append function and want to access
# The last appended value, you can use simplelist[-1] instead of simplelist[len(simplelist)-1]
# Where len( list ) is the function that gives you the length of a list.


# A lot of times it is cumbersome to declare each entry in the list by hand.
# If it is for instance necessary to store 100 numbers in your analysis, you
# can declare a list to contain them in the following way (if you are a python expert
# you probably know 10 other ways of doing this)

alotofzeros = [0.0]*100

print "My simple list     : ", simplelist
print "Which has          : ", len(simplelist), "Entries"
print "The first entry is : ", simplelist[1]
print "The last entry is  : ", simplelist[-1], simplelist[len(simplelist)-1]
print ""
print "A large list   : ", alotofzeros    # Not so nice output, will be adressed below.
print ""

# A great strenght of the python list is that you can store just about everything you want to
# in them. Say if you want to store a name and a score for some persons :

mixedlist = [ ["Max"  ,  7 ] , # This is a list of lists, each containing a string and an integer
              ["John" ,  12] ,
              ["Nick" , -3 ] ,
              ["Niels",  10] ]

# If you want to sort by score you can use the sorting function :
sortedlist = sorted( mixedlist, key=lambda name : name[1] )

# This is a bit more advanced since, you have to tell python
# that it should sort it by the 'second entry' in each list (i.e. column 1)
# If you only have a list with numbers thelist = [0, -214, 35, 12, 343, 1224] you can simply
# Use sorted( thelist ) or thelist.sort()


# -------------------------------------------------------------------------------
# Looping and logical statemants
# -------------------------------------------------------------------------------

# A lot of times you want to repeat a calculation with some different initial parameters
# which is where the loop comes in handy:

#This is a simple loop
for i in range( 10 ) :

    #This is the block within the loop
    print "Counting to ten : ", i

# This will tell the intepreter that it should make a list with the numbers 0, ..., 9
# For each of these numbers, it will assign i to the given value and perform whatever
# is inside the 'loop block' with that specific value of i.

print ""
#We can now return to how you can print list more nicely :
for ientry in mixedlist : # ientry will now be the ith entry in the mixed list,
                          # i.e ientry = "["max", 7] the first time etc.
    print "Name %s \t -> \t Score %3d"%( ientry[0], ientry[1] )


# If you both want the counter 'i' and the entry value 'ientry' of the list, the enumerate function
# provides a simple way to do this:
print ""
for i, ientry in enumerate( sortedlist ) :
    print "Counter %d \t Name %s \t -> \t Score %3d"%( i, ientry[0], ientry[1] )
print ""


# -------------------------------------------------------------------------------
# A note on programming blocks
# -------------------------------------------------------------------------------

# As is the case with programming, you will structure your code as blocks, just like above

# statement1 :
#
#    This is coding block1
#
#    statement2 :
#
#        This is the coding block2
#
#    ...
#
# Note that all the variables you declare in statement2 is only known in coding block2
# But everything you define in statement1 is also known in statement2
# Most programming languages you have probably seen incloses the statements
# with brackets or curly braces. In python this is done solely by indention
# (The recommeded pratice is to use four spaces). This means that the interpreter
# knows where e.g. coding block2 is (8 spaces) and when it stops (when you are back
# to 4 spaces). To learn more about the python development teams stance on braces,
# try to import :
# from __future__ import braces
# in your your terminal interpreter


# -------------------------------------------------------------------------------
# Back to looping and logical statemants
# -------------------------------------------------------------------------------

# To compare values, you can use the if statement
anint   = 3
afloat  = 314.0
astring = "string"

if anint == 3 :
    print "The integer value is three "

if afloat > 1000.0 :
    print "The float value is greater than 1000"

elif 100.0 < afloat < 500.0 :
    print "The float value is somewhere between 100. and 500."

else :
    print "Did not find the interval where a float value is in"

if astring is not "this does not say 'string'" :
    print "'astring' does not say 'string"

if astring is "string" : print "'astring' says", astring
print ""


# -------------------------------------------------------------------------------

# One very nice thing with python is you can combine lists, for loops and if statements
# in an intuitive way. If you e.g. want a list containing the first 20 square numbers, you
# can use what is called a list comprehension:

sqrnumbers = [isqr*isqr for isqr in range( 20 ) ]

for isqr in sqrnumbers : print "This is a square number ", isqr

print ""

# If you only want the even square numbers, you can use the modulus operator :
evensqrnumbers = [ isqr*isqr for isqr in range( 20 ) if isqr % 2 == 0 ]

for isqr in evensqrnumbers : print "This is an even square number", isqr

print ""


# -------------------------------------------------------------------------------

# Another form of loop is the while statement
whilevar = 0.0
while ( math.tan( whilevar ) < 1000.0 ) :
    whilevar += 3.1415926535897932385 / 10000

print "%6.3f is the first value whose tangent is greater than 1000 (%8.3f)."%(whilevar, math.tan( whilevar )),
print "(in steps of pi/10000)"

# Above while loop test weather tan( whilevar ) is less than 1000
# If it is greater than 1000 it will exit the loop. In the block
# inside the loop it will increment whilevar with pi / 10000, and
# run the test again


# -------------------------------------------------------------------------------
# Random numbers
# -------------------------------------------------------------------------------

# To generate some randoms numbers, we will use the ROOT class TRandom3

# Get the object from the ROOT module
r = ROOT.TRandom3()

# You can look up in the ROOT documentation for which kind of random numbers,
# (and functionality in general) It is possible to generate with the TRandom3 class.
#   http://root.cern.ch/root/html/TRandom3.html

# Print some random numbers uniformely distributed between 0 and 1 :
for i in range( 10 ) :
    print "This is a uniformely generated number", r.Uniform()   # Calls the uniform function

print ""

# Create some lists containing random numbers :

# List with 1000 uniformly distributed random numbers
uniflist = [r.Uniform() for i in range( 1000 ) ]

# List with 1000 gaussianly distributed random numbers
gauslist = [r.Gaus(0.0, 1.0) for i in range( 1000 ) ]

# Print a couple of numbers from the list
for i in range( 10 ) :
    print "Uni number %5.3f \t Gaussian number %5.3f"%( uniflist[i], gauslist[i] )
print ""


# -------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------

# To define a function, use the following structure
#
# def ( input ) :
#     function block
#     return value
#
# Normally it is good pratice to put this in the beginning of your
# script, but for the sake of readability we will just do it here in this case:


# Define a function that returns the square of a number
def sqr( a ) :
    return a*a

# Print the square of some of your random numbers :
for i in range( 10 ) :
    print "Uni : %5.3f^2 = %5.3f \t Gauss : %6.3f^2 = %5.3f"%( uniflist[i], sqr(uniflist[i]) ,
                                                               gauslist[i], sqr(gauslist[i]) )

print ""

# Define a more complicated function that calculates the mean and RMS of the values in a list

# Notice how the function is assigned an empty list in the start. This can be good pratice
# s.t. you don't by accident call it with a wrong object. The reason the sqr function was
# not defined in this way is that, it is in this way able to calculate squares of integers
# int * int = int and floats : float * float = float.
# Note that if you have several arguments in the function you should ALWAYS have the
# unassigned parameters first and the assigned afterwards :
#
# def somefunction( unassigned_a, unassigned_b, assigned_a = "somestring", assgined_b = 9999.0 ) :
#    ...

def MeanAndRMS( inlist = [] ) :

    if len( inlist ) == 0  :
        print "Ups, called function with an empty list"
        print "If I don't exit now, I will divide by zero"
        return [-9999999999.9, -99999999999.9]

    elif len( inlist ) == 1  :
        print "Ups, called function with a list of length one"
        print "If I don't exit now, I will divide by zero"
        return [inlist[0], -99999999999.9]

    # Find the mean :
    mu = 0.0
    for ientry in inlist : # Add all the values together
        mu += ientry       # This is equivalent to the mathematical sum
                           # Sigma_i ( x_i )

    mu = mu / len( inlist ) # Divide by the number of entries

    # Find the standard deviation
    std = 0.0
    for ientry in inlist :         # Again this is equivalent to :
        std += sqr( ientry - mu )  # Sigma_i ( x_i - mu )^2

    std = math.sqrt( std / (len(inlist) - 1) ) # Divide by N-1 and take the square root

    return [mu, std]

# A natural extension of this function would be to also return the uncertainties
# on the mean and the RMS!




# Calculate the mean and rms of the values in your two lists with random numbers :
mu_sigma_unif = MeanAndRMS( uniflist )
mu_sigma_gaus = MeanAndRMS( gauslist )

# Print the results. Do these values make sense?
print "For 1000 uniformely distributed numbers mu +- sigma = %5.3f +- %5.3f"%(mu_sigma_unif[0], mu_sigma_unif[1])
print "For 1000 Gaussianly distributed numbers mu +- sigma = %5.3f +- %5.3f"%(mu_sigma_gaus[0], mu_sigma_gaus[1])
print ""


# -------------------------------------------------------------------------------
# Writing and reading files
# -------------------------------------------------------------------------------

# Often you will have to read and write ascii files (i.e. human readable text files)
# Start with writing a file randomnumbers.dat containing some random numbers:

# Open 'randomnumbers.dat' in write mode.
# Only open in the block opened by the 'with ... as file' statement
with open( 'randomnumbers.dat', 'w' ) as file :

    for i in range( 100 ) :

        # Numbers distributed according to the following pdfs:
        #   uniform, gaussian, poissonian, breitwigner, landau
        outline = "%7.4f \t %7.4f %7.4f \t %7.4f \t %7.4f \n"%(r.Uniform(), r.Gaus(), r.PoissonD( 1.0 ), r.BreitWigner(), r.Landau() )

        file.write( outline )


# Now we will read the same file in again.

# Define lists that can contain the table of random numbers:
unif = []
gaus = []
pois = []
brwi = []
land = []

with open( 'randomnumbers.dat', 'r' ) as file :

    # Loop through each line in the file
    for iline in file :

        # Now we have the whole line in string format, but want it back in floating point format.
        # The command below does the following :
        # Take iline and strip it of '\n and \t' (i.e. newlines and tabulations)
        # '1.0 \t 2.0 \t 3.0 \n' -> '1.0    2.0    3.0'
        # (strip('somestring') will in general remove 'somestring' but default is '\n \t'
        # Take the result of this and split it into a list :
        # '1.0    2.0    3.0' -> ['1.0', '2.0', '3.0']
        # Take this an convert it to floating point numbers
        # ['1.0', '2.0', '3.0'] -> [1.0, 2.0, 3.0]
        format_line = [float( ientry ) for ientry in iline.strip().split() ]

        unif.append( format_line[0] )        # Now "unif" gets the first number in the line.
        gaus.append( format_line[1] )        # Now "gaus" gets the second numb...
        pois.append( format_line[2] )
        brwi.append( format_line[3] )
        land.append( format_line[4] )


# To check that the above worked, print the lines 30 to 39:
for i in range( 30, 40 ) :
    print "Random numbers : ",
    print "%8.4f \t %8.4f %8.4f \t %8.4f \t %8.4f"%(unif[i], gaus[i], pois[i], brwi[i], land[i] )
print "\n"

# Lastly create a latex table you can copy paste into your paper
# with the mean and rms of the numbers you have genereated:
mu_sigma_unif = MeanAndRMS( unif )
mu_sigma_gaus = MeanAndRMS( gaus )
mu_sigma_pois = MeanAndRMS( pois )
mu_sigma_brwi = MeanAndRMS( brwi )
mu_sigma_land = MeanAndRMS( land )

print "\\begin{tabular}{ | l | c  c |}"
print "\t \\hline"
print "\t \\multicolumn{3}{|c|}{Pdf Means and RMS}"
print "\t \\hline"
print "\t %15s & %7s & %7s\\\\"%( "pdf", "$\\mu$", "$\\sigma$" )
print "\t \\hline"
print "\t %15s & %7.3f & %7.3f \\\\"%( "Uniform"     , mu_sigma_unif[0], mu_sigma_unif[1] )
print "\t %15s & %7.3f & %7.3f \\\\"%( "Gaussian"    , mu_sigma_gaus[0], mu_sigma_gaus[1] )
print "\t %15s & %7.3f & %7.3f \\\\"%( "Poissonian"  , mu_sigma_pois[0], mu_sigma_pois[1] )
print "\t %15s & %7.3f & %7.3f \\\\"%( "Breit Wigner", mu_sigma_brwi[0], mu_sigma_brwi[1] )
print "\t %15s & %7.3f & %7.3f \\\\"%( "Landau"      , mu_sigma_land[0], mu_sigma_land[1] )
print "\t \\hline"
print "\\end{tabular}"

print ""

# Done
