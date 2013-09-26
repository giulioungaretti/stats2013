#!/usr/bin/env python

# ---------------------------------------------------------------------------------- #
# 
#   ROOT macro for illustrating a likelihood fit.
# 
#   The example uses as default 100 exponentially distributed random times, with the goal
#   of finding the best estimate of the lifetime, tau = 1. Four estimates are considered:
#    - Mean
#    - Chi-square fit (chi2)
#    - Binned Likelihood fit (bllh)
#    - Unbinned Likelihood fit (ullh)
# 
#   While the mean can be simply calculated, the three other methods are based on a scan
#   of values for tau in the range [0.5, 2.0]. For each value of tau, the chi2, bllh, and
#   llh are calculated (in the two likelihood cases, it is actually -2*log(likelihood)
#   which is calculated).
# 
#   This is both an exercise, but also an attempt to illustrate four things:
#    - How to make a (binned and unbinned) Likelihood function (and fit).
#    - The difference and a comparison between a Chi-square and a (binned) Likelihood.
#    - The difference and a comparison between a binned and unbinned Likelihood.
#    - What goes on behind the scenes in ROOT, when it is asked to fit something.
# 
# 
#   Author: Troels C. Petersen (NBI)
#   Email:  petersen@nbi.dk
#   Date:   14th of September 2013
# 
# ---------------------------------------------------------------------------------- #

from ROOT import *        # Import ROOT libraries (to use ROOT)
from array import array   # Import array for TGraphErrors...
import math               # Import MATH libraries (for extended MATH functions)

SavePlots = False         # Determining if plots are saved or not

gStyle.SetOptStat("emr")
gStyle.SetOptFit(1111)


# ---------------------------------------------------------------------------------- #
def sqr(a) : return a*a


# ---------------------------------------------------------------------------------- #
# Parabola:
# Note that the parabola is defined slightly differently. The Parameters are:
#   par[0]: Minimum value (i.e. constant)
#   par[1]: Minimum position (i.e. x of minimum)
#   par[2]: Quadratic term.
# ---------------------------------------------------------------------------------- #
def func_para(x, par) :
    return par[0] + par[2]*sqr(x[0]-par[1])



# ---------------------------------------------------------------------------------- #
# Double parabola with different slopes on each side of the minimum:
# Parameters are as follows:
#   par[0]: Minimum value (i.e. constant)
#   par[1]: Minimum position (i.e. x of minimum)
#   par[2]: Quadratic term on lower side
#   par[3]: Quadratic term on higher side
# ---------------------------------------------------------------------------------- #
def func_asympara(x, par) :
    if (x[0] < par[1]) :
        return par[0] + par[2]*sqr(x[0]-par[1])
    else :
        return par[0] + par[3]*sqr(x[0]-par[1])




# ---------------------------------------------------------------------------------- #
# Likelihood program:
# ---------------------------------------------------------------------------------- #

# Parameters of the problem:
Ntimes = 100;          # Number of time measurements (IMPORTANT NOTE: If you change this, you
                       # also need to change the normalization in the fit functions - lines 280's).
tau_truth = 1.0;       # We choose (like Gods!) the lifetime.
t = []                 # List of times

verbose = False        # Should the program print (a lot) or not? (true/false)
r = TRandom3()         # Random numbers
r.SetSeed(11)          # We set the numbers to be random, but the same for all

Nbin_exp = 50          # Number of bins in histogram
tmax = 10.0            # Maximum time in histogram
dt = tmax / Nbin_exp   # Time step
Hist_Exp = TH1F("Hist_Exp", "Hist_Exp", Nbin_exp, 0.0, tmax)


# ------------------------------------
# Generate data:
# ------------------------------------
sum1 = 0.0
sum2 = 0.0

for i in range (Ntimes) :
    t.append(r.Exp(tau_truth))                   # Exponential with lifetime tau.
    Hist_Exp.Fill(t[i])
    sum1 += t[i]
    sum2 += t[i]*t[i]
    if (verbose) : print "  %5.2f,", t[i]
if (verbose) : print "\n\n"

mean = sum1 / Ntimes
rms  = sqrt(sum2/Ntimes - mean*mean)
emean = rms / sqrt(Ntimes)
print "  Mean of %d time measurements is:  mu = %6.4f +- %6.4f"%(Ntimes, mean, emean)


# ------------------------------------
# Analyse data:
# ------------------------------------

# Define the number of tau values and their range to test in Chi2 and LLH:
# (As we know the "truth", namely tau = 1, the range [0.5, 2.0] seems fitting
# for the mean. The number of bins can be increased at will...)
Ntau = 150
min_tau = 0.5
max_tau = 2.0
delta_tau = (max_tau-min_tau) / Ntau

# Define histograms to contain the calculated Chi2 and LLHs:
# Hist_chi2 = TH1F("Hist_chi2", "Hist_chi2", Ntau+1, min_tau-delta_tau/2.0, max_tau-delta_tau/2.0)
# Hist_bllh = TH1F("Hist_bllh", "Hist_bllh", Ntau+1, min_tau-delta_tau/2.0, max_tau-delta_tau/2.0)
# Hist_ullh = TH1F("Hist_ullh", "Hist_ullh", Ntau+1, min_tau-delta_tau/2.0, max_tau-delta_tau/2.0)


# Loop over hypothesis for the value of tau and calculate Chi2 and LLH:
# ---------------------------------------------------------------------
chi2_minval = 999999.0
chi2_minpos = 0.0
bllh_minval = 999999.0
bllh_minpos = 0.0
ullh_minval = 999999.0
ullh_minpos = 0.0

tau  = array( 'f', [0.0]*(Ntau+1) )
chi2 = array( 'f', [0.0]*(Ntau+1) )
bllh = array( 'f', [0.0]*(Ntau+1) )
ullh = array( 'f', [0.0]*(Ntau+1) )

# Now loop of POSSIBLE tau estimates:
for itau in range (Ntau+1) :
    tau_hypo = min_tau + itau*delta_tau   # Scan in values of tau
    tau[itau] = tau_hypo

    # Calculate Chi2 and binned likelihood (from loop over bins in histogram):
    chi2[itau] = 0.0
    bllh[itau] = 0.0
    for ibin in range ( 1, Nbin_exp) :
        # Note: The number of EXPECTED events is the intergral over the bin!
        xlow_bin = Hist_Exp.GetBinCenter(ibin) - dt/2.0
        xhigh_bin = Hist_Exp.GetBinCenter(ibin) + dt/2.0
        nexp = Ntimes * (exp(-xlow_bin/tau_hypo) - exp(-xhigh_bin/tau_hypo))
        nobs = Hist_Exp.GetBinContent(ibin)

        chi2[itau] += sqr(nobs-nexp) / nexp                        # Chi2 summation/function
        bllh[itau] += -2.0*log(TMath.Poisson(int(nobs), nexp))     # Binned LLH function
    

    # Calculate Unbinned likelihood (from loop over events):
    ullh[itau]  = 0.0
    for iev in range ( Ntimes ) :
        ullh[itau] += -2.0*log(1.0/tau_hypo*exp(-t[iev]/tau_hypo))   # Unbinned LLH function
    
    if (verbose) :
        print " %3d:  tau = %4.2f   chi2 = %6.2f   log(bllh) = %6.2f   log(ullh) = %6.2f"%(itau, tau_hypo, chi2[itau], bllh[itau], ullh[itau])

    # Search for minimum values of chi2, bllh, and ullh:
    if (chi2[itau] < chi2_minval) :
        chi2_minval = chi2[itau]
        chi2_minpos = tau_hypo
    if (bllh[itau] < bllh_minval) :
        bllh_minval = bllh[itau]
        bllh_minpos = tau_hypo
    if (ullh[itau] < ullh_minval) :
        ullh_minval = ullh[itau]
        ullh_minpos = tau_hypo
  

print "  Minimum found:   chi2 = %7.4f    bllh = %7.4f    ullh = %7.4f"%(chi2_minpos, bllh_minpos, ullh_minpos)



# ------------------------------------
# Plot and fit results:
# ------------------------------------

# ChiSquare:
# ----------
c_chi2 = TCanvas("c_chi2","",80,40,600,450)
graph_chi2 = TGraphErrors(Ntau+1, tau, chi2)
fit_chi2 = TF1("fit_chi2", func_asympara, chi2_minpos - 0.20, chi2_minpos + 0.30, 4)
fit_chi2.SetParameters(chi2_minval, chi2_minpos, 20.0, 20.0)
fit_chi2.SetLineColor(4)
graph_chi2.SetMaximum(200.0)
graph_chi2.SetMarkerStyle(20)
graph_chi2.SetMarkerSize(0.4)
graph_chi2.Fit("fit_chi2","R")
graph_chi2.Draw("AP")

# Draw lines corresponding to minimum Chi2 and minimum Chi2+1, and draw errors:
minval = fit_chi2.GetParameter(0)
minpos = fit_chi2.GetParameter(1)
err_lower = 1.0 / sqrt(fit_chi2.GetParameter(2))
err_upper = 1.0 / sqrt(fit_chi2.GetParameter(3))

line_min = TLine(chi2_minpos - 0.30, minval, chi2_minpos + 0.30, minval)
line_min.Draw()
line_min1 = TLine(chi2_minpos - 0.30, minval+1.0, chi2_minpos + 0.30, minval+1.0)
line_min1.Draw()
line_low = TLine(minpos-err_lower, minval+1.0, minpos-err_lower, minval-2.0)
line_low.Draw()
line_upp = TLine(minpos+err_upper, minval+1.0, minpos+err_upper, minval-2.0)
line_upp.Draw()

print "  Chi2 fit gives:    tau = %6.4f + %6.4f - %6.4f"%(minpos, err_lower, err_upper)


# Go through tau values to find minimum and +-1 sigma:
# This assumes knowing the minimum value, and Chi2s above Chi2_min+1
if (((chi2[0] - chi2_minval) > 1.0) and ((chi2[Ntau] - chi2_minval) > 1.0)) :
    found_lower = False
    found_upper = False
    for itau in range (Ntau+1) :
        if ((not found_lower) and ((chi2[itau] - chi2_minval) < 1.0)) :
            tau_lower = tau[itau]
            found_lower = True
      
        if ((found_lower) and (not found_upper) and ((chi2[itau] - chi2_minval) > 1.0)) :
            tau_upper = tau[itau]
            found_upper = True
      
    
    print "  Chi2 scan gives:   tau = %6.4f + %6.4f - %6.4f"%(chi2_minpos, chi2_minpos-tau_lower, tau_upper-chi2_minpos)
else :
    print "Error: Chi2 values do not fulfill requirements for finding minimum and errors!"
  

c_chi2.Update()
# c_chi2.SaveAs("FitMinimum_chi2.png")



# Binned Likelihood:
# ------------------
c_bllh = TCanvas("c_bllh","",110,60,600,450)
graph_bllh = TGraphErrors(Ntau+1, tau, bllh)
fit_bllh = TF1("fit_bllh", func_asympara, bllh_minpos - 0.20, bllh_minpos + 0.20, 4)
fit_bllh.SetParameters(bllh_minval, bllh_minpos, 20.0, 20.0)
fit_bllh.SetLineColor(4)
graph_bllh.SetMarkerStyle(20)
graph_bllh.SetMarkerSize(0.4)
graph_bllh.Fit("fit_bllh","R")
graph_bllh.Draw("AP")

c_bllh.Update()
# c_bllh.SaveAs("FitMinimum_bllh.png")



# Unbinned Likelihood:
# --------------------
c_ullh = TCanvas("c_ullh","",140,80,600,450)
graph_ullh = TGraphErrors(Ntau+1, tau, ullh)
fit_ullh = TF1("fit_ullh", func_asympara, ullh_minpos - 0.20, ullh_minpos + 0.20, 4)
fit_ullh.SetParameters(ullh_minval, ullh_minpos, 20.0, 20.0)
fit_ullh.SetLineColor(4)
graph_ullh.SetMarkerStyle(20)
graph_ullh.SetMarkerSize(0.4)
graph_ullh.Fit("fit_ullh","R")
graph_ullh.Draw("AP")

c_ullh.Update()
# c_ullh.SaveAs("FitMinimum_ullh.png")







# Fit the data using ROOT (both chi2 and binned likelihood fits):
c1 = TCanvas("c1","",180,110,600,450)

Hist_Exp.SetXTitle("Lifetime [s]")
Hist_Exp.SetYTitle("Frequency [ev/0.1s]")

# Note this fitting function:
# I do NOT leave a constant for the normalization, and therefore have to put
# it in correctly.
rootfit_chi2 = TF1("rootfit_chi2", "100.0 * 0.20 / [0] * exp(-x/[0])", 0.0, 10.0)
rootfit_chi2.SetParameter(0, 1.0)
rootfit_chi2.SetLineColor(4)
Hist_Exp.Fit("rootfit_chi2","RE")

rootfit_bllh = TF1("rootfit_bllh", "100.0 * 0.20 / [0] * exp(-x/[0])", 0.0, 10.0)
rootfit_bllh.SetParameter(0, 1.0)
rootfit_bllh.SetLineColor(2)
Hist_Exp.Fit("rootfit_bllh","RLE+")

c1.Update()
# c1.SaveAs("GraphFitted.png")



raw_input( ' ... Press enter to exit ... ' )


# ---------------------------------------------------------------------------------- #
# 
# Make sure that you understand how the likelihood is different from the ChiSquare,
# and how the binned likelihood is different from the unbinned. If you don't do it,
# this exercise, much of the course and statistics in general will be a bit lost on
# you! :-)
# 
# The binned likelihood resembels the ChiSquare, only the evaluation in each bin is
# a bit different, especially if the number of events in the bin is low, as the PDF
# considered (Poisson for the LLH, Gaussian for the ChiSquare) is then very different.
# 
# 
# Questions:
# ----------
# 1) Try to increase the number of exponential numbers you consider to say 10000,
#    and see if the errors become more symetric. Perhaps you will have to also
#    increase the number of points you calculate the chi2/bllh/ullh (or decrease
#    the range you search!), and remember to change the normalization in the final
#    fits!
# 
# 2) Try to decrease the number of exponential numbers you consider to say 20,
#    and see that things get even worse. The difference between chi2 and llh is
#    quite significant.
# 
# 3) Make a loop over the production of random data, and try to see, if you can
#    spot the general trends. Is the Chi2 always lower or higher than the (B/U)LLH?
#    Is the error averagely smaller? Are any of the estimators biased?
# 
# 4) Make a copy of the program and put in a different PDF (i.e. not the exponential).
#    Run it, and see if the errors are still asymetric. For the function, try either
#    e.g. a Uniform or a Gaussian.
#    NOTE: If you want to try other more complex functions, then the method
#          "TH1::FillRandom" might come in handy! Look it up! We'll get to this.
# 
# ---------------------------------------------------------------------------------- #
