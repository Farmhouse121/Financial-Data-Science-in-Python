# Financial Data Science in Python
This GitHub repository
https://github.com/Farmhouse121/Financial-Data-Science-in-Python
collects the scripts and notebooks required to reproduce my published work. This includes both the articles that I have written in _Willmott_ magazine and my forthcoming book, which will also be titled _Financial Data Science in Python_.

I will be featuring _mostly_ notebooks prepared for the Google _colab_ system, although I **strongly** reccommend using a more "procedural" workflow than most notebook users adopt. For analytical work it is important that the _internal state_ of the analytical system in use be _well known_ when an _inferential procedure_ is executed. Notebooks tend to encourage a "spaghetti" workflow that is not conducive to the internal state being well known. It is my intention that the notebooks, therefore, always be executed _from the beginning to the end_ in one session. Breaking the work into "cells" is provided for narrative convenience only.

## my_library.py
A key file for all of my work will be the `my_library.py` _mini-package_. I write "mini" because it's simply a file, and it does not provide a novel software suite. It just imports most of the stuff I always import and provides a few, key, custom writtent extensions and utilities. That file will exist here, in the top level of this repository, and every independent analysis will sit in a folder below. When imaged onto a computer (with `git clone https://github.com/Farmhouse121/Financial-Data-Science-in-Python.git`, for example) each subfolder should _symlink_ to the parent version. On Unix systems, this is done via the command line with `ln -s ../my_library.py` from within the sub-folder, although `git` should copy all of those links automatically. (On Windows systems there is the `mklink my_library.py ..\my_library.py` command that can be used to execute this functionality in the shell, although I don't have a windows machine and haven't tried that personally.)

To run this file from within a Python script, just include the line 
```
from my_library import *
``` 
at the beginning. This will produce an identical internal state to having pasted all of the included code into a single file or cell and then executed it.

### Changes and Idiosyncracies
All of the scripts are going to include useage of four "standard" packages, and three are imported wholly in `my_library.py`.

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl ; plt=pl
```

I know that `pyplot` is usually imported as `plt`, not `pl` as I have, but I use it so much that having a two-letter namespace prefix is worthwhile to me and it's my computer, I get to chose the abstractions I like. For those who wish to follow the conventional usage, I have aliased it to `plt`. Feel free to use either prefix -- it's your computer -- and if you wish to "take back" the variable `pl`, Python will let you do that too. 

For the record, I am also going to invoke `matplotlib` _mostly_ via the construct

```
figure,plot=pl.subplots(figsize=(ten*GoldenRatio,ten))
```

You will find the _friendly numbers_ `ten` and `GoldenRatio` defined to their correct values inside `my_library.py`. My experience with numerical computation, over many years, in many languages and on many platforms, has taught me that typing one of `10`, `10.`, and `10e0` **will not guarantee** that you end up with the same IEEE floating point number stored in a CPU register on your computer. My assignment `ten=10e0` and usage as just `ten` guarantees that I will always get the same number. You may not find this particularly important immediately, but you will as soon as you try to represent `one/ten` in binary on any computer of your choice.

Also, I'm using `figure,plot` not `fig,ax` in my code. I like _long descriptive names_ and these describe what I am making: a figure that contains a plot. (An axe is something that I use to split wood but, earlier in my career, it represented the bonds that a trading desk wanted to sell, occasionally _desperately_.)

### Statsmodels
I will use `statsmodels` as my primary inference engine, but will not usually import the entire package into the namespace. I _really_ try to decrease namespace pollution where ever possible! Estimation is optimization of statistical models with inference about the presented results. The chain of actions --  modeling, estimation, inference -- represents empirical science. Mere optimization, such as that provided by `scikit.learn`, _without inference_ is not science. It is not merely necessary to know which set of parameters, whether latent, explicit or "hyper," give the best performance of your system _in sample_, we also need to know, or have some indication of, whether the selected performance differs significantly from that accessible by chance. What `statsmodels` does is the _hard work_ of adding the metrics of statistical inference to the output of optimization. I value that greatly.

### arch
I'm going to use Kevin Sheppard's `arch` package as well, with some modifications to lessen the bounds on various regressions. This is an excellent and useful tool, although I feel Dr. Sheppard has erred in doing things like excluding the Laplace distribution via parametric constraints, etc. After a brief discussion with him, I follow his recommended path of deriving new versions of his classes `GeneralizedError` and `GARCH`, which I call `GeneralizedError2` and `GARCH2` (somewhat unoriginally). These are defined within `my_library.py`.

### scipy
I'm going to use code from `scipy`, mostly `scipy.stats` and, occasionally, `scipy.optimize` directly (rather than via `statsmodels` or `arch`). I use the distributions and tests from `scipy.stats`, but often find that they have annoyingly short or annoyingly long names. Thus you will see things like:
```
from scipy.stats import t as density
```
and
```
from scipy.stats import scipy.stats.ttest_1samp as ttest
```
**I** would much rather import only the functions I need, rather the entire package, or give my self the ability to switch distributions easily, in later code...
```
#from scipy.stats import t as density
from scipy.stats import norm as density
```
etc.

### nprint
I find that, in notebooks, knowing _when_ code executed is so useful that attaching times to print statements is very useful. Thus `my_library.py` includes the following function definitions:
```
from datetime import datetime ; date_format,time_format="%Y-%m-%d","%H:%M:%S" ; datetime_format=date_format+" "+time_format

def now():
    """Quickly return the time."""
    return datetime.now().strftime(time_format)

def nprint(*args,**kwargs):
    """Decorate the print statement with the time."""
    print(now(),*args,**kwargs)
    stdout.flush()
```
To use it, use `nprint` as you would `print`. e.g.
```
nprint("Hello world!")
```
should output:

![image](https://github.com/Farmhouse121/Financial-Data-Science-in-Python/assets/469106/f111b0ec-57e8-4acf-b97d-0b838ee13170)

## The Articles
This repository is going to include all of the code supporting the new book I am writing, _Financial Data Science in Python_. **But**, I am also going to be writing on Medium at [https://medium.com/@stattrader](https://medium.com/@stattrader). I will include links to each article _and_ the relevant folder within this repository below. Since this `README` is fairly long, it will also serve as the first article.

| Title | GitHub | Medium |
|-------|--------|--------|
| Financial Data Science in Python | [README](https://github.com/Farmhouse121/Financial-Data-Science-in-Python/README.md) | [Financial Data Science in Python](https://stattrader.medium.com/financial-data-science-in-python-ee66dab460cf) |
| The Market's Not Normal: Part 1 | [The_Market's_Not_Normal.ipynb](https://github.com/Farmhouse121/Financial-Data-Science-in-Python/blob/2fe3ae6dc08dc80d2f5d0c38ba0562e01f1c7415/The%20Market's%20Not%20Normal/The_Market's_Not_Normal.ipynb)| [The Market's Not Normal, Part 1](https://medium.com/adventures-in-data-science/the-markets-not-normal-part-1-bbba8dad2807) |
| The Market's Not Normal: Part 2| [These_Two_Things_are_Not_the_Same.ipynb](https://github.com/Farmhouse121/Financial-Data-Science-in-Python/blob/2fe3ae6dc08dc80d2f5d0c38ba0562e01f1c7415/The%20Market's%20Not%20Normal/These_Two_Things_are_Not_the_Same.ipynb) | [The Market's Not Normal: Part 2](https://medium.com/adventures-in-data-science/the-markets-not-normal-part-2-cf8c4060f6b4)|
| Can Non-Stationarity Rescue the Normal Distribution? | [Non_Stationarity_in_the_First_Two_Moments.ipynb](https://github.com/Farmhouse121/Financial-Data-Science-in-Python/blob/2fe3ae6dc08dc80d2f5d0c38ba0562e01f1c7415/The%20Market's%20Not%20Normal/Non_Stationarity_in_the_First_Two_Moments.ipynb) | [Can Non-Stationarity Rescue the Normal Distribution?](https://medium.com/adventures-in-data-science/can-non-stationarity-rescue-the-normal-distribution-4af9f708b26a)|
| Let's Talk About Heteroskedasticity | [The_Variance_is_Not_Stationary.ipynb](https://github.com/Farmhouse121/Financial-Data-Science-in-Python/blob/main/The%20Market's%20Not%20Normal/The_Variance_is_Not_Stationary.ipynb) | [Let's Talk About Heteroskedasticity](https://medium.com/@stattrader/lets-talk-about-heteroskedasticity-f1443d628da0)|

## The Data
I am going to use public domain data sources, which will be mostly _Yahoo! Finance_, accessed via the `yfinance` package, and the _Fred_ depository, operated by the Federal Reserve Bank of St. Louis with data downloaded directly via the web service they provide. This is mostly daily and slower cadence data. Most of what I will write about lives in that space.

## Making Proper Time Indices for Pandas
It's been my experience that many codes return Pandas dataframes with a timestamp field for an axis but that the system is _not properly told_ that the data is, in fact, temporal in nature. (I'm looking at you **everybody** who uses textual dates as their timestamps!) This error can be remedied with the following construct, which you will see _extensively_ in my code:
```
df=pd.DataFrame(...)
df.index=pd.DatetimeIndex(df.index).to_period('B')
```
which delivers an index of _business days_, for example. (I am grateful to [Alex De Castro](https://github.com/decastro-alex) for pointing out the existence of the `B` argument to me.)

## $\LaTeX$ "Scratchpads"
Since my writing contains _a lot_ of mathematics, which I generally render in $\LaTeX$ and then cut'n'paste into less civil document preparation systems, I've decided to add documents that include the _math mode code_ to generate the equations. These will not render as full $\LaTeX$ documents (as I am not writing the Medium articles in $\LaTeX$, I'm not going to go through the bother of preparing an analogue document for antoher format). If Medium would support $\LaTeX$ markup, in the way that GitHub does, then that would change.

## There Will be Many Commits
I have learned from three decades doing scientific research & development work that it is very hard to predict which of the many edits to a script will be the _final_ one that makes it all work. In addition, I've learned that memorializing that "first working version" with a weighty editorial commit will be immediately followed by an "oh yea, also" commit to follow a few minutes later. So I don't really try, I commit when I think I've done something useful and don't shy away from committing frequently. This is particularly useful if one uses GitHub, _as I do_, to synchronize code between different physical locations (e.g. my desktop and an AWS server, for example). This may be "bad practice," but it is my practice.

## Support
I appreciate the many positive comments I receive regarding my work and my attempts to explain aspects of the scientific analysis of financial markets to people. If you would like to _directly_ support this work, you can _Buy me a Coffee_ via the link below. [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/H2H7EC7Z5)

You may also buy my books via Amazon and other booksellers.

* [Adventures in Financial Data Science](https://medium.com/r/?url=https%3A%2F%2Famzn.to%2F3P66fyK)
* [Essays on Trading Strategy](https://medium.com/r/?url=https%3A%2F%2Fwww.amazon.com%2FEssays-Trading-Strategy-Scientific-Finance%2Fdp%2F9811273812)
