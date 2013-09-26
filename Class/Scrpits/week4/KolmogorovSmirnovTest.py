#!/usr/bin/env python
#
# ----------------------------------------------------------------------------------- #
#
#  Python macro for illustrating test statistics among them the Kolmogorov-Smirnov test.
#
#  The Kolmogorov-Smirnov test (KS-test) is a general test for two distributions in 1D
#  are the same. This program applies both a binned and an unbinned KS test, and compares
#  it to a Chi2 test and a simple comparison of means.
#
#  References:
#    http://en.wikipedia.org/wiki/Kolmogorov-Smirnov_test
#
#  Author: Troels C. Petersen (NBI)
#  Email:  petersen@nbi.dk
#  Date:   23rd of September 2013
#
# ----------------------------------------------------------------------------------- #

from ROOT import *
from array import array


# ----------------------------------------------------------------------------------- #
def sqr(a) : return a*a
# ----------------------------------------------------------------------------------- #

# Setting what to be shown in statistics box:
gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)

# Random numbers from the Mersenne-Twister:
r = TRandom3()
r.SetSeed(0)

verbose = True


# ----------------------------------------------------------------------------------- #
# Make Histograms:
# ----------------------------------------------------------------------------------- #

# Resulting p-values for each test (means, Chi-Squared binned, KS binned, KS unbinned):
Hist_ProbMu  = TH1F("Hist_ProbMu",  "Hist_ProbMu",   50,  0.0, 1.0)
Hist_ProbCSb = TH1F("Hist_ProbCSb", "Hist_ProbCSb",  50,  0.0, 1.0)
Hist_ProbKSb = TH1F("Hist_ProbKSb", "Hist_ProbKSb",  50,  0.0, 1.0)
Hist_ProbKS  = TH1F("Hist_ProbKS" , "Hist_ProbKS",   50,  0.0, 1.0)


# ----------------------------------------------------------------------------------- #
# Generate and fit data:
# ----------------------------------------------------------------------------------- #

# How many experiments, and how many events in each:
Nexp = 1
Nevents = 1000

# Define the two Gaussians to be generated:
dist_meanA  =  0.0
dist_widthA =  1.0
dist_meanB  =  0.0
dist_widthB =  1.0


# Two distributions to be compared:
Hist_gaussA  = TH1F("Hist_gaussA", "Hist_gaussA",  100, -5.0, 5.0)
Hist_gaussB  = TH1F("Hist_gaussB", "Hist_gaussB",  100, -5.0, 5.0)


for iexp in range (Nexp) :

    x_gaussA = []
    x_gaussB = []

    sumA = [0.0, 0.0, 0.0]
    sumB = [0.0, 0.0, 0.0]

    # Make empty arrays:
    x_gaussA_array = array( 'd' ) 
    x_gaussB_array = array( 'd' ) 


    # Generate data:
    # --------------
    for i in range (Nevents) :
        xA = r.Gaus(dist_meanA, dist_widthA)
        sumA[1] += xA
        sumA[2] += xA*xA
        x_gaussA_array.append(xA)
        Hist_gaussA.Fill(xA)
    
        xB = r.Gaus(dist_meanB, dist_widthB)
        sumB[1] += xB
        sumB[2] += xB*xB
        x_gaussB_array.append(xB)
        Hist_gaussB.Fill(xB)


    # Test distributions:
    # -------------------

    # Test mean and width:
    meanA = sumA[1] / float(Nevents)
    widthA = sqrt(sumA[2] / float(Nevents) - meanA*meanA)
    meanB = sumB[1] / float(Nevents)
    widthB = sqrt(sumB[2] / float(Nevents) - meanB*meanB)
    dMean = meanA - meanB
    dMeanError = sqrt(sqr(widthA)/float(Nevents) + sqr(widthB)/float(Nevents))
    pMean = TMath.Erfc(dMean / dMeanError / sqrt(2.0)) / 2.0        # Turn a number of sigmas into a probability!
    Hist_ProbMu.Fill(pMean)

    # Binned Chi2 and Kolmogorov-Smirnov Test:
    # (see options at http://root.cern.ch/root/html/TH1.html#TH1:KolmogorovTest):
    pCSbinned = Hist_gaussA.Chi2Test(Hist_gaussB, "UU")
    pKSbinned = Hist_gaussA.KolmogorovTest(Hist_gaussB, "UU")
    Hist_ProbCSb.Fill(pCSbinned)
    Hist_ProbKSb.Fill(pKSbinned)

    # Unbinned Kolmogorov-Smirnov Test (requires sorting):
    x_gaussA_array = array('d', sorted(x_gaussA_array))
    x_gaussB_array = array('d', sorted(x_gaussB_array))

    # Make Kolmogorov test with unbinned data in two sorted arrays:
    pKS = TMath.KolmogorovTest(Nevents, x_gaussA_array, Nevents, x_gaussB_array, "")
    Hist_ProbKS.Fill(pKS)

    if (verbose and iexp < 10) :
      print " %4d:  pMean: %6.4f   pCSbinned: %6.4f   pKSbinned: %6.4f   pKS: %6.4f"%(iexp, pMean, pCSbinned, pKSbinned, pKS)

    if (Nexp > 1) :
        Hist_gaussA.Reset("ICE")
        Hist_gaussB.Reset("ICE")

    else :
        # Make a white canvas and plot the two distributions:
        c0 = TCanvas("c0","",120,20,900,600)
        c0.SetFillColor(0)
        
        Hist_gaussA.SetLineWidth(2)
        Hist_gaussA.SetLineColor(2)
        Hist_gaussA.Draw()
        
        Hist_gaussB.SetLineWidth(2)
        Hist_gaussB.SetLineColor(4)
        Hist_gaussB.Draw("same")


# ------------------------------------------------------------------ #
# Show the distribution of fitting results:
# ------------------------------------------------------------------ #

# Make a white canvas divided into four regions:
c1 = TCanvas("c1","",150,70,500,700)
c1.SetFillColor(0)
c1.Divide(1,4)
    
c1.cd(1)
Hist_ProbMu.SetMinimum(0.0)
Hist_ProbMu.SetLineWidth(2)
Hist_ProbMu.SetLineColor(4)
Hist_ProbMu.Draw()
    
c1.cd(2)
Hist_ProbCSb.SetMinimum(0.0)
Hist_ProbCSb.SetLineWidth(2)
Hist_ProbCSb.SetLineColor(4)
Hist_ProbCSb.Draw()
    
c1.cd(3)
Hist_ProbKSb.SetMinimum(0.0)
Hist_ProbKSb.SetLineWidth(2)
Hist_ProbKSb.SetLineColor(4)
Hist_ProbKSb.Draw()
    
c1.cd(4)
Hist_ProbKS.SetMinimum(0.0)
Hist_ProbKS.SetLineWidth(2)
Hist_ProbKS.SetLineColor(4)
Hist_ProbKS.Draw()
    
c1.Update()
# c1.SaveAs("TestDist.eps")



# ---------------------------------------------------------------------------------- 
raw_input('Press Enter to exit')

# ---------------------------------------------------------------------------------- 
# 
# Questions:
# ----------
#  1) First run the program to display the two distributions A and B, when
#     - They are the same.
#     - The mean of A is increased.
#     - The width of A is enlarged.
#     Get a feel for how much you need to change the distribution, before you can
#     by eye see that they are not the same.
#     Could you for the test of the means have calculated this? Do so, and see if
#     it somewhat matches you number from above!
# 
#  2) Now run the tests 100 times, where A and B are unit Gaussians and thus identical.
#     How should the distributions of the test probabilities come out? And is this the
#     case?
# 
#  3) Repeat the changes in question 1), and see which tests "reacts" most to these
#     modifications.
#     How much of a change in the mean is required for 95% of the tests (of each kind)
#     to give a probability below 5%? How much is required for the width?
# 
#  4) Obviously, the test of the means is not sensitive the a change in the width.
#     Make such a test yourself by calculating the widths and the uncertainty on the
#     widths (or perhaps try the F-test!).
#     Note that in a (unit) Gaussian the uncertainty on the width is of the same order
#     as that of the means! That is generally good to know :-)
# 
#  5) Try to test different distributions than the Gaussian one (e.g. exponential,
#     binomial, etc.), and see how the tests performs.
# 
# NOTE: The unbinned Kolmogorov-Smirnov test has the great advantage that it can handle
#       ANY distribution (even the Cauchy distribution - remind yourself of that one!).
#       The reason is, that it doesn't care about how far out an outlier is.
#     
# Advanced questions:
# -------------------
#  1) Implement in ROOT the following tests:
#      - Lilliefors test
#      - Shapiro-Wilk test
#      - Anderson-Darling test
#      - Cramer-von-Mises test
#      - Jarque-Bera test
#      - Kuiper's test
#      - Mann-Whitney-Wilcoxon test
#      - Siegel-Tukey test
#     and quantify under various conditions the power of each and the correlation
#     among them. Write it up, and send it to a statistics journal. :-)
# 
# ---------------------------------------------------------------------------------- 




