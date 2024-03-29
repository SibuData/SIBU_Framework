# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:21:53 2018

@author: DANIEL MARTINEZ
@co-author: FABIO FERNÁNDEZ AGUILAR  [2019-10-12]
Desc: Se revisan y extienden las funcionalidades del EDA-Framework

"""

import pandas as pd

def get_missing_data_table(dataframe):
    total = dataframe.isnull().sum()
    percentage = dataframe.isnull().sum() / dataframe.isnull().count()
    
    missing_data = pd.concat([total, percentage], axis='columns', keys=['TOTAL','PERCENTAGE'])
    return missing_data.sort_index(ascending=True)

def get_null_observations(dataframe, column):
    return dataframe[pd.isnull(dataframe[column])]

def delete_null_observations(dataframe, column):
    fixed_df = dataframe.drop(get_null_observations(dataframe,column).index)
    return fixed_df
    
def transform_dummy(dataframe, column, drop_first=False):
    df = dataframe.copy()
    col = df[column]
    transformed = pd.get_dummies(col, drop_first=drop_first)
    transformed.rename(columns=lambda x: column+'_'+x, inplace=True)
    return transformed

def imput_nan_values(dataframe, column, strateg, fill_value=None):
    from sklearn.impute import SimpleImputer
    if strateg == 'constant':
        imp = SimpleImputer(strategy=strateg, fill_value=fill_value)
    else:
        imp = SimpleImputer(strategy=strateg)
    df = dataframe.copy()
    df[column] = imp.fit_transform(df[column].values.reshape(-1,1))
    return df

def delete_column(dataframe, column):
    return dataframe.drop([column], axis='column')

def get_upper_outliers(dataframe, column):
    h_spread = dataframe[column].quantile(.75) - dataframe[column].quantile(.25)
    limit = dataframe[column].quantile(.75) + 2 * h_spread
    return dataframe[dataframe[column] > limit]

def get_lower_outliers(dataframe, column):
    h_spread = dataframe[column].quantile(.75) - dataframe[column].quantile(.25)
    limit = dataframe[column].quantile(.25) - 2 * h_spread
    return dataframe[dataframe[column] < limit]

def delete_outliers(dataframe, column, hinge):
    if hinge == 'upper':
        outliers = get_upper_outliers(dataframe, column)
    elif hinge == 'lower':
        outliers = get_lower_outliers(dataframe, column)
    
    return dataframe.drop(outliers.index)

def get_correlation_table(dataframe):
    df = dataframe.copy()
    corr = df.corr()
    return corr.style.background_gradient().set_precision(2)
    
