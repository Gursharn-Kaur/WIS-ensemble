from scipy.stats import norm
import math
import warnings

'''
    This function calculates the quantile values of multiple gaussian distributions.
    
    Arguments-
    
    data: pandas dataframe. There must be at least two columns: fct_mean and fct_std. `fct_mean` is the forecasting mean and `fct_std` is the forecasting standard deviation. The distribution must be a gaussian.
    alpha: list of float, sequence of quntiles. All quantiles must be in between 0 and 1, inclusive.
    
    Returns-
    
    data: dataframe, returns the same dataframe. New columns are added at the end of the given dataframe. Newly added column size depends on the size of the alphas. For each value of alpha, there is a new column named `q_{alpha value}`. For example, for a given alpha=[0.1,0.2], there will be two new columns- q_0.1 and q_0.2. q_0.1 column has the qunatile values for 0.1. 

'''
def get_all_quatiles(data, alpha):
    
    assert len(alpha)!=0, 'alpha can not be empty.'
    assert 'fct_mean' in data.keys() and 'fct_std' in data.keys(), '`fct_mean` and/or `fct_std` column are absent in the data' 
    
    
    for a in alpha:
        data['q_'+str(a)] = data.apply(lambda x: quantiles(x['fct_mean'],x['fct_std'],a), axis=1)
    return data


'''

    This function is used to calculate a quantile value of a gaussian distribution.
    Arguments-
    
    mean: float, mean of a gaussian distribution.
    std: float, standard deviation of a gaussian distribution.
    alpha: float, indicates quantile. alpha must be in between 0 and 1, inclusive.
    
    
    Returns-
    
    how/low: float, quantile value of the distribution for the specified quantile. 
    
    
'''
def quantiles(mean, std, alpha):
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        try:
            if std<=0:
                return mean
            elif alpha<0.5:
                alpha = (0.5-alpha)*2
                low, high = norm.interval(alpha, loc=mean, scale=std)
                return low
            else:
                alpha = (alpha-0.5)*2
                low, high = norm.interval(alpha, loc=mean, scale=std)
                return high
        except Warning as warn:
            # Handle the warning
            print("Warning:", str(warn), mean, std, alpha)