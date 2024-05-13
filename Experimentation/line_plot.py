import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
###range takes 2 values maximum: ymin, ymax
def plot_lines(data, fig_size=(10,8),group_col=['target'],add_baseline=[], y_range=[], marker_type='o', line_width_focus= 2, x_axis='forecast_date', y_axis='model', x_label='Forecast Date', y_label='Method', save_folder='Analysis', savefile='line_plot', value='wis', plot_rank=False, plot_normal=True, column_color={}, focus_column=[], opacity_non_focus=0.3, non_focus_color='grey', line_width_non_focus=1):
    if len(group_col)>0:
        for (target_week), group in data.groupby(group_col):
            if len(group) == 0:
                continue
            
            group = group.sort_values(by=[x_axis])
            
            plt.figure(figsize=fig_size)

            plots_name = group[y_axis].unique()
            colors = dict(zip(plots_name, plt.cm.tab10.colors[:len(plots_name)]))
            
            if len(column_color)>0:
                colors = column_color
            for model, model_group in group.groupby(y_axis):
                if len(focus_column)==0:
                    plt.plot(model_group[x_axis], model_group[value], label=model,color=colors[model], marker=marker_type)
                else:
                    alpha = 1
                    linewidth = line_width_focus
                    marker = marker_type
                    if model not in focus_column:
                        alpha=opacity_non_focus
                        linewidth = line_width_non_focus
                        marker = ''
                        if non_focus_color!='None':
                            colors[model] = non_focus_color
                        
                    plt.plot(model_group[x_axis], model_group[value], label=model, alpha=alpha, linewidth=linewidth, color=colors[model], marker=marker, markersize=3)

            plt.xlabel(x_label)
            plt.ylabel(y_label)
            if not plot_normal:
                plt.yscale('log')  # Set the y-axis scale to logarithmic
            plt.legend()
            
            plt.savefig(f'{save_folder}/{savefile}_{target_week}.png', bbox_inches='tight')
            plt.close()  # Close the figure to avoid overlapping plots
    
    else:
        
        group = data.sort_values(by=[x_axis])
            
        plt.figure(figsize=fig_size)

        plots_name = group[y_axis].unique()
        colors = dict(zip(plots_name, plt.cm.tab10.colors[:len(plots_name)]))
            
        if len(column_color)>0:
            colors = column_color
        for model, model_group in group.groupby(y_axis):
            if len(focus_column)==0:
                plt.plot(model_group[x_axis], model_group[value], label=model,color=colors[model], marker=marker_type)
            else:
                alpha = 1
                linewidth = line_width_focus
                marker = marker_type
                if model not in focus_column:
                    alpha=opacity_non_focus
                    linewidth = line_width_non_focus
                    marker = ''
                    if non_focus_color!='None':
                        colors[model] = non_focus_color
                        
                plt.plot(model_group[x_axis], model_group[value], label=model, alpha=alpha, linewidth=linewidth, color=colors[model], marker=marker, markersize=3)
        if len(add_baseline):
            for val in add_baseline:
                plt.axhline(val, linestyle='--', alpha=0.5)
        if len(y_range):
            plt.ylim(y_range[0], y_range[1])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if not plot_normal:
            plt.yscale('log')  # Set the y-axis scale to logarithmic
        plt.legend()
            
        plt.savefig(f'{save_folder}/{savefile}.png', bbox_inches='tight')
        plt.close()  # Close the figure to avoid overlapping plots
        


# if plot_rank:
#             plt.figure(figsize=(10, 8))
#             rank_df = group.pivot_table(index=x_axis, columns=y_axis, values=value).rank(axis=1, ascending=lower_is_better)
            
#             for model in rank_df.columns:
#                 plt.plot(rank_df.index, rank_df[model], label=model)

#             plt.xlabel(x_label)
#             plt.ylabel(y_label)
#             plt.yscale('log')  # Set the y-axis scale to logarithmic
#             plt.legend()

#             plt.title(f"Line Plot (Rank) for {target_week}")
#             plt.savefig(f'{save_folder}/{savefile}_rank_{target_week}.png', bbox_inches='tight')
#             plt.close()  # Close the figure to avoid overlapping plots
