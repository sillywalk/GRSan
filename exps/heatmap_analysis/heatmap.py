import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import re, tables, argparse
from subprocess import call


def heatmap(exp_name, drop_cache=False, var_name=None, robust=False, save_data=False):

    with pd.HDFStore('store.h5') as store:
        if (args.drop_cache or '/'+exp_name not in store.keys()):
            print('loading data from '+exp_name+'/')

            dfs = []
            for f in glob(exp_name+'/*.csv'):
                df = pd.read_csv(f, header=None)
                
                m = re.search(r'd_(\d+).csv', f)
                if (m.groups()):
                    i = int(m.groups()[0])
                    
                    df[5] = i
                    df[6] = df.index
                    
                    dfs.append(df)
                    print('loaded '+f)

            df = pd.concat(dfs)
            df = df.reset_index(drop=True)
            df.columns = ('ins', 'val', 'lbl', 'ndx', 'pdx', 'xind', 'yind')

            store[exp_name] = df

        else:
            df = store[exp_name]

    if (save_data):
        call(['mkdir', 'saved_data'])
        df.to_csv('saved_data/'+exp_name+'.csv')

    if (var_name):
        df = df[df.ins == var_name]
    df.yind = df.yind - df.yind.min()

    # print(df)


    nx = df.xind.max() + 1
    ny = df.yind.max() + 1
    ndx = np.zeros((nx, ny))
    pdx = np.zeros((nx, ny))
    vals = np.zeros((nx, ny))

    for row in df.itertuples():
    #     print(row)
        ndx[row.xind, row.yind] = row.ndx
        pdx[row.xind, row.yind] = row.pdx
        vals[row.xind, row.yind] = row.val

    call(['mkdir', '-p', 'figs/'+exp_name])

    plt.figure(figsize=(8,6))
    sns.heatmap(ndx, robust=robust)
    plt.title('Zlib hash chain heatmap neg deriv')
    plt.xlabel('Hash chain indices')
    plt.ylabel('Input indices')
    plt.savefig('figs/'+exp_name+'/'+'ndx_heatmap.png')

    plt.figure(figsize=(8,6))
    sns.heatmap(pdx, robust=robust)
    plt.title('Zlib hash chain heatmap pos deriv')
    plt.xlabel('Hash chain indices')
    plt.ylabel('Input indices')
    plt.savefig('figs/'+exp_name+'/'+'pdx_heatmap.png')

    plt.figure(figsize=(8,3))
    sns.heatmap(vals, robust=robust)
    plt.title('Zlib hash chain heatmap values')
    plt.xlabel('Hash chain indices')
    plt.ylabel('Input indices')
    plt.savefig('figs/'+exp_name+'/'+'vals_heatmap.png')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("exp_name")
    parser.add_argument("-f", dest='drop_cache', action='store_true')
    parser.add_argument("-n", dest='var_name', default=None)
    parser.add_argument("-r", "--robust", dest='robust', action='store_true')
    parser.add_argument("-s", "--save-data", dest='save_data', action='store_true')
    args = parser.parse_args()

    print('args:', args)
    heatmap(args.exp_name, args.drop_cache, args.var_name, args.robust, args.save_data)

