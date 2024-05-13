import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_boxplot(data, group_col=['target'], x_axis='model', y_axis='wis', x_label='Model', y_label='WIS', save_folder='Analysis', savefile='boxplot', log_scale=True):
    for (target_week,), group in data.groupby(group_col):
        if len(group) == 0:
            continue
        
        plt.figure(figsize=(10, 8))
        
        if log_scale:
            group[y_axis] = np.log1p(group[y_axis])  # Applying log transformation for better visualization
        
        sns.boxplot(x=x_axis, y=y_axis, data=group)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45)
        plt.savefig(f'{save_folder}/{savefile}_{target_week}.png', bbox_inches='tight')
        plt.close()  # Close the figure to avoid overlapping plots


