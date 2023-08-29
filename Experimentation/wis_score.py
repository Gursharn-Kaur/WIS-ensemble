'''
    this function is used to calculate WIS value based on different quantile values for different forecasts.
    
    Arguments-
    
    data: pandas dataframe. data must have the following columns: `cases`, `q_alpha[0]`, `q_alpha[1]`, `q_alpha[2]`, ..., `q_alpha[len-1]`.
    alpha: list of float, sequence of quntiles. All quantiles must be in between 0 and 1, inclusive.
    
    
    Returns-
    
    data: pandas dataframe. returns the same dataframe as input. In addition, a new `wis`
'''

def get_all_wis_score(data, alpha):
    data['wis'] = data.apply(lambda x:wis_score(x['cases'],[x['q_'+str(a)] for a in alpha], alpha), axis=1)
    return data


'''
    function calculates WIS based on the following formula:
    https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618
    
    Arguments-
    
    y: float, ground truth.
    quantiles: list of float, indicates the quantile values at each point of alpha.
    alpha: list of float, sequence of quntiles. All quantiles must be in between 0 and 1, inclusive.
    
    Returns-
    
    wis: float, weighted interval score for the given distribution (distribution represented by the quantiles).

'''
def wis_score(y, quantiles, alpha):
    sum_val = 0
    for idx,(q,a)  in enumerate(zip(quantiles,alpha)):
        sum_val+=2*((y<=q)-a)*(q-y)
    return sum_val/len(quantiles)
    