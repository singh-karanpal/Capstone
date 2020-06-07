# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-06

import pandas as pd
import numpy as np
import os
import pickle

with open('data/interim/subthemes/subtheme_dict.pickle', 'rb') as handle:
    subtheme_dict = pickle.load(handle)
    
def subset_data(label_name, X_train, y_train, X_valid, y_valid):
    """
    Subsets training and validation data for the provided label of question 1 for 
    subtheme classification and saves these datasets
    
    Parameters
    ----------
    label_name: (str)
        name of the label/main theme for which data has to be subsetted
    X_train: (Pandas dataframe)
        training dataframe containing raw comments
    y_train: (Pandas dataframe)
        training dataframe containing labels values
        
    Returns
    -------
    None
    """
    x = str(label_name)
    dir_name = os.mkdir('data/interim/subthemes/' + x)
    
    train_subset = pd.concat([X_train, y_train[subtheme_dict[x]]], axis=1)
    train_subset['remove_or_not'] = np.sum(train_subset.iloc[:,1:], axis=1)
    train_subset = train_subset[train_subset['remove_or_not'] != 0]
    train_subset.drop(columns='remove_or_not', inplace=True)
    
    X_train_subset = train_subset['Comment']
    X_train_subset.to_excel('data/interim/subthemes/' + x + '/X_train_subset.xlsx', index=False)
    
    Y_train_subset = train_subset.iloc[:, 1:]
    Y_train_subset.to_excel('data/interim/subthemes/' + x + '/Y_train_subset.xlsx', index=False)
    
    valid_subset = pd.concat([X_valid, y_valid[subtheme_dict[x]]], axis=1)
    valid_subset['remove_or_not'] = np.sum(valid_subset.iloc[:,1:], axis=1)
    valid_subset = valid_subset[valid_subset['remove_or_not'] != 0]
    valid_subset.drop(columns='remove_or_not', inplace=True)
    
    X_valid_subset = valid_subset['Comment']
    X_valid_subset.to_excel('data/interim/subthemes/' + x + '/X_valid_subset.xlsx', index=False)
    
    Y_valid_subset = valid_subset.iloc[:, 1:]
    Y_valid_subset.to_excel('data/interim/subthemes/' + x + '/Y_valid_subset.xlsx', index=False)