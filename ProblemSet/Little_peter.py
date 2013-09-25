import numpy as  np
from scipy import *
from pylab import *
from scipy.misc import factorial as  factorial
from style import rstyle
matplotlib.rcParams.update({'font.size': 18})
p = 0.5  # prob of each try
n = 20  # tries 


r_int = 14  # number of success out of n tires 
r = np.linspace(0, 30)

def binominalp(n,p,r):
	binomial_factor = factorial(n) / (factorial(r) *  factorial(n-r) )
	prob20_14 = binomial_factor * p ** r * (1-p)**(n-r)
	return prob20_14



## plot the binomial for 20 coins, 14 heads
fig,ax = subplots()
ax.plot(r,binominalp(n,p,r),'-',c ='orange',label='p = %s, n = %s '%(p,n),
	linewidth = 1.5)
ax.set_xlabel('Number of success, r ')
ax.set_ylabel('P(r)')
ax.axvline(x=r_int, ls='--', c='black')
ax.axhline(y=binominalp(n,p,r_int),ls='--', c='black')
ax.text(14.2,0.045,'r = %s'%(r_int))
ax.fill_between(r,binominalp(n,p,r),where=r>r_int,color='#467821',alpha=.5)
ax.legend()
rstyle(ax)
fig.show()
fig.savefig('../Latex/fig/lil.pdf', bbox_inches='tight')
print binominalp(n,p,r_int)


## same thing for 20 coins, 18.
p = 0.5  # prob of each try
n = 20  # tries 
r_int = 18
p18 = binominalp(n,p,r_int)

n = 100
r_int = 1
r = np.linspace(0.01, 100,5000)

## plot the binomial for 20 coins, 14 heads
fig,ax = subplots()
ax.plot(r,binominalp(n,p18,r),'-',c ='#FF366D',label='p = %.6f, n = %s '%(p18,n),
	linewidth = 1.5)
ax.set_xlabel('Number of success, r ')
ax.set_ylabel('P(r)')
ax.axvline(x=r_int, ls='--', c='black')
ax.axhline(y=binominalp(n,p18,r_int),ls='--', c='black')
	# ax.text(r_int+.2,0.045,'r = %s'%(r_int))
ax.fill_between(r,binominalp(n,p18,r),where=r>r_int,color='#5FFFC2',alpha=.5)
ax.legend()
ax.set_xlim(0,1.5)
ax.set_ylim(0,0.8)
rstyle(ax)
fig.show()
fig.savefig('../Latex/fig/lil_2.pdf', bbox_inches='tight')
print binominalp(n,p18,r_int)

##3
