import pandas as pd
import math
import numpy as np
from Experimentation.monte_carlo import *
'''

    Returns ensemble result using Vincent aggregation.
    
    Arguments-
    data: dataframe. There must be `target_end_date` and `cases` column in the dataframe. `target_end_date` is the end date of forecasting week and `cases` is the ground truth. Column size depends on the size of the alphas. For each value of alpha, there must be a column named `q_{alpha value}`. For example, for a given alpha=[0.1,0.2], there will be two new columns- q_0.1 and q_0.2. q_0.1 column has the qunatile values for 0.1. 
    
    w_data: dataframe. Contains weights for each model at different forecasting date. There must be `target_end_date` column as forecasting date and {model name} columns indicating as model weights for that forecasting date.
    alphas: list of quantiles to compute, which must be between 0 and 1 inclusive.
    
    Returns: 
    
    A new dataframe containing `target_end_date`, `cases`, and `q_{quantiles}`. `q_{quantiles}` is the quantile values for the ensemble model. 
'''

def Vincent_Ensemble(data, w_data, alphas):
    quantiles = ['q_{}'.format(a) for a in alphas]
    columns = ['target_end_date','cases', 'forecast_date','FIPS','target','method']
    columns.extend(quantiles)
    final_output = pd.DataFrame(columns=columns)
    w_data = w_data.replace(np.nan,0)
    
    for idx,row in w_data.iterrows():
        train_data = data[(data['target_end_date']==row['target_end_date'])&(data['target']==row['target'])&(data['FIPS']==row['FIPS'])]

        final_output.loc[idx, quantiles] = 0
        for _,method_row in train_data.iterrows():
            final_output.loc[idx, quantiles] += method_row[quantiles]*row[method_row['method']]
        
        final_output.loc[idx,'cases'] = train_data['cases'].values[0]
        assert train_data['cases'].unique().__len__()==1, 'Number of cases for a forecast must be same: {} {}'.format(train_data, train_data['cases'].unique().__len__())
        final_output.loc[idx,'target_end_date'] = row['target_end_date']
        final_output.loc[idx,'forecast_date'] = row['forecast_date']
        final_output.loc[idx,'FIPS'] = row['FIPS']
        final_output.loc[idx, 'target'] = row['target']
        final_output.loc[idx, 'method'] = 'Vincent'
        
        
    return final_output
    
    
'''

    Returns ensemble result using LOP aggregation.
    
    Arguments-
    data: dataframe. There must be `target_end_date`, `FIPS`, `forecast_date`, `target`, `fct_mean`, `fct_std`, and `cases` column in the dataframe. `target_end_date` is forecasting date and `cases` is the ground truth. Column size depends on the size of the alphas.
    
    w_data: dataframe. Contains weights for each model at different forecasting date. There must be `target_end_date` column as forecasting date and {model name} columns indicating as model weights for that forecasting date.
    alphas: list of quantiles to compute, which must be between 0 and 1 inclusive.
    
    Returns: 
    
    A new dataframe containing `target_end_date`, `FIPS`, `forecast_date`, `target`, `cases`, and `q_{quantiles}`. `q_{quantiles}` is the quantile values for the ensemble model. 
'''
def LOP_Ensemble(data, w_data, alphas):
    quantiles = ['q_{}'.format(a) for a in alphas]
    columns = ['target_end_date','cases', 'forecast_date','FIPS','target','method']
    columns.extend(quantiles)
    final_output = pd.DataFrame(columns=columns)
    w_data = w_data.replace(np.nan,0)
    for idx,row in w_data.iterrows():
        train_data = data[(data['target_end_date']==row['target_end_date'])&(data['target']==row['target'])&(data['FIPS']==row['FIPS'])]

        means = train_data['fct_mean'].tolist()
        stds = train_data['fct_std'].tolist()
        
        methods = train_data['method'].tolist()
        weights = row[methods].tolist()
        
        
        
        assert len(weights)!=0, 'no weights found'
        
        lop_quantiles = monte_carlo(weights, means, stds, alphas)
        final_output.loc[idx,quantiles] = lop_quantiles
        final_output.loc[idx,'cases'] = train_data['cases'].values[0]
        assert train_data['cases'].unique().__len__()==1, 'Number of cases for a forecast must be same'
        final_output.loc[idx,'target_end_date'] = row['target_end_date']
        final_output.loc[idx,'forecast_date'] = row['forecast_date']
        final_output.loc[idx,'FIPS'] = row['FIPS']
        final_output.loc[idx, 'target'] = row['target']
        final_output.loc[idx, 'method'] = 'LOP'
        
        
    return final_output
