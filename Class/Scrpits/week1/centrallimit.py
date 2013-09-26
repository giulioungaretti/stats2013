#!/usr/bin/env python

# ----------------------------------------------------------------------------------- 
#
#  ROOT macro for illustration of the Central Limit Theorem.
#
#  Random numbers from different distributions are added to a sum, and many such sums
#  are plottet. As it turns out (and as dictated by the CLT), their distribution turns
#  about to be Gaussian.
#  The example also illutrates how widths (and therefore uncertainties) are added in
#  quadrature, as one has to divide the sum by the square root of the number of random
#  numbers that went into the sum in order to get a Gaussian of unit width (when using
#  random numbers of unit width).
#
#  For more information on the Central Limit Theorem, see:
#    R. Barlow: page 49
#    G. Cowan: page 33
#    http://en.wikipedia.org/wiki/Central_limit_theorem
#
#  Run this pyROOT macro by:
#    From prompt: > ./central_limit.py
#  
#  Result in file results.root, displayed by:
#    In prompt: > root -l results.root
#    Followed by (in ROOT): TBrowser a (use mouse from there)
#
#  Author: Troels C. Petersen (NBI/CERN)
#  Email:  petersen@nbi.dk
#  Date:   31st of August, 2013
#
#  Author: Lars Egholm Pedersen (NBI/CERN)
#  Email:  egholm@cern.ch
#  Date:   -----------------------------
#
#
#  ----------------------------------------------------------------------------------- //

from ROOT import TRandom3
import math

r = TRandom3()                        #Random generator
Nexperiments = 1000                   # Number of sums produced
Nuniform     = 10                     # Number of uniform numbers used in sum
Nexponential = 0                      # Number of exponential numbers used in sum
Ncauchy      = 0                      # Number of cauchy numbers used in sum

pi = 3.14159265358979323846264338328  # Selfexplanatory!!!

verbose = True                        # Print some numbers or not?
Nverbose = 10                         # If so, how many?

SavePlots = True


#----------------------------------------------------------------------------------
# Make histograms (name, title, number of bins, minimum, maximum):

Hist_Sum         = TH1F("Hist_Sum"        , "Hist_Sum"        , 120, -6.0, 6.0)
Hist_Uniform     = TH1F("Hist_Uniform"    , "Hist_Uniform"    , 240, -6.0, 6.0)
Hist_Exponential = TH1F("Hist_Exponential", "Hist_Exponential", 240, -6.0, 6.0)
Hist_Cauchy      = TH1F("Hist_Cauchy"     , "Hist_Cauchy"     , 240, -6.0, 6.0)

#----------------------------------------------------------------------------------
# Loop over process:
#----------------------------------------------------------------------------------

for iexp in range( Nexperiments ) : 

    if iexp % 100 == 0 : print "At iexp : ", iexp

    sum = 0.0
    
    # Generating uniform numbers (with mean 0, and RMS of 1):
    for i in range( Nuniform ) : 

        x = math.sqrt(12.0) * (r.Uniform() - 0.5)        # Uniform between +-sqrt(3)
        sum += x
        Hist_Uniform.Fill(x)

        if verbose and iexp == 0 and i < Nverbose : print "   Uniform:     %7.4f"%x


    # Generating exponential numbers (with mean 0, and RMS of 1):
    for i in range( Nexponential ) : 

        x = -math.log( r.Uniform() ) - 1.0                # Exponential starting at -1
        sum += x
        Hist_Exponential.Fill(x)

        if verbose and iexp == 0 and i < Nverbose : print "   Exponential: %7.4f"%x

    # Generating numbers according to a Cauchy distribution (1 / (1 + x^2)):
    for i in range( Ncauchy ) : 

      x = math.tan(pi * (r.Uniform() - 0.5))              # Cauchy with mean 0
      sum += x
      Hist_Cauchy.Fill(x)

      if verbose and iexp == 0 and i < Nverbose : print "   Cauchy       : %7.4f"%x

    
    sum = sum / math.sqrt( Nuniform + Nexponential + Ncauchy )
    Hist_Sum.Fill(sum)


#---------------------------------------------------------------------------------- 
# Draw output plots with corresponding fits to the screen:
#---------------------------------------------------------------------------------- 

# Define a "canvas", i.e. a new window on the screen.
# This is again a ROOT thing (hence the "T" in TCanvas),
# and you give it name, title, x-position, y-position, x-size and y-size
canvas = TCanvas( "canvas", "canvas", 50, 50, 1200, 600 )

Hist_Sum.GetXaxis().SetRangeUser(-7.0, 7.0)       # From the histogram, we get the x-axis, and set the range.
Hist_Sum.SetMinimum(0)                            # We also set the minimum.
Hist_Sum.GetXaxis().SetTitle("Prime number")      # We give the x-axis a label.
Hist_Sum.GetYaxis().SetTitle("Frequency")         # We give the y-axis a label.

Hist_Sum.SetMarkerColor(kBlue)                    # Set the histogram marker color to blue.
Hist_Sum.SetMarkerStyle(20)                       # Set the histogram marker style to filled circles.
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
fit_Sum = TF1("fit_Sum", "gaus", -5.0, 5.0)
fit_Sum.SetParameters(0.0, 10.0)         # Set the starting values of [0] and [1] to 0 and 10.
fit_Sum.SetLineColor(kRed)               # Set the line color to red.
fit_Sum.SetLineWidth(4)                  # Set tne line width to 4.

# So now we ask that the histogram is fitted by the fitting function.
# The options "L" is for Likelihood fit (ChiSquare is defalt)
Hist_Sum.Fit("fit_Sum", "L")

# Draw the histogram with the option "e" for showing the errors in the plot.
Hist_Sum.Draw("e")

if (SavePlots):
    canvas.SaveAs("Plot_CentralLimit.png")      # Save plot (format follow extension name)




#---------------------------------------------------------------------------------- 
# Write histograms to file:
#---------------------------------------------------------------------------------- 
outfile = TFile("results.root", "RECREATE", "Histograms")

Hist_Sum.Write()
Hist_Uniform.Write()
Hist_Exponential.Write()
Hist_Cauchy.Write()

outfile.Write()
outfile.Close()


# Finally, ensure that the program does not termine (and the plot disappears), before you press enter:
raw_input('Press Enter to exit')


# ---------------------------------------------------------------------------------- 
# 
# 
# First acquaint yourself with the program, and make sure that you understand what the
# Central Limit Theorem states. Do you understand why the uniform distribution needs to
# go from +-sqrt(3) in order to give a distribution with a width of one (i.e. unit) and
# why you subtract one from the exponential distribution (and how this works at all)?
# 
# Then try to see what the result of adding 100 uniform random numbers is? Which
# distribution does it give (surprice!!!), and how well does it resemble it? Try for
# example to fit this distribution with a Gaussian (in ROOT, right click on the line
# of the distribution, and select "FitPanel" in which you set the function to be a
# "gaus").
# 
# 
# Questions:
# ----------
#  1) Using the sum of 10 uniform random numbers with mean 0 and width 1,
#     what is the probability of obtaining a number beyond 3 sigma?
#     What would you expect from a true Gaussian distribution?
#     And what about the same question for 4 sigma?
# 
#  2) Why do the Cauchy distribution "ruin" the Gaussian distribution?
#     And is this in conflict with the Central Limit Theorem?
# 
#  3) If the original distributions which are added into a sum did not have a mean
#     of zero and unit width, but instead each had a different mean and width, what
#     would be the result be? Would the Central Limit Theorem still apply? And what
#     would the width of the resulting distribution be?
# 
#  4) Which of the three random distributions has a sum, which converges
#     fastest to a Gaussian?
#     Which distribution would in general converge fastest?
# 
# 
# Advanced questions:
# -------------------
#  1) If one used a trunkated mean (throwing away the top and bottom 10%),
#     will the mean of 1000 Cauchy numbers then converge?
# 
#  2) How few/many uniform random numbers needs to be added, before the probability
#     for the sum to follow a Gaussian distribution is greater than 1% (on average)
#     when using 1000 sums (i.e. Nexperiments = 1000)?
# 
#  3) Try to add a triangular PDF, which again has mean 0 and width 1.
#     By which method(s) is this possible?
# 
# 
# ---------------------------------------------------------------------------------- 