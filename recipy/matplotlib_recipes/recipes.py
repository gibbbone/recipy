import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def shares_barplot(ax, results, category_names=None, cmap='inferno', fontsize=8, contrast_thres=186):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
        
    Modified from:
    https://matplotlib.org/3.1.3/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
    """
    # get cumulative sum of the data
    if type(results) == dict:
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)    

        # rescale data by total sum and multiply by 100
        data_tot = data.sum(1).reshape(data.shape[0],1)
        data = (data/data_tot)*100
        data_cum = (data_cum/data_tot)*100        

        # results keys become x labels
        # use string to avoid white spacees
        labels = list(map(str,list(results.keys())))        
    elif type(results) == pd.core.frame.DataFrame:
        data_cum = results.cumsum(1).div(results.sum(1), axis=0)*100
        data = results.div(results.sum(1), axis=0)*100
        labels = list(map(str,list(data.index)))
        category_names = list(data.columns)        
        
    # get colors
    category_colors = plt.get_cmap(cmap)(
        np.linspace(0.05, 0.95, data.shape[1]))
    
    # axis configuration
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, 100) 

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        # select ith row of data to plot it
        if type(results) == dict:
            widths = data[:, i]
            starts = data_cum[:, i] - widths
        elif type(results) == pd.core.frame.DataFrame:    
            widths = data.iloc[:, i]
            starts = data_cum.iloc[:, i] - widths  
            
        ax.barh(
            labels, widths, left=starts, 
            height=1, label=colname, 
            color=color)
        
        # annotate the row
        xcenters = starts + widths / 2
        r, g, b, _ = color        
        # cfr: 
        # https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        text_color =  'darkgrey' if (r*0.299 + g*0.587 + b*0.114)*255 > contrast_thres else "white"        
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            # skip small percentages
            if int(c)>0:
                ax.text(
                    x, y, str(int(c)), 
                    ha='center', va='center',
                    color=text_color, fontsize=fontsize)
    
    ax.legend(
        ncol=10,
        bbox_to_anchor=(0, 1),
        loc='lower left', fontsize='small')

    return ax