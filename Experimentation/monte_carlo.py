import pandas as pd
import numpy as np

'''
    LOP method aggregate singular predictions.
    Monte carlo assumes that the singular predictions follow gaussian distribution and can be represented by mean and standard deviation.
    Monte carlo method takes four arguments-- weights, means, stds, and alphas. 
    
    weights: list of weights for individual distributions. Example: weights = [0.1,0.2,0.3,0.4] indicates 4 individual distributions having weights 0.1, 0.2, 0.3, and 0.4. Summation of the weights must be 1, i.e., sum(weights)=1.
    
    means: list of mu for individual distributions. Length of means and weights must be same.
    stds: list of standard deviation for individual distributions. Length of stds and weights must be same.
    alphas: list of quantiles to compute, which must be between 0 and 1 inclusive.
    
    
    
    
    
    Returns:
    quantiles: the result corresponds to the quantiles.
    
'''
def monte_carlo(weights, means, stds, alphas):
    
    assert len(weights)!=0, 'Weights can not be empty.'
    assert len(means)!=0, 'Mean can not be empty.'
    assert len(stds)!=0, 'Standard Deviation can not be empty.'
    assert len(alphas)!=0, 'Alphas can not be empty.'
    assert min(alphas)>=0 and max(alphas)<=1, 'quantile values must be between 0 and 1 inclusive.'
    
    assert len(weights)==len(means) and len(means)==len(stds), 'Length of weights, means, and standard deviation must be same.'
#     assert sum(weights) == 1.0,"Summation of the weights must be equal to 1."
    sample_dist = np.sum(np.random.multinomial(n=1, pvals=weights, size=10000), axis=0)
    samples = []
    for dist in range(len(sample_dist)):
        sample = np.random.normal(loc=means[dist], scale=stds[dist], size=sample_dist[dist])
        samples.extend(sample)
    samples = np.array(samples)
    quantiles = np.quantile(samples, alphas)
    quantiles[quantiles<0] = 0
    
    return quantiles