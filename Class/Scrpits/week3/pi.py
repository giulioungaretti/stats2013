#!/usr/bin/env python

 
---------------------------------------------------------------------------------- 

 
ROOT macro for estimating the value of pi using a Monte Carlo 
technique.

The program picks random points in the area [-1,1] x [-1,1], and 
determines which
fraction of these are within the unit circle. This in turn gives a 
measure of pi
with associated statistical uncertainty. Performing such 
"experiments" many times
not only gives the value of pi, but also a feel for the use of Monte 
Carlo, and
experience in calculating averages, RMSs, and the error on these.

For more information see:
P. R. Bevington: page 75-78

Author: Troels C. Petersen (NBI)
Email:  petersen@nbi.dk
Date:   16th of September 2013
 
 
---------------------------------------------------------------------------------- 


from ROOT import *        # Import ROOT libraries (to use ROOT)
from array import array   # Import array for TGraphErrors...
import math               # Import MATH libraries (for extended MATH 


gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)

SavePlots = False         # Determining if plots are saved or not

r = TRandom3()

# Set parameters:
Nexperiments = 100        # Number of "experiments" determining pi
Npoints      = 1000       # Number of points per experiment in 

pi_true = 3.14159265358979323846264338328

# Make histograms:
Hist_PiDist  = TH1F("Hist_PiDist",  "Hist_PiDist",   50, 2.9, 3.4)
Hist_HitDist = TH2F("Hist_HitDist", "Hist_HitDist", 200, -1.0, 1.0, 200, 
-1.0, 1.0)




#----------------------------------------------------------------------------------- 
#
# Loop over process:
#----------------------------------------------------------------------------------- 
#

sum1 = 0.0
sum2 = 0.0

for iexp in range ( Nexperiments ) :
    Nhit = 0
    for j in range ( Npoints ) :
      
        # Get two random numbers uniformly distributed in [-1,1]:
        x1 = 2.0 * (r.Uniform() - 0.5)
        x2 = 2.0 * (r.Uniform() - 0.5)

        # Test if (x1,x2) is within unit circle:
        if (x1*x1 + x2*x2 < 1.0) : Nhit += 1

        # Plot 2D distribution of (x1,x2) for the first experiment:
        if (iexp == 0) : Hist_HitDist.Fill(x1,x2)

    
    # Calculate the fraction of points within the circle and its error:

    # From this we can get pi and its error:
    pi_estm = 0.0    # Calculate yourself!
    pi_error = 0.0   # Calculate yourself!

    # Plot these values and calculate mean and RMS:

    # Print first couple of pi measurements:
    if (iexp < 5) :
        print "  %2d. pi estimate:   %7.4f +- %6.4f"%(iexp+1, pi_estm, pi_error)


# 
#----------------------------------------------------------------------------------- 
#
# Calculate average and RMS, and print the result compared to the true  value of pi:
if (Nexperiments > 1) :
    pi_ave = 0.0    # Fill this out yourself!!!
    pi_rms = 0.0    # ...and this!

# Print how many sigmas your final result is away from the true value of    pi.
  

# 
#
# Plot the histograms:
# 

#

# Distribution of points from one experiment:
canvas1 = TCanvas("canvas1","", 80, 40, 650, 600)
Hist_HitDist.SetMarkerColor(kRed)
Hist_HitDist.SetMarkerStyle(20)
Hist_HitDist.SetMarkerSize(0.4)
Hist_HitDist.Draw()
if (SavePlots) : canvas1.SaveAs("HitDist.png")



raw_input( ' ... Press enter to exit ... ' )


# 
# #
# # 
# # First acquaint yourself with the program, and make sure that you 
# understand what the
# # parameters "Nexperiment" and "Npoints" refere to! Also, before running 
# the program,
# # calculate what precision you expect on pi, when using the number of 
# points chosen in
# # the program.
# # 
# # Then, run the program, and then take a look at the result. Did you 
# estimate match
# # the number given by the program?
# # 
# # 
# # Questions:
# # ----------
# #  1) Try to run 100 experiments with 1000 points in each. What is the 
# approximate
# #     uncertainty on pi in each experiment? Does that fit, what you 
# calculated before
# #     running the program? What is the uncertainty on the AVERAGE of all 
# 100 experiments?
# # 
# #  2) How do you expect the values of pi to distribute themselves? And 
# is this the
# #     case in reality?
# # 
# #  3) Does it make any difference on the precision of the final pi 
# value, whether
# #     you make many experiments with few points, or one experiment with 
# many points,
# #     as long as the product of Nexperiment x Npoints remains constant?
# # 
# # The following problem is the REAL question in this exercise!
# # 
# #  4) Now try to use this method in three dimensions to estimate the 
# constant in
# #     front of the r^3 expression for the volume. Do you get 3/4*pi?
# #     Increase the dimensionality (say up to 10), and see if you can 
# figure out
# #     the constants needed to calculate the hyper-volumes!
# # 
# # HINT: I'll reveal, that for Ndim of 4 and 5, the constant contains 
# pi^2 and some simple
# #       rational fraction, while for Ndim 6 and 7, it contains pi^3 and 
# a rational fraction.
#
# #
