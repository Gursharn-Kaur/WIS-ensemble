import pandas as pd
import math
import numpy as np
'''
    Calculates the weights for each model over a training period following the formula:
    
    W_m_i = Mean[t=1..tp]{1/wis_m_{i-t}}/Sum[x in all models]{Mean[t=1..tp]{1/wis_x_{i-t}}}
    
    Arguments-
    
    data: dataframe. Data must contain at least four columns. They must be named `target_end_date` (end date of forecasting week), `method`, `forecast_date` (forecasting date, always monday), `target` (indicates how many week ahead forecasting e.g., 1-step_ahead), and `wis` (indicates wis value of the model), `FIPS` (indicates fips code for the county).
    
    t_p: training period. By default 4
    
    
    Returns-
    
    same dataframe with three extra columns: `avg_wis_training`, `inv_wis_training`, `weights`
'''

def model_weights(data, t_p = 4):
    
    avg_wis_value = []

    for idx, row in data.iterrows():
        target = int(row['target'].split('-')[0])
        e_date = row['forecast_date']-pd.Timedelta(days=target*7)
        s_date = row['forecast_date']-pd.Timedelta(days=target*7+t_p*7)
        selected_rows = data[(data['forecast_date']>s_date)&(data['forecast_date']<=e_date)&(data['method']==row['method'])&(data['target']==row['target'])&(data['FIPS']==row['FIPS'])]

        assert selected_rows['forecast_date'].unique()!=len(selected_rows) or selected_rows['target_end_date'].unique()!=len(selected_rows), 'Duplicate rows are found: {}'.format(selected_rows)
        assert len(selected_rows)<=t_p, 'Selected rows more than training period size: {}'.format(selected_rows)
        if len(selected_rows)==0:
            avg_wis_value.append(np.nan)
            continue
        avg_wis = selected_rows['wis'].mean()
        avg_wis_value.append(avg_wis)
        
    
    data['avg_wis_trainig'] = avg_wis_value

        
    return data











'''
converts row dataframe to column dataframe

takes a dataframe found from ``model_weights`` methods


returns a dataframe with following columns:
`forecast_date`, `target_end_date`, `target`, `FIPS`, {model_name}
model_name indicates weights for that models for the specific dates
'''





def change_weights_format(data):
    forecast_date = []
    target_end_date = []
    target = []
    FIPS = []
    ar = []
    ar_spatial = []
    lstm = []
    patch = []
    patch_delta = []
    arima = []
    enkf = []
    for name, group in data.groupby(['forecast_date','target_end_date','FIPS','target']):

        fct_date, target_date, fips, step_ahead = name
        forecast_date.append(fct_date)
        target_end_date.append(target_date)
        FIPS.append(fips)
        target.append(step_ahead)
        
        
        
        if group['avg_wis_trainig'].min()<=0:
            zero_count = len(group[group['avg_wis_trainig']<=0])
            group['weights'] = 0
            group.loc[group['avg_wis_trainig']<=0, 'weights'] = 1.0/zero_count
            print(zero_count)
        else:
            sum_inv_wis = (1.0/group['avg_wis_trainig']).sum()
            group['weights'] = (1.0/group['avg_wis_trainig'])/sum_inv_wis
            
        

        if len(group[group['method']=='AR'])>0:
            ar.append(group[group['method']=='AR']['weights'].values[0])
        else:
            ar.append(np.nan)
        if len(group[group['method']=='AR_spatial'])>0:
            ar_spatial.append(group[group['method']=='AR_spatial']['weights'].values[0])
        else:
            ar_spatial.append(np.nan)
        if len(group[group['method']=='ARIMA'])>0:
            arima.append(group[group['method']=='ARIMA']['weights'].values[0])
        else:
            arima.append(np.nan)
        if len(group[group['method']=='PatchSim_adpt'])>0:
            patch.append(group[group['method']=='PatchSim_adpt']['weights'].values[0])
        else:
            patch.append(np.nan)
        if len(group[group['method']=='lstm'])>0:
            lstm.append(group[group['method']=='lstm']['weights'].values[0])
        else:
            lstm.append(np.nan)
        if len(group[group['method']=='PatchSim_adpt-Delta'])>0:
            patch_delta.append(group[group['method']=='PatchSim_adpt-Delta']['weights'].values[0])
        else:
            patch_delta.append(np.nan)
        if len(group[group['method']=='ENKF'])>0:
            enkf.append(group[group['method']=='ENKF']['weights'].values[0])
        else:
            enkf.append(np.nan)
    weights_data = pd.DataFrame({
        'forecast_date': forecast_date,
        'target_end_date': target_end_date,
        'target': target,
        'FIPS': FIPS,
        'AR': ar,
        'AR_spatial': ar_spatial,
        'ARIMA': arima,
        'lstm': lstm,
        'PatchSim_adpt': patch,
        'PatchSim_adpt-Delta': patch_delta,
        'ENKF': enkf
    })
    return weights_data

