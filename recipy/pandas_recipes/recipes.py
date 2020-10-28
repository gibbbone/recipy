import pandas as pd
from functools import reduce

def merge_dfs_on_common_element(dfs, on='index', how='left'):
    if on=='index':
        results = reduce(
            lambda x, y: pd.merge(x, y,left_index=True, right_index=True, how=how), 
            dfs)
    else: 
        results = reduce(
            lambda x, y: pd.merge(x, y,left_on=on, right_on=on, how=how), 
            dfs)
    return results    

def get_duplicate_columns(df):
    '''
    Get a list of duplicate columns.
    It will iterate over all the columns in dataframe and find the columns whose contents are duplicate.
    :param df: Dataframe object
    :return: List of columns whose contents are duplicates.
    '''
    duplicate_column_names = set()
    # Iterate over all the columns in dataframe
    for x in range(df.shape[1]):
        # Select column at xth index.
        col = df.iloc[:, x]
        # Iterate over all the columns in DataFrame from (x+1)th index till end
        for y in range(x + 1, df.shape[1]):
            # Select column at yth index.
            otherCol = df.iloc[:, y]
            # Check if two columns at x / y index are equal
            if col.equals(otherCol):
                duplicate_column_names.add((df.columns.values[x],df.columns.values[y]))
 
    return list(duplicate_column_names)    