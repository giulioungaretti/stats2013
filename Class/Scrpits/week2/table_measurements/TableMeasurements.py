#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#
#   Python program for analysing measurements of the length of the lecture table in
#   Auditorium A at NBI.
# 
#   There are two measurements each with estimated error of the table length:
#     1: Measurement with a 30cm ruler.
#     2: Measurement with a 2m folding ruler.
# 
#   Each person was asked not only to state the measurement, but also their estimated
#   uncertainty. None of the persons could see others measurements in order to get the
#   largest degree of independence. Also, the 30cm ruler measurement was asked to be
#   done first.
# 
#   Author: Troels C. Petersen (NBI)
#   Email:  petersen@nbi.dk
#   Date:   4th of September 2012
#
#   Author: Lars Egholm Pedersen (NBI/CERN)
#   Email:  egholm@cern.ch
#
# ----------------------------------------------------------------------------------- #

from ROOT import *
import os, math

# Set the showing of statistics and fitting results (0 means off, 1 means on):
gStyle.SetOptStat("emr");   # See http://root.cern.ch/root/html/TStyle.html#TStyle:SetOptStat
gStyle.SetOptFit(1111);     # See http://root.cern.ch/root/html/TStyle.html#TStyle:SetOptFit

SavePlots = False


# Define two histograms with the lengths recorded and the correlation between length residual and uncertainty:
Hist_L30cm = TH1F("Hist_L30cm", "Lengths estimates by 30cm ruler",      250, 0.0, 5.0);
Hist_30cm_RvsE  = TH2F("Hist_30cm_LvsE",   "Length residual vs. uncertainty estimates", 250, 0.0, 0.05, 250, 0.0, 0.05);


# Define lists to contain the measurements, such that you can easily loop over them later!
L30cm = []
eL30cm = []
L2m = []
eL2m = []

# Define sums, from which the mean and RMS can be calculated:
sum0 = 0.0
sum1 = 0.0
sum2 = 0.0

files = ["data_TableMeasurements2009.txt", "data_TableMeasurements2010.txt", "data_TableMeasurements2011.txt", "data_TableMeasurements2012.txt", "data_TableMeasurements2013.txt"]

# Loop over files and open them
for file in files :
    with open( file, 'r' ) as f : 

        # Read and ignore header lines:
        header1 = f.readline()
        header2 = f.readline()

        # Loop over lines and extract variables of interest
        for line in f:
            line = line.strip()
            columns = line.split()
            if (len(columns) == 4) :
                L30cm.append(float(columns[0]))
                eL30cm.append(float(columns[1]))
                L2m.append(float(columns[2]))
                eL2m.append(float(columns[3]))        
                print "  Measurement %3d:   L(30cmR): %6.3f +- %6.3f m      L(2mFR): %6.3f +- %6.3f m"%(int(sum0), L30cm[-1], eL30cm[-1], L2m[-1], eL2m[-1])

                Hist_L30cm.Fill(L30cm[-1])
                Hist_30cm_RvsE.Fill(fabs(L30cm[-1]-3.360), eL30cm[-1])

                sum0 += 1
                sum1 += L30cm[-1]
                sum2 += L30cm[-1]*L30cm[-1]

    f.close()



# ----------------------------------------------------------------------------------- #
# Calculate mean, RMS and from that error on the mean:

sum1 = sum1/sum0                           # Calculate the mean
sum2 = sqrt(sum2/(sum0-1.0) - sum1*sum1)   # Calculate the RMS (remember: RMS = sqrt(<sum_x^2> - <sum_x>^2))
esum1 = sum2 / sqrt(sum0)                  # Uncertainty of the mean is RMS / sqrt(N)

# This is the "naive" mean, in that it simply uses all measurements without any inspection.
print "  Mean = %6.4f +- %6.4f      RMS = %6.4f"%(sum1, esum1, sum2)


# ----------------------------------------------------------------------------------- #
# Plot histogram on the screen in one canvas:

# canvas = TCanvas( "canvas", "canvas", 50, 50, 1200, 600 )

# Set all the trimmings for the histogram plotting:
Hist_L30cm.GetXaxis().SetRangeUser(0.0, 5.0)       # From the histogram, we get the x-axis, and set the range.
Hist_L30cm.SetMinimum(0)                           # We also set the minimum.
Hist_L30cm.GetXaxis().SetTitle("Table length (m)") # We give the x-axis a label.
Hist_L30cm.GetYaxis().SetTitle("Frequency")        # We give the y-axis a label.
Hist_L30cm.SetLineColor(kBlue)                     # Set the histogram line color to blue.
Hist_L30cm.SetLineWidth(2)                         # Set the histogram line width to two.

# Define a resonable fitting function:
fit_L30cm = TF1("fit_L30cm", "gaus", 0.0, 5.0)     # Define a (predefined) Gaussian fitting function.
fit_L30cm.SetLineColor(kRed)                       # Set the line color to red.
fit_L30cm.SetLineWidth(2)                          # Set tne line width to 2.

# Fit the histogram (with a likelihood function in the range the function is defined in):
# Hist_L30cm.Fit("fit_L30cm", "LR")                  # Note the two options: L for Likelihood and R for Range.
# Hist_L30cm.Draw()                                  # Draw the histogram

# if (SavePlots):
#    canvas.SaveAs("TableMeasurements_30cmRuler.png")      # Save plot (format follow extension name)

# ----------------------------------------------------------------------------------- #
raw_input('Press Enter to exit')



# ----------------------------------------------------------------------------------- #
#
# Start by taking a close look at the data, first by inspecting the numbers in the data
# file, and then by considering the histograms produced by running the macro.
# 
# To begin with, only consider the 30cm ruler measurements from 2013, and disregard the
# estimated/guessed uncertainties. You can then expand from there, as guided below with
# questions.
# 
# Questions:
# ----------
#  1) Consider the calculated mean and width, and make sure that you understand how
#     they were performed. Is the result as you would expect it? And do you think that
#     it is close to the best possible (i.e. most precise) result?
# 
#  2) Do any of the measurements looks wrong/bad/suspecious? Do you see any repeated
#     mistakes done? Would you correct or exclude any of the measurements and how would
#     you justify this?
#     If so, make sure that your program does this, and recalculate the result (with sums).
#     Also, fit the length measurements with a Gaussian distribution. Should the binning
#     be changed for these fits? And is the Gaussian distribution justified?
#
#  3) Write the number of measurements you accepted for the length determination along
#     with your result (mean and error on mean) into the questionaire.
#
# You should at least reach this point in the exercise! And preferably much further!!!
# Of the questions below, you should perhaps focus mostly on 5, 6 and 7.
#
#  4) (Slightly difficult question)
#     Is there any correlation between the errors on the measurements and the actual
#     distance to the mean (this is called the "residual")? That is, do the errors
#     contain useful information, that should be used in the calculation of the most
#     accurate estimate of the mean? 
#     In all simplicity - did those who had a measurement close to the mean also put down a
#     small uncertainty? What is the correlation between residuals and the uncertainties?
#     Yes, define new sums as discussed in the lectures, and calculate the correlation!
#
#  5) Compare the size of the residuals with the size of the uncertainties. Were people too
#     optimistic or too pesimistic (or were the uncertainty estimates/guesses good)?
#
#  6) Whether or not you found a large enough correlation above, try to calculate the
#     weighted mean. Do you need to discard more dubious measurements? Did the result
#     improve? Do you trust this result more?
# 
#  7) Repeat the above questions for the 2m folding rule.
# 
#  8) How much did the single measurement uncertainty go down from the 30cm ruler case
#     to the 2m folding rule? Can you quantify how much better the 2m folding rule is?
# 
# 
# Advanced questions:
# -------------------
#  1) Does the length of the table seems to be different when measured with a 30cm and a 2m
#     ruler? Quantify this statement! I.e. what is the difference, and what is the
#     uncertainty on that difference? Is this significantly away from 0? How big an
#     effect on the 30cm ruler would this correspond to?
# 
#  2) If you were asked for the best estimate of the length of the table, what would
#     you do? (If posssible, read Bevington page 58 bottom!)
# 
# 
#
#---------------------------------------------------------------------------------- 
