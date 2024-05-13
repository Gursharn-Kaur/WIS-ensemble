import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
def plot_bar(data, legend_always=True, fig_size=(10, 8), group_col=['target'], x_axis='rank', y_axis='count', x_label='Rank', y_label='Forecast Count', save_folder='Analysis', savefile='line_plot', hue='model', column_color={}):
    if len(group_col)>0:
        grouped_df = data.groupby(group_col)
        counter = 1
        for (target), group in grouped_df:
            plt.figure(figsize=fig_size)
            ax = sns.barplot(data=group, x=x_axis, y=y_axis, hue=hue, palette=column_color)
            for i in ax.containers:
                ax.bar_label(i)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            if legend_always:
                plt.legend()
            elif counter == 1:
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
                counter = 0
            else:
                ax.get_legend().remove()
            plt.savefig(f'{save_folder}/{savefile}_{target}.png', bbox_inches='tight')
            plt.close()  # Close the figure to avoid overlapping plots
    else:
            
            plt.figure(figsize=fig_size)
            ax = sns.barplot(data=data, x=x_axis, y=y_axis, hue=hue, palette=column_color)
            for i in ax.containers:
                ax.bar_label(i, fontsize=9)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            if legend_always:
                plt.legend()
            else:
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
            
            plt.savefig(f'{save_folder}/{savefile}.png', bbox_inches='tight')
            plt.close()  # Close the figure to avoid overlapping plots