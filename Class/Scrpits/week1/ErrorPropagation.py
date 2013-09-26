#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
# 
#   ROOT macro for illustrating error propagation using random Gaussian numbers.
# 
#   The example is based on first doing the error propagation analytically, and then
#   verifying it by running a so-called Monte-Carlo (MC) program.
# 

#   For more information on error propagation, see:
#     R. J. Barlow: page 48-61 
#     P. R. Bevington: page 36-48
# 
#   Author: Troels C. Petersen (NBI)
#   Email:  petersen@nbi.dk
#   Date:   6th of September 2012
#
#  Author: Lars Egholm Pedersen (NBI/CERN)
#  Email:  egholm@cern.ch
#  Date:   -----------------------------
# 
# ----------------------------------------------------------------------------------- #

from ROOT import *
from math import sqrt, atan, sin, cos

#---------------------------------------------------------------------------------- 

def sqr( a ) : 
    return a*a

#---------------------------------------------------------------------------------- 
# Error propagation
#---------------------------------------------------------------------------------- 

# Setting of general plotting style:
gStyle.SetCanvasColor(0)
gStyle.SetFillColor(0)
# Setting what to be shown in statistics box:
gStyle.SetOptStat(1110)   # Print for stat: Entries, Mean, and RMS
gStyle.SetOptFit(1111)    # Print for fit:  Everything!


# Set parameters:
Nexp = 10000           # Number of experiments
pi = 3.14159265358979323846264338328

r = TRandom3()

# Make histograms (all 1D):
Hist_x1 = TH1F( "Hist_x1", "Hist_x1", 100,  0.0,  5.0 )
Hist_x2 = TH1F( "Hist_x2", "Hist_x2", 100,  0.0,  2.0 )
Hist_y  = TH1F( "Hist_y",  "Hist_y",  200,  0.0, 12.0 )


#----------------------------------------------------------------------------------
# Loop over process:
#----------------------------------------------------------------------------------

mu1   =  3.5
sig1  =  0.4
mu2   =  0.8
sig2  =  0.2
rho12 =  0.0            # Correlation parameter!

if rho12 < -1.0 or rho12 > 1.0 : 
    print "ERROR: Correlation factor not in interval [-1,1], as it is %6.2f"%rho12
    exit
    
# Transform to correlated random numbers (see Barlow page 42-44):
#Note that the absolute value is taken before the square root to avoid sqrt(-x).
theta = 0.5 * atan( 2.0 * rho12 * sig1 * sig2 / ( sqr(sig1) - sqr(sig2) ) )
sigu = sqrt( fabs( (sqr(sig1*cos(theta)) - sqr(sig2*sin(theta)) ) / ( sqr(cos(theta)) - sqr(sin(theta))) ) )
sigv = sqrt( fabs( (sqr(sig2*cos(theta)) - sqr(sig1*sin(theta)) ) / ( sqr(cos(theta)) - sqr(sin(theta))) ) )


#----------------------------------------------------------------------------------
# Loop over process:
#----------------------------------------------------------------------------------

for i in range( Nexp ) : 

    # Get (uncorrelated) random Gaussian numbers u and v:
    u = r.Gaus( 0.0, sigu )
    v = r.Gaus( 0.0, sigv )

    # Transform into (possibly) correlated random Gaussian numbers x1 and x2:
    x1 = mu1 + cos(theta)*u - sin(theta)*v
    x2 = mu2 + sin(theta)*u + cos(theta)*v
    Hist_x1.Fill(x1)
    Hist_x2.Fill(x2)

    # Calculate y (circumference, area or diagonal):
    y = x1 - x2    # Just nonsense formula! Write the appropriate formula yourself!
    Hist_y.Fill(y)

    if i < 5 : print "Gaussian:  x1 = %4.2f    x2 = %4.2f   ->   y =%5.2f"%( x1, x2, y )


#---------------------------------------------------------------------------------- 
# Plot histograms on screen:
#---------------------------------------------------------------------------------- 

# Making a new window (canvas):
# --------------------------------------------------------------------
c0 = TCanvas("c0", "", 100, 20, 800, 600)
# c0.SetLogy()

# Setting line width and color of histograms:
Hist_y.SetLineWidth(2)
Hist_y.SetLineColor(4)

# Fitting histogram with Gaussian:
fitGauss = TF1("fitGauss","gaus", 0.0, 12.0)
Hist_y.Fit("fitGauss", "l")

# Drawing histograms with errors in the same plot:
Hist_y.Draw("e")

c0.Update()
# c0.SaveAs("Dist_ErrorProp.png")

raw_input( ' ... Press enter to exit ... ' )


#---------------------------------------------------------------------------------- 
# 
# 
# Questions:
# ----------
# 1) A class of students estimate by eye, that the length of the table in Auditorium A
#    is L = 3.5+-0.4m, and that the width is W = 0.8+-0.2m.
# 
#    Assuming that there is no correlation between these two measurements, calculate
#    ANALYTICALLY what the circumference, area, and diagonal length is including
#    (propagated) uncertainties.
#    Repeat the calculation, given that the correlation is rho(L,W) = 0.5.
# 
# 
# 2) Now look at the program, and assure yourself that you understand what is going on.
#    Put in the correct expression for y in terms of x1 and x2 in order to calculate the
#    circumference, area, and diagonal length, and run the program.
#    Does the output correspond well to the results you expected from calculations in 1)?
# 
# 
# 3) Imagine that you wanted to know the central value and uncertainty of:
#      y = log(sqr(x1*tan(x2))+sqrt(abs(x1-x2)/(cos(x2)+1.0+x1)))
#    Get the central value of y, and see if you can quickly differentiate this with
#    respect to x1 and x2, and thus predict what uncertainty to expect for y using
#    the error propagation formula. It is (for once) OK to give up :-)
#    Next, try to estimate the central value and uncertainty using random numbers
#    like above - do you trust this result?
# 
# 
# Advanced questions:
# -------------------
#  1) Try to generate x1 and x2 with a quadratic correlation, and see that despite
#     not having any linear correlation, the result on circumference, area, and diagonal
#     length is still affected.
# 
# 
#---------------------------------------------------------------------------------- 
