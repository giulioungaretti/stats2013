#!/usr/bin/env python

# ----------------------------------------------------------------------------------- #
#  Python macro for testing Raphael Weldon's dices.
# ----------------------------------------------------------------------------------- #
#
#  Walter Frank Raphael Weldon DSc FRS (15 March 1860 - 13 April 1906)
#  generally called Raphael Weldon, was an English evolutionary
#  biologist and a founder of biometry. He was the joint founding
#  editor of Biometrika, with Francis Galton and Karl Pearson.
#
#  http://en.wikipedia.org/wiki/Walter_Frank_Raphael_Weldon
#
#  Weldon and his two collegues (Francis Galton and Karl Pearson) were
#  interested in statistics (to say the least!), and in order to do a
#  simple hypothesis test, Weldon rolled 12 dices 26306 times
#  (i.e. 315672 throws), which he wrote about in a letter to Galton
#  dated 2nd of February 1894 (which is how we have this data).
#
#  There were actually four data sets as follows:
#
#  I: 12 dice were rolled 26306 times, and number of 5s and 6s was
#     counted with the following result:
#  0	1	2	3	4	5	6	7	8	9	10	11	12
#  185	1149	3265	5475	6114	5194	3067	1331	403	105	14	4	0
#
#  II: 7006 of the 26306 experiments were performed by a clerk, deemed
#      by Galton to be "reliable and accurate", yielding:
#  0	1	2	3	4	5	6	7	8	9	10	11	12
#  45	327	886	1475	1571	1404	787	367	112	29	2	1	0
#
#  III: In this subset of the data, 4096 of the rolls were scrutinized
#       with only a 6 counting as a success:
#  0	1	2	3	4	5	6	7	8	9	10	11	12
#  447	1145	1181	796	380	115	24	8	0	0	0	0	0
#
#  IV: Finally, a subset of 4096 rolls were considered counting 4s, 5s
#      and 6s as successes:
#  0	1	2	3	4	5	6	7	8	9	10	11	12
#  0	7	60	198	430	731	948	847	536	257	71	11	0
#
#  References:
#    Kemp, A.W. and Kemp, C.D. (1991), "Weldon's dice data revisited",
#    American Statistician, 45, 216-222.
#
# ----------------------------------------------------------------------------------- #
#
#  Original author (C++):  Troels C. Petersen
#  Python version author:  Lars Egholm Pedersen & Troels C. Petersen
#  Email:                  egholm@nbi.dk, petersen@nbi.dk
#  Date:                   4th of September 2013
#
# ----------------------------------------------------------------------------------- #

from ROOT import *
from array import array


# ----------------------------------------------------------------------------------- #
def sqr(a):
    return a*a
# ----------------------------------------------------------------------------------- #

# Setting what to be shown in statistics box:
gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)

# Random numbers from the Mersenne-Twister:
r = TRandom3()
r.SetSeed(0)

# Settings for script:
verbose   = True
savePlots = False
Ndices   = 12;
Noutcome = 13


# ------------------------------------------------------------------ #
# Data:
# ------------------------------------------------------------------ #

sum1 = 0
data1 = [185, 1149, 3265, 5475, 6114, 5194, 3067, 1331, 403, 105, 14,  4, 0]
data2 = [ 45,  327,  886, 1475, 1571, 1404,  787,  367, 112,  29,  2,  1, 0]
data3 = [447, 1145, 1181,  796,  380,  115,   24,    8,   0,   0,  0,  0, 0]
data4 = [  0,    7,   60,  198,  430,  731,  948,  847, 536, 257, 71, 11, 0]

print "   N   data1  data2  data3  data4"
for i in range (Noutcome):
    if (verbose):
        print "  %2d:  %5d  %5d  %5d  %5d"%(i, data1[i], data2[i], data3[i], data4[i])
    sum1 += data1[i]


# ------------------------------------------------------------------ #
# Testing simple hypothesis (p_naive = 1/3):
# ------------------------------------------------------------------ #

# Make histograms with data (note the range, which is suitable for integers):
Hist_data1 = TH1F("Hist_data1", "Weldon's dices", Noutcome, -0.5, Noutcome-0.5)


# Make factorial array (which might come in handy!):
factorial = [0]*Noutcome
factorial[0] = 1.0
for i in range (1, Noutcome):
    factorial[i] = factorial[i-1] * i


# Put the data into histogram
# Note that this is NOT done with "Fill" but with "SetBinContent".
for i in range (0, Noutcome):
    Hist_data1.SetBinContent(i+1,data1[i])
    Hist_data1.SetBinError(i+1,0.0)               # You decide on errors...


# Plot histograms with data and prediction:
canvas = TCanvas("canvas", "", 50, 50, 900, 600)

# Hist_data1.SetMinimum(0.0)
Hist_data1.SetLineWidth(2)
Hist_data1.SetLineColor(kRed)
Hist_data1.Draw("e")

canvas.Update()
if (savePlots):
    canvas.SaveAs("WeldonDices_NaiveHypothesis.png")



# ----------------------------------------------------------------------------------- #
raw_input('Press Enter to exit')



# ----------------------------------------------------------------------------------- #
#
# Questions:
# ----------
# 1) Consider first just the first (and largest) dataset. Plot the data along with the
#    "naive" prediction, and calculate the Chi2. What is the probability of this Chi2
#    given the number of degrees of freedom? Is the naive p=1/3 very likely?
#
# 2) Next, consider an alternative hypothesis of a "non-naive" value of the probability
#    for a 5 or a 6, and find the optimal value of this probability by scanning through
#    the possible values and calculating the Chi2 for each of them.
#    Fitting (the minimum of) this Chi2 distribution, what is the uncertainty on this
#    probability? And how probable is the Chi2 of this new hypothesis?
#
# 3) Many of the bins don't have much data in them. Therefore, repeat the above scan,
#    but now calculating the likelihood (or rather -2*log(llh)). Does this improve the
#    measurement of the probability?
#
# 4) Do the same exercise for the other three datasets. Do they all show the same
#    behavior, and is the large statistics needed?
#
#
# Advanced questions:
# -------------------
# 1) Assuming that the dices rolled all had the same probabilities associated to each
#    value, do a "global fit" of all four datasets, finding the probabilities which
#    best explains all four datasets.
#
# ----------------------------------------------------------------------------------- #




