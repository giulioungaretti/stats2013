#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
# 
#   ROOT macro for fitting points with errors to a user defined function.
# 
#   This ROOT macro illustrates the use of ChiSquare as a goodness-of-fit measure, how
#   this distribution comes about, and that it actually works! At the same time, it is
#   also an illustration of how to do a linear fit analytically, that is without running
#   the ROOT fitting algorithm (called Minuit).
# 
#   References:
#     Barlow: Chapter 6
#     Cowan: Chapter 2.7, Chapter 7
#     Bevington: Chapter 6
# 
#   Author: Troels C. Petersen (CERN)
#   Email:  petersen@nbi.dk
#   Date:   9th of September 2013
#
#   Author: Lars Egholm Pedersen (NBI/CERN)
#   Email:  egholm@cern.ch
# 
# ----------------------------------------------------------------------------------- #

from ROOT import *
from array import array
from math import sqrt

# ----------------------------------------------------------------------------------- #
def sqr( a ) : 
    return a*a
# ----------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------- #
# Chi Squared Test
# ----------------------------------------------------------------------------------- #

gROOT.Reset()

# Setting of general plotting style:
gStyle.SetCanvasColor(0)
gStyle.SetFillColor(0)

# Settings for statistics box:
gStyle.SetOptStat(1111)
gStyle.SetOptFit(1111)

# Random numbers from the Mersenne-Twister:
r = TRandom3()
r.SetSeed(1)    # Initializing the random numbers using 1 as seed. Put "0" to use the time (i.e. random)!

# Text to write on the plot:
text = TLatex()
text.SetNDC()
text.SetTextFont(1)
text.SetTextColor(1)


# ------------------------------------------------------------------ #
# Define Histograms:
# ------------------------------------------------------------------ #

# How does the fitted values come out:
Hist_alpha0 = TH1F("Hist_alpha0", "Hist_alpha0", 80,  0.0,  8.0)
Hist_alpha1 = TH1F("Hist_alpha1", "Hist_alpha1", 80, -0.25, 1.35)

# How does the Chi-square and probability come out:
Hist_Chi2   = TH1F("Hist_Chi2",   "Hist_Chi2",   20,  0.0, 20.0)
Hist_Prob   = TH1F("Hist_Prob",   "Hist_Prob",   20,  0.0,  1.0)



# ------------------------------------------------------------------ #
# Loop over generating and fitting data:
# ------------------------------------------------------------------ #

Nexp = 1000
Npoints = 9
x  = array( 'f', [0.0]*Npoints )   # Create an array of length Npoints with zeros.
ex = array( 'f', [0.0]*Npoints )   # [X]*N is just a python syntax to initialize
y  = array( 'f', [0.0]*Npoints )   # a list of values X.
ey = array( 'f', [0.0]*Npoints )   

alpha0 = 3.6
alpha1 = 0.3
# alpha2 = 0.1
sigmay = 1.0

for iexp in range( Nexp ) : 

    # Generate data:
    # --------------
    for i in range( Npoints ) : 

      x[i]  = float( i+1 )
      ex[i] = 0.0
      y[i]  = alpha0 + alpha1 * x[i] + r.Gaus( 0.0 ,sigmay )
      # y[i]  = alpha0 + alpha1 * x[i] + alpha2 * x[i]*x[i] + r.Gaus(0.0,sigmay)
      ey[i] = sigmay


    # ----------------------
    # Fit data analytically:
    # ----------------------
    # The linear fit can be done analytically, as is outlined here
    # (link at the bottom of course webpage):
    #   http://www.nbi.dk/~petersen/Teaching/Stat2013/StraightLineFit.pdf

    # Define the sums needed for the calculation:
    s   = 0.0
    sx  = 0.0
    sxx = 0.0
    sy  = 0.0
    sxy = 0.0

    # Loop over data to calculate relevant sums:
    for i in range( Npoints ) : 
      s   += 1.0
      sx  += x[i]
      sxx += sqr(x[i])
      sy  += y[i]
      sxy += x[i] * y[i]

    # Use sums in calculations:
    Delta = sxx * s - sqr(sx)
    alpha0_calc = (sy  * sxx - sxy * sx) / Delta
    alpha1_calc = (sxy * s   - sy  * sx) / Delta
    sigma_alpha0_calc = sigmay * sqrt(sxx / Delta)
    sigma_alpha1_calc = sigmay * sqrt(s   / Delta)

    # So now you have data points and a fit/theory. How to get the fit quality?
    # The answer is to calculate the Chi2 and Ndof, and from them get their
    # probability using a function (e.g. from ROOT):
    Chi2_calc = 0.0
    for i in range( Npoints ) : 
      fit_value = alpha0_calc + alpha1_calc * x[i]
      Chi2_calc += sqr((y[i] - fit_value) / ey[i])

    Nvar = 2                     # Number of variables (alpha0 and alpha1)
    Ndof_calc = Npoints - Nvar   # Number of degrees of freedom

    # From Chi2 and Ndof, one can calculate the probability of obtaining this
    # or something worse (i.e. higher Chi2). This is a good function to have!
    Prob_calc = TMath.Prob( Chi2_calc, Ndof_calc )


    # -----------------------------------------
    # Fit data numerically (i.e. using Minuit):
    # -----------------------------------------
    # This is the same fit, but now done numerically and iteratively by Minuit in ROOT:
    # It is shorter, but a lot slower!
    graph = TGraphErrors( Npoints,x,y,ex,ey )
    fit   = TF1("fit", "[0] + [1]*x", 0.5, float( Npoints )+0.5 )
    graph.Fit("fit","RQ")               # The "Q" option means "Quiet", i.e. don't print or plot anything!

    alpha0_fit = fit.GetParameter(0)
    alpha1_fit = fit.GetParameter(1)
    sigma_alpha0_fit = fit.GetParError(0)
    sigma_alpha1_fit = fit.GetParError(1)

    # In ROOT, you can just ask the fit function for it:
    Chi2_fit = fit.GetChisquare()
    Ndof_fit = fit.GetNDF()
    Prob_fit = fit.GetProb()

    # Let us see, if the calculated and the fitted values agree:
    if iexp < 25 : 
      print "  Calc:%6.3f+-%5.3f  %5.3f+-%5.3f   p=%6.4f    Fit:%6.3f+-%5.3f  %5.3f+-%5.3f   p=%6.4f"%(alpha0_calc , sigma_alpha0_calc ,  
                                                                                                       alpha1_calc , sigma_alpha1_calc , 
                                                                                                       Prob_calc,
                                                                                                       alpha0_fit  , sigma_alpha0_fit  ,
                                                                                                       alpha1_fit  , sigma_alpha1_fit  ,
                                                                                                       Prob_fit )

    # Fill histograms with fit results:
    Hist_alpha0.Fill(alpha0_calc)
    Hist_alpha1.Fill(alpha1_calc)
    
    Hist_Chi2.Fill(Chi2_fit)
    Hist_Prob.Fill(Prob_fit)



# ------------------------------------------------------------------ #
# Fit the data and plot the result:
# ------------------------------------------------------------------ #

# Make a white canvas and draw the example fit in:
c0 = TCanvas("c0","",100,20,600,450)
c0.SetFillColor(0)

graph.SetLineWidth(2)
graph.SetMarkerStyle(20)
graph.SetMarkerColor(2)
graph.Draw("AP")


# If there have been more than one experiment, then make another white canvas:
if Nexp > 1 : 
    c1 = TCanvas("c1","",150,50,1200,700)
    c1.SetFillColor(0)
    c1.Divide(2,2)             # Divide the canvas into 2-by-2 subcanvas
 
    c1.cd(1)                   # Go to the first subcanvas
    Hist_alpha0.Draw()

    c1.cd(2)                   # Go to the second subcanvas (surprise!)
    Hist_alpha1.Draw()
    
    c1.cd(3)
    Hist_Chi2.Sumw2()
    Hist_Chi2.DrawNormalized("e")   # Here I draw it normalized, so that the function will match!
    f1a = TF1("f1a","ROOT::Math::chisquared_pdf(x,7)", 0, 20)     # Define a function that is the Chi-square with Ndof=7
    f1a.Draw("same")                # Draw it on top of the histogram.

    # Text:
    text.SetTextSize(0.06)          # Put some text in the plot too.
    text.DrawLatex(0.20, 0.16, "NOTE: This is not a fit!")
    
    c1.cd(4)
    Hist_Prob.SetMinimum(0.0)
    Hist_Prob.Draw("e")

    # Save to file:
    c1.Update()
    c1.SaveAs("FitChi2dist.pdf")

raw_input( ' ... Press enter to exit ... ' )



#---------------------------------------------------------------------------------- 
# 
# Make sure you've read the relevant references and that you understand not only what
# the ChiSquare is, but also that it follows the ChiSquare distribution, and that the
# probability of obtaining such a ChiSquare or worse can be calculated from it.
# 
# The program generates a certain number of datasets, each consisting of 9 points along
# a line. These are then fitted (both analytically and numerically), and the result and
# the Chi2 of the fit is recorded along with the probability of the fit.
# 
# 
# Questions:
# ----------
#  1) Run the code such that it does exactly one fit, and take a look at the line fitted.
#     Does this look reasonable, and what is the chance that the input for the data could
#     actually be from a flat distribution?
# 
#  2) Does the fit reproduce the input numbers well (include the uncertainties in your
#     answer)? And do the analytical result(s) agree with the numerical one(s)?
# 
#  3) Now increase the number of experiments to e.g. 1000, and rerun the macro. Figure
#     out what you see in the window split in 2-by-2, and go through each of these to
#     see, if you understand every feature of the distributions shown, and if you are
#     happy with them!
#     This somehow makes this the "long" question without any leading questions, but
#     you should by now be statistically minded enough to know what to look for, at
#     least to some degree :-)
# 
#  4) Investigate if the distributions of probabilities is flat, or if it has some
#     slope to it. Do you understand why the distributions of probabilities is flat?
# 
#  5) Find the line where the random points for the line are generated, and add a
#     quadratic term in x with the coefficient 0.1. Run the program again with Nexp=1,
#     and start by looking at the single fit in the graph. Can you see this change?
#     Now run 1000 experiments again, and see what has changed in the distributions
#     in the 2-by-2 window when including such a term, and think what consequences
#     it might have for an experiment.
# 
# 
# Advanced questions:
# -------------------
#  1) Change the coefficient from question 5) to -0.2. Of course the linear fit does
#     not do very well. What changes are needed for the fit to be good again? Make
#     these changes, and see that the condition in question 4) is again met.
# 
#  2) On page 104 Glen Cowan lists the conditions under which the ChiSquare distribution
#     is obtained (hypothesis is linear in fit parameters). Try to make a test, where
#     this is not the case (e.g. f(x) = cos(a*x)), and see to what degree this requirement
#     is actually needed.
# 
# 
#---------------------------------------------------------------------------------- 




