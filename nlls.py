import numpy as np
from statsmodels.base.model import GenericLikelihoodModel
from statsmodels.api import add_constant
from scipy.stats import norm
from scipy.optimize import Bounds
from my_library import zero,one

class NLLS(GenericLikelihoodModel):
    """
    Fit a Non-Linear Least Squares model to data via MLE.

    This is a maximum likelihood regression to a Normal distribution with a non-linear mean process,
    with an added regressor being the standard deviation of errors. If you do not override the `.predict()`
    method it will actually use a linear mean process and so is equivalent to OLS, but slower! You can change
    the distribution used by supplying a pdf function that matches the scipy.stats framework.

    The code follows the usual statsmodels conventions for a model defined in terms of a dependent variable named `endog` and independent
    variables named `exog`, and with the `add_constant()` function expected if an intercept is required. If you do not supply any data for
    `exog` a constant column will be used. The system fits the standard deviation of the data (which is required by the method). You can supply
    any `scipy.stats` format univariate distribution via the `distribution` argument and any extra variables via `extra_params_names`. The
    regression is performed via the `scipy.optimize.minimize` function and (in my experience) can be a little brittle. You may need to supply
    user bounds for the latent variables if the default ones chosen are incorrect.
    """
    def __init__(self,endog,exog=None,distribution=norm,extra_params_names=[],**kwargs):
        """Initialize the object, setting helpful data, and then call the base constructor."""
        # a small number
        self.epsilon=1e-7

        # check for univariate problem
        if len(endog.shape)>1:
            raise NotImplementedError("Only univariate processes are supported, you supplied a %d-d array for endog." % len(endog.shape))

        # if no exogenous series, put in a series of ones for the constant
        if exog is None:
            exog=np.ones(endog.shape[0])

        # add xtra distribution process parameters, which are "hidden" from the exog vector input
        self.distribution=distribution
        self.latent_variables=['sigma']+extra_params_names

        # initialize the base class with the added variables as "extra_params"
        super(NLLS,self).__init__(endog,exog,extra_params_names=self.latent_variables,**kwargs)

        # adjust d.o.f., it seems that the code doesn't get this right as given by the examples on line
        self.df_resid-=len(self.latent_variables)
        self.df_model=self.nparams-self.k_constant

    def _pick_params(self,params):
        """Helper function to divide the parameters into linear process, disperstion and other latent variable parameters."""
        assert len(params)==self.nparams

        # memorialize parameters
        self.params=params

        # pick up parameters from the right slots
        n=len(self.latent_variables)

        if n>1:
            beta=params[:-n]
            sigma=params[-n]
            extra=list(params[-n+1:])

        elif n==1:
            beta=params[:-1]
            sigma=params[-1]
            extra=[]

        else:
            raise ValueError("The number of latent variables cannot be zero.")

        return beta,sigma,extra

    def predict(self,exog=None,params=None):
        """
        Returns the mean process prediction for the given inputs.

        If exog or params are None then self.exog, and/or self.params, will be used respectively.
        If you want to do something other than OLS, you should override this method with some other
        formula. If you don't want to use the Normal Distribution for the error process you should
        supply some other distribution when you instantiate the class.
        """
        beta,sigma,extra=self._pick_params(params if params is not None else self.params)
        _exog=exog if exog is not None else self.exog
        mean=np.dot(_exog,beta) # if you want something other than OLS, change this formula

        return mean

    def nloglikeobs(self,params):
        """Returns a vector of negative log-likelihood values for each observation."""
        # get the parameters divided into those for the mean process and the latent variables
        beta,sigma,extra=self._pick_params(params)

        # compute the mean model, dot computes the time-series of the dot product of the observation rows with beta
        self.mean=self.predict()
        self.innovation=(self.endog-self.mean)/sigma

        # set the distribution with the location set to zero as we specify the mean-model explicitly
        density=self.distribution(*extra,loc=zero,scale=sigma)

        # compute vector of negative log likelihood of vector of observations
        return -density.logpdf(self.endog-self.mean)

    def fit(self,start_params=None,bounds=None,maxiter=1000,**kwargs):
        """
        Perform a regression using trust-constrained gradient minimization.

        NOTE: This code will try to guess values for `start_params` and `bounds` if you don't supply them. In particular,
        it will guess `(-np.inf,+np.inf)` for the limits of any latent variables added by the user. If this assumption is wrong,
        the regression may fail. In which case, user supplied values should be substituted. It's my experience that this regression
        method is "slow" and "fragile," but it is the required one.
        """
        # the regression problem parameters are defined HERE by the start_params vector, wierd huh?
        if start_params is None:
            start_params=[zero]*self.exog.shape[1]+[self.endog.std()]+[one]*(len(self.latent_variables)-1)

            if self.k_constant:
                start_params[0]=self.endog.mean()

        # set the bounds
        if bounds is None:
            bounds=[(-np.inf,np.inf)]*self.exog.shape[1]+[(self.epsilon,np.inf)]+[(-np.inf,np.inf)]*(len(self.latent_variables)-1)

        # check we set the right number of variables
        assert len(start_params)==self.nparams
        assert len(bounds)==self.nparams

        # now let the base class do the regression, specifying the trust-constraint method for scipy.optimize with bounds
        f=super(NLLS,self).fit(
            start_params=start_params,
            method='minimize',
            min_method='trust-constr',
            bounds=Bounds(*list(zip(*bounds))),
            maxiter=maxiter,
            **kwargs
        )
        f.named_params=dict(zip(self.exog_names,self.params))
        f.num_params=len(f.named_params)
        return f

