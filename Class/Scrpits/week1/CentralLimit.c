// ----------------------------------------------------------------------------------- //
/*
  ROOT macro for illustration of the Central Limit Theorem.

  Random numbers from different distributions are added to a sum, and many such sums
  are plottet. As it turns out (and as dictated by the CLT), their distribution turns
  about to be Gaussian.
  The example also illutrates how widths (and therefore uncertainties) are added in
  quadrature, as one has to divide the sum by the square root of the number of random
  numbers that went into the sum in order to get a Gaussian of unit width (when using
  random numbers of unit width).

  For more information on the Central Limit Theorem, see:
    R. Barlow: page 49
    G. Cowan: page 33
    http://en.wikipedia.org/wiki/Central_limit_theorem

  Run this ROOT macro by:
    From prompt: > root -l CentralLimit.c
    Inside ROOT: > .x CentralLimit.c
  
  Result in file results.root, displayed by:
    In prompt: > root -l results.root
    Followed by (in ROOT): TBrowser a (use mouse from there)

  Author: Troels C. Petersen (NBI/CERN)
  Email:  Troels.Petersen@cern.ch
  Date:   19th of August 2012
*/
// ----------------------------------------------------------------------------------- //

#include <TFile.h>
#include <TH1F.h>
#include <TRandom3.h>



//---------------------------------------------------------------------------------- 
void CentralLimit()
//---------------------------------------------------------------------------------- 
{
  TRandom3 r;
  const int Nexperiments = 100000;                   // Number of sums produced
  const int Nuniform     = 100;                    // Number of uniform numbers used in sum
  const int Nexponential = 0;                      // Number of exponential numbers used in sum
  const int Ncauchy      = 0;                      // Number of cauchy numbers used in sum

  double pi = 3.14159265358979323846264338328;     // Selfexplanatory!!!

  bool verbose = true;                             // Print some numbers or not?
  int Nverbose = 10;                               // If so, how many?


//----------------------------------------------------------------------------------
// Make histograms (name, title, number of bins, minimum, maximum):

  TH1F *Hist_Sum         = new TH1F("Hist_Sum", "Hist_Sum", 120, -600, 600);
  TH1F *Hist_Uniform     = new TH1F("Hist_Uniform", "Hist_Uniform", 240, -600, 600);
  TH1F *Hist_Exponential = new TH1F("Hist_Exponential", "Hist_Exponential", 240, -6.0, 6.0);
  TH1F *Hist_Cauchy      = new TH1F("Hist_Cauchy", "Hist_Cauchy", 240, -6.0, 6.0);


//----------------------------------------------------------------------------------
// Loop over process:
//----------------------------------------------------------------------------------

  for (int iexp = 0; iexp < Nexperiments; iexp++) {
    double sum = 0.0;

    // Generating uniform numbers (with mean 0, and RMS of 1):
    for (int i = 0; i < Nuniform; i++) {
      double x = sqrt(12.0) * (r.Uniform() - 0.5);        // Uniform between +-sqrt(3)
      sum += x;
      Hist_Uniform->Fill(x);
      // if ((verbose) && (iexp < 1) && (i < Nverbose)) printf("  Uniform:     %7.4f \n", x);
    }

    // Generating exponential numbers (with mean 0, and RMS of 1):
    for (int i = 0; i < Nexponential; i++) {
      double x = -log(r.Uniform()) - 1.0;                // Exponential starting at -1
      sum += x;
      Hist_Exponential->Fill(x);
      //if ((verbose) && (iexp < 1) && (i < Nverbose)) printf("  Exponential: %7.4f \n", x);
    }

    // Generating numbers according to a Cauchy distribution (1 / (1 + x^2)):
    for (int i = 0; i < Ncauchy; i++) {
      double x = tan(pi * (r.Uniform() - 0.5));          // Cauchy with mean 0
      sum += x;
      Hist_Cauchy->Fill(x);
      //if ((verbose) && (iexp < 1) && (i < Nverbose)) printf("  Cauchy:      %7.4f \n", x);
    }
    sum = sum / sqrt(double(Nuniform + Nexponential + Ncauchy));
    Hist_Sum->Fill(sum);
  }

// Hist_Sum->Draw() ;
Hist_Uniform->Draw() ;

//---------------------------------------------------------------------------------- 
// Write histograms to file:
//---------------------------------------------------------------------------------- 
  // TFile *file = new TFile("results.root", "RECREATE", "Histograms");

//   Hist_Sum->Write();
//   Hist_Uniform->Write();
//   Hist_Exponential->Write();
//   Hist_Cauchy->Write();

//   file->Write();
//   file->Close();

}


//---------------------------------------------------------------------------------- 
/*

First acquaint yourself with the program, and make sure that you understand what the
Central Limit Theorem states. Do you understand why the uniform distribution needs to
go from +-sqrt(3) in order to give a distribution with a width of one (i.e. unit) and
why you subtract one from the exponential distribution (and how this works at all)?

Then try to see what the result of adding 100 uniform random numbers is? Which
distribution does it give (surprice!!!), and how well does it resemble it? Try for
example to fit this distribution with a Gaussian (in ROOT, right click on the line
of the distribution, and select "FitPanel" in which you set the function to be a
"gaus").


Questions:
----------
 1) Using the sum of 10 uniform random numbers with mean 0 and width 1,
    what is the probability of obtaining a number beyond 3 sigma?
    What would you expect from a true Gaussian distribution?
    And what about the same question for 4 sigma?

 2) Why do the Cauchy distribution "ruin" the Gaussian distribution?
    And is this in conflict with the Central Limit Theorem?

 3) If the original distributions which are added into a sum did not have a mean
    of zero and unit width, but instead each had a different mean and width, what
    would be the result be? Would the Central Limit Theorem still apply? And what
    would the width of the resulting distribution be?

 4) Which of the three random distributions has a sum, which converges
    fastest to a Gaussian?
    Which distribution would in general converge fastest?


Advanced questions:
-------------------
 1) If one used a trunkated mean (throwing away the top and bottom 10%),
    will the mean of 1000 Cauchy numbers then converge?

 2) How few/many uniform random numbers needs to be added, before the probability
    for the sum to follow a Gaussian distribution is greater than 1% (on average)
    when using 1000 sums (i.e. Nexperiments = 1000)?

 3) Try to add a triangular PDF, which again has mean 0 and width 1.
    By which method(s) is this possible?

*/
//---------------------------------------------------------------------------------- 
