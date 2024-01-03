from __future__ import annotations

# this is designed to set up every notebook or executable script properly with common resources
from sys import stdout,stderr,executable,version_info
assert version_info.major>=3

from datetime import datetime
DATE_FORMAT,TIME_FORMAT='%m/%d/%Y','%H:%M:%S'
DATETIME_FORMAT=DATE_FORMAT+" "+TIME_FORMAT

def now():
    """Quickly return the time."""
    return datetime.now().strftime(TIME_FORMAT)

def nprint(*args,**kwargs):
    """Decorate the print statement with the time."""
    print(now(),*args,**kwargs)
    stdout.flush()

nprint("Starting...")

# allow code to use the SIGALARM functionality to interrupt itself in a controlled fashion
from signal import signal,SIGALRM,alarm

class Timeout(Exception):
    """Permits time limits."""
    def __str__(self):
        return "Timeout."
    
def sigalrm(x,y):
    """Handle SIGALRM by raising a Timeout exception."""
    raise Timeout
    
signal(SIGALRM,sigalrm) # register the handler

# allow deep breaks, the python break syntax can only break out one level
class Break(Exception):
    """Permits deep breaks."""
    def __str__(self):
        return "Break"
        
# passive wrapper for with clauses for objects that don't provide __enter__ and __exit__
class With:
    """Dummy for with clauses."""
    def __enter__(self):
        return self
        
    def __exit__(self,*args):
        pass
        
    def __init__(self,object=None):
        self.object=object
        
    def __call__(self):
        return self.object
        
    def __str__(self):
        return str(self.object)
        
    def __repr__(self):
        return repr(self.object)

# deal with some Google colab specific stuff
try:
    from IPython import get_ipython
    ip=get_ipython()

    if ip is not None and 'google' in str(ip):
        for package in 'yfinance','arch':
            nprint("Installing %s into Google notebook..." % package)
            ip.system("pip install %s 1>/dev/null" % package)

except ModuleNotFoundError:
    pass # if IPython not installed, we're definitely not in a notebook

from warnings import filterwarnings
filterwarnings("ignore",category=RuntimeWarning) # I don't care

# yfinance - download function
from yfinance import download

# the usual suspects
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl ; plt=pl

# some friendly numbers
zero,one,two,three,four,five,ten,hundred,thousand=0e0,1e0,2e0,3e0,4e0,5e0,1e1,1e2,1e3
half,GoldenRatio=one/two,(one+np.sqrt(five))/two

# import arch classes
from arch.univariate import ConstantMean,ARX,GeneralizedError,Normal,GARCH
from arch.typing import Float64Array

# change the constraints for GeneralizedError
class GeneralizedError2(GeneralizedError):
    """Version of the GED with bounds on fit adjusted to include all feasible distributions (GED is valid for all positive nu values)."""
    def bounds(self,*args)->list[tuple[float,float]]:
        """Revised bounds."""
        return [(0e0,1e2)]

    def constraints(self,*args)->tuple[Float64Array,Float64Array]:
        return np.array([[1], [-1]]), np.array([self.bounds()[0][0],-self.bounds()[0][1]])

# change the constraints for GARCH
class GARCH2(GARCH):
    """Version of GARCH with constraints modified to be more relaxed, leads to models that don't bind on constraints."""
    def bounds(self,resids:Float64Array)->list[tuple[float,float]]:
        """Modify bounds to be more relaxed."""
        v=float(np.mean(abs(resids)**self.power))
        bounds=[(1e-8*v,ten*v)]
        bounds.extend([(-one,two)]*(self.p+self.o+self.q))
        return bounds

    def constraints(self,*args)->tuple[Float64Array,Float64Array]:
        """Modify constraints to permit negative values for A and D etc."""
        a,b=super(GARCH2,self).constraints()
        b[1:(self.p+self.o+1)]=-one
        return a,b

# some special axis formatters for matplotlib
from matplotlib.ticker import Formatter

class DirectionalLabels(Formatter):
    """Base class to provide directional formats for matplotlib axes."""

    def __init__(self):
        """Abstract base class."""
        raise NotImplementedError("DirectionalLabels is an abstract base class. You cannot instantiate it directly.")

    def __call__(self,datum,pos=None):
        """Render the provided number as a string."""
        return self.plus.format(datum*self.scale) if datum>0e0 else self.minus.format(-datum*self.scale) if datum<0e0 else self.zero
    
class PercentLabels(DirectionalLabels):
    """Output Excel style percent labels."""
    def __init__(self,precision=2,zero="0",scale=1e0):
        """Set decimal precision and string to use for zeros."""
        self.plus="{:,.%df} %%" % precision
        self.minus="({:,.%df}) %%" % precision
        self.zero=str(zero)
        self.scale=abs(scale)
        
class CurrencyLabels(DirectionalLabels):
    """Matplotlib formatter to provide Excel type currency formats for axes."""
    def __init__(self,precision=2,zero="0",symbol="$",suffix="",scale=1e0):
        """Set decimal precision and string to use for zeros."""
        self.plus="%s {:,.%df}%s" % (symbol,precision,suffix)
        self.minus="(%s {:,.%df}%s)" % (symbol,precision,suffix)
        self.zero=str(zero)
        self.scale=abs(scale)

class CountLabels(DirectionalLabels):
    """Matplotlib formatter to provide integers with commas."""
    def __init__(self,zero="0",scale=1e0):
        """Integers with commas."""
        self.plus="{:,.0f}"
        self.minus=self.plus
        self.zero=str(zero)
        self.scale=abs(scale)

# that's all folks
nprint("Initialized.")
