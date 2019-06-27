import numpy as np
import pandas as pd

def stat_summary(df):
    statsdf = df[['taint_precision', 'taint_recall', 'grad_precision', 'grad_recall']]
    for col in statsdf.columns:
        statsdf = statsdf[statsdf[col].notnull()]
    return pd.DataFrame({'mean':statsdf.mean(), 'std': statsdf.std()})


def precision(pred, actual):
    if type(pred) is float or type(actual) is float or len(pred) == 0:
        return np.nan
    return np.sum([1 if t in actual else 0 for t in pred])/len(pred)

def recall(pred, actual):
    if type(pred) is float or type(actual) is float or len(actual) == 0:
        return np.nan
    return np.sum([1 if t in pred else 0 for t in actual])/len(actual)


def get_labeled(df):
    return df[(df.lhs_label != 0) | (df.rhs_label != 0)]

def get_nonzero(df):
    return df[(np.abs(df.lhs_ndx.apply(np.float)) > 0.0) | (np.abs(df.lhs_pdx.apply(np.float)) > 0.0) |
               (np.abs(df.rhs_ndx.apply(np.float)) > 0.0) | (np.abs(df.rhs_pdx.apply(np.float)) > 0.0)]

def args_get_labeled(df):
    return df[(df.lhs_label != 0) | (df.rhs_label != 0)]

def args_get_nonzero(df):
    return df[(np.abs(df.ndx.apply(np.float)) > 0.0) | (np.abs(df.pdx.apply(np.float)) > 0.0) ]