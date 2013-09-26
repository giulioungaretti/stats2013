#!/usr/bin/env python

# ---------------------------------------------------------------------------------- #
# 
#  ROOT macro for estimating the integral of exp(-x/3.0)*cos(x)^2 in the interval [0,inf]
#  using a combination of Transformation and Hit-and-Miss method.
#
#  Author: Troels C. Petersen (NBI)
#  Email:  petersen@nbi.dk
#  Date:   16th of September 2013
# 
# ---------------------------------------------------------------------------------- #

from ROOT import *        # Import ROOT libraries (to use ROOT)
from array import array   # Import array for TGraphErrors...
import math               # Import MATH libraries (for extended MATH functions)


gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)

SavePlots = False         # Determining if plots are saved or not

r = TRandom3()
r.SetSeed(1)

# Set parameters:
Npoints = 10000           # Number of points per experiment in determining pi

# Make histograms (obviously not out to infinity, but just a range for sanity check):
Hist_xy = TH2F("Hist_xy", "Hist_xy", 200, 0.0, 10.0, 200, 0.0, 1.0)


#----------------------------------------------------------------------------------- #
# Loop over process:
#----------------------------------------------------------------------------------- #

Nhit = 0
for i in range ( Npoints ) :
      
    # Well, the inside of the loop is up to you :-)





integral  = 0.0     # Well, put your value here
eintegral = 0.0     # ...
print "  The integral is %7.5f +- %7.5f"%(integral, eintegral)


# Distribution of (x,y) points:
canvas1 = TCanvas("canvas1","", 80, 40, 900, 600)

Hist_xy.SetMarkerColor(kRed)
Hist_xy.SetMarkerStyle(20)
Hist_xy.SetMarkerSize(0.4)
Hist_xy.Draw()

if (SavePlots) : canvas1.SaveAs("Hist_xy.png")



raw_input( ' ... Press enter to exit ... ' )

# ----------------------------------------------------------------------------------- #
# 
# The purpose of this exercise is to combine Transformation and Hit-and-Miss methods
# to evaluate an integral (here only in 1D, to make it easy/illustrative).
# 
# Questions:
# ----------
#  1) Find the integral of exp(-x/3.0)*cos(x)^2 in the interval [0,inf] using a
#     combination of the Transformation and Hit-and-Miss methods.
# 
# ----------------------------------------------------------------------------------- #
