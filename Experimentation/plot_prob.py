import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def prob_plot(data, legend_always=True, fig_size=(10, 8), group_col='target', x_axis='forecast_date', y_axis='cases', x_label='Forecast Time', y_label='Weekly Cases', save_folder='Analysis', savefile='prob_plot', is_log=True, column_color={}, focus_model=['OptimWISE'], location=''):
    
    plt.figure(figsize=fig_size)
    gt = data[data[group_col]=='1-step_ahead'].sort_values(x_axis)
    s_date = data[x_axis].min()+pd.Timedelta(days=7)
    e_date = data[x_axis].max()
    plt.plot(gt[x_axis], gt[y_axis], color='black', linestyle='-', label='ground Truth', linewidth=1)
    models = data.model.unique()
    temp = s_date
    
    track_i = True
    
    while(temp<e_date):
        f_dates = [temp, temp+pd.Timedelta(days=7),temp+pd.Timedelta(days=14), temp+pd.Timedelta(days=21)]
        
        for m, t_group in data.groupby('model'):
            n_group = t_group[t_group[x_axis]==temp]
            if len(n_group)<4:
                continue
            n_group = n_group.sort_values(group_col)
            low = n_group['q_0.025']
            high = n_group['q_0.975']
            if m in focus_model:
                alpha = 1
                linewidth = 3
                linestyle = '-'
            else:
                linewidth = 2
                linestyle = '--'
                alpha=1
            if m in models:
                plt.plot(f_dates, n_group['point'], color=column_color[m], linestyle=linestyle, label=m, linewidth=linewidth, alpha=alpha)
                models = models[models!=m]
            else:
                plt.plot(f_dates, n_group['point'], color=column_color[m], linestyle=linestyle, linewidth=linewidth, alpha=alpha)
            if m in focus_model:
                plt.fill_between(f_dates, high, low, color=column_color[m], alpha=0.25) #, label='95% Interval'
        track_i = False
        temp = temp+pd.Timedelta(days=28)
            
    if is_log:
        plt.yscale('log')
    plt.xlabel('Forecast Time')
    plt.ylabel('Weekly Cases')
    plt.legend()
    plt.savefig(f'{save_folder}/{savefile}_{location}.png', bbox_inches='tight')