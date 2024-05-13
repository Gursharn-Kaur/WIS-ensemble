import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap

def plot_heatmap(data, group_col=['target'],x_axis='forecast_date',y_axis='model', x_label='Forecast Date',y_label='Method',save_folder = 'Analysis', savefile='heatmap', value='wis', plot_rank=False, plot_normal=True, lower_is_better=True): ###groupby target, forecast_date, wis
    
    for (target_week,), group in data.groupby(group_col):
        # group = group[(group['forecast_date']>pd.to_datetime('2021-01-01'))&((group['forecast_date']<pd.to_datetime('2021-09-01')))]
        if len(group)==0:
            continue
        pivot_df = group.pivot_table(index=y_axis, columns=x_axis, values=value)
        pivot_df.columns = pivot_df.columns.strftime('%Y-%m-%d')
        if plot_normal:
            plt.figure(figsize=(10, 8))
            # cmap = sns.light_palette('blue', as_cmap=True)
            reverse = lower_is_better
            # cmap, cmap_segments = create_custom_colormap(reverse=reverse)
            # cmap = sns.light_palette("orange", as_cmap=True)
            
            # cmap = create_custom_colormap("#251232", "#ad3c72", "#e7453e", "#ea9371", )
            # cmap = sns.light_palette(, as_cmap=True)
            # cmap = sns.light_palette(("#e0d7d3", "#ad3c72"), as_cmap=True, reverse=True)
            # cmap = sns.light_palette(((20, 60, 40),(20,60,80)), input="husl", as_cmap=True, reverse=reverse)
            cmap = sns.light_palette("seagreen", as_cmap=True, reverse=reverse)

            sns.heatmap(pivot_df, cmap=cmap, annot=False, linewidths=0,square=False, cbar_kws={'shrink': 0.5})

            plt.xticks(rotation=45, ticks=plt.xticks()[0][::3])  # Rotate x-axis labels for better readability
            # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            plt.xlabel(x_label)
            plt.ylabel(y_label)

            # plt.title(f"Heatmap for {target_week}")
            plt.savefig(f'{save_folder}/{savefile}_{target_week}.png', bbox_inches='tight')
        
        if plot_rank==True:
            plt.figure(figsize=(10, 8))
            rank_df = pivot_df.rank(axis=0, ascending=True, method='min')
            
            # cmap = sns.light_palette('red', as_cmap=True, reverse=True)
            # cmap = sns.dark_palette("orange", as_cmap=True)
            
            # cmap = create_custom_colormap("#251232", "#ad3c72", "#e7453e", "#ea9371", "#e0d7d3")
            # cmap = sns.light_palette("#ad3c72", as_cmap=True)
            # cmap, cmap_segments = create_custom_colormap(reverse=False)
            # cmap = sns.light_palette((20, 60, 50), input="husl", as_cmap=True, reverse=True)
            cmap = sns.light_palette("seagreen", as_cmap=True, reverse=True)
            sns.heatmap(rank_df, cmap=cmap, annot=False, linewidths=0,square=False, cbar_kws={'shrink': 0.5})

            plt.xticks(rotation=45, ticks=plt.xticks()[0][::3])  # Rotate x-axis labels for better readability
            # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            plt.xlabel(x_label)
            plt.ylabel(y_label)

            # plt.title(f"Heatmap for {target_week}")
            plt.savefig(f'{save_folder}/{savefile}_rank_{target_week}.png', bbox_inches='tight')