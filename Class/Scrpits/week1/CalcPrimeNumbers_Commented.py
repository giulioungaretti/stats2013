#!/usr/bin/env python

# --------------------------------------------------------- #
#  Simple python script to calculate prime numbers!
#   
#  Author: Troels C. Petersen (Niels Bohr Institute)
#  Date:   27-06-2013
#
#  Run by: ./CalcPrimeNumbers_Commented.py
# --------------------------------------------------------- #

from ROOT import *        # Import ROOT libraries (to use ROOT)
import math               # Import MATH libraries (for extended MATH functions)

Nmax = 10000              # Maximum prime number
N    = 2                  # Starting value

SavePlots = True         # Determining if plots are saved or not

# Setting what to be shown in statistics box:
gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)

# Define a histogram.
# In Python one does not need to state the type of anything,
# so when writing "hist_prime = ..." it will simply take on
# the type of what comes after.
# TH1D is a ROOT object: They always start with "T", and the "H1"
# means 1D histogram, while "D" referes to "double" (i.e. numbers
# with digits!)
# After giving it a name and a title (here the same), one defines
# the number of bins, and the starting and ending of the range.
hist_prime = TH1D("hist_prime", "Prime number distribution", 100, 0.0, Nmax)


# --------------------------------------------------------- #
# Calculate prime numbers:
# --------------------------------------------------------- #

# Calculating prime numbers comes down to taking a number (here N),
# and testing if it is prime by dividing it by all numbers up the
# the square root of it. If no number divides N (tested using the 
# "%" operator, which returns the remainder: 6%3 = 0, 5%2 = 1, etc.),
# then N is prime!

# See if you can follow this in python program form below. There 
# are only 8 lines in total!


# While-loop, which loops as long as the statement is true.
# It is true to begin with (N=2, Nmax = 10000), but at some point
# N will have increased beyond Nmax, and the looping stops.
while (N < Nmax):
    hit = 0                    # Define a variable "hit", with starting value 0.

    # For-loop, which lets "i" have values from 2 to the integer value
    # of the square root of N, rounded up ("int" rounds down, hence "+1").
    for i in range (2,int(sqrt(N))+1):

        if (N%i == 0):         # If the remainder of the integer division is 0, hit = 1
            hit = 1
                               # The end of the indention closes the for-loop!

    if (hit == 0):             # If no number gave a perfect integer division (i.e. with remainder 0)...
        hist_prime.Fill(N)     # the it is a prime number. Fill it into the histogram.
    N += 1                     # Increase N by one.


# This algorithm gives the prime numbers up to Nmax = 10000!
# Think it through, and see if you understand it...


# --------------------------------------------------------- #
# Draw output:
# --------------------------------------------------------- #

# Define a "canvas", i.e. a new window on the screen.
# This is again a ROOT thing (hence the "T" in TCanvas),
# and you give it name, title, x-position, y-position, x-size and y-size
canvas = TCanvas( "canvas", "canvas", 50, 50, 1200, 600 )

hist_prime.GetXaxis().SetRangeUser(0, Nmax)         # From the histogram, we get the x-axis, and set the range.
hist_prime.SetMinimum(0)                            # We also set the minimum.
hist_prime.GetXaxis().SetTitle("Prime number")      # We give the x-axis a label.
hist_prime.GetYaxis().SetTitle("Frequency")         # We give the y-axis a label.

hist_prime.SetMarkerColor(kBlue)                    # Set the histogram marker color to blue.
hist_prime.SetMarkerStyle(20)                       # Set the histogram marker style to filled circles.
# How could you know that 20 is filled circles? Well, ROOT is well documented and quite used,
# so if you write "setmarkerstyle" in Google, the first hit is: http://root.cern.ch/root/html/TAttMarker.html
# Here, you can find all the options, details, etc.

# The Prime Number Theorem (http://en.wikipedia.org/wiki/Prime_number_theorem) states,
# that the number of prime numbers follows roughly the function f(x) = 1/ln(x).

# We have binned our prime numbers (see histogram definition at the top), so we
# must have a function with a few more degrees of freedom: f(x) = a + b/ln(x),
# where a and b are constants that needs to be fitted.

# We define a function in ROOT as shown below. "T" from ROOT and "F1" is 1D function.
# Again it has a name (chosen to be the same as the function name), and then one has to
# specify the function expression, where "[0]" and "[1]" are constants and "log" is the
# natural logarithm (log10 is the base 10 logarithm). Finally, it needs a range, which is [0,N].
fit_prime = TF1("fit_prime", "[0] + [1]/log(x)", 0, N)
fit_prime.SetParameters(0.0, 10.0)         # Set the starting values of [0] and [1] to 0 and 10.
fit_prime.SetLineColor(kRed)               # Set the line color to red.
fit_prime.SetLineWidth(4)                  # Set tne line width to 4.

# So now we ask that the histogram is fitted by the fitting function.
# The options "L" is for Likelihood fit (ChiSquare is defalt)
hist_prime.Fit("fit_prime", "L")

# Draw the histogram with the option "e" for showing the errors in the plot.
hist_prime.Draw("e")

# Put a legend on the plot:
# The name is not surprisingly "TLegend", and one specifies the four corners:
leg = TLegend( 0.25, 0.73, 0.60, 0.88 )
leg.SetFillColor(kWhite);                  # Let the fill color be white
leg.SetLineColor(kWhite);                  # Let the edge be white (i.e. no edge)
leg.AddEntry(hist_prime, " Prime number distribution", "P")       # Histogram represented by a point "P"
leg.AddEntry(fit_prime,  " Prime number fit result", "L")         # Fit function represented by a line "L"
leg.Draw()                                 # Draw the legend

if (SavePlots):
    canvas.SaveAs("test.png")              # Save plot as "test.png" (format follow extension name)

# Finally, ensure that the program does not termine (and the plot disappears), before you press enter:
raw_input('Press Enter to exit')
