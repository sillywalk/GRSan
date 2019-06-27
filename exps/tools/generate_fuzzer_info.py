import random
import numpy as np
import pandas as pd
# import comp_exp as cpe
import sys, os, argparse
from glob import glob
import math

def get_labeled(df):
    return df[(df.lhs_label != 0) | (df.rhs_label != 0)]

def get_nonzero(df):
    return df[(np.abs(df.lhs_ndx.apply(np.float)) > 0.0) | (np.abs(df.lhs_pdx.apply(np.float)) > 0.0) |
               (np.abs(df.rhs_ndx.apply(np.float)) > 0.0) | (np.abs(df.rhs_pdx.apply(np.float)) > 0.0)]


def gen_taint_info_single_mode2(mode, df1, fname):
    df = df1
    if mode == 'grad':
        processed_df = get_nonzero(df)
    else:
        processed_df = df
    hot_bytes = processed_df.groupby(["deriv_byte", 'file_id', 'inst_id']).agg(lambda x: tuple(x)).groupby(['deriv_byte']).size().sort_values(ascending=False)

    k_bytes = len(hot_bytes)
    #k_bytes = min(len(hot_bytes), len(hot_bytes2))
    if(k_bytes > 512):
        k_bytes = 512
    print('hot bytes num' + str(k_bytes))
    c_iter = int(math.log(k_bytes,2))
    col1 = list(hot_bytes.index[:k_bytes])
    if mode == 'grad':
        # check deriv for each byte and take the max among all options
        deriv_for_byte = {}
        for idx, row in processed_df.groupby(["deriv_byte", 'file_id', 'inst_id']).agg([lambda x: tuple(x)]).iterrows():
            current_max = 0
            for x in row.rhs_ndx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            for x in row.rhs_pdx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            for x in row.lhs_ndx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            for x in row.lhs_pdx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            deriv_for_byte[idx[0]] = current_max

        final_changes_per_byte = {}
        for key, val in deriv_for_byte.items():
            if val >= 0.0:
                final_changes_per_byte[key] = 1
            else:
                final_changes_per_byte[key] = -1
        col2 = [final_changes_per_byte[byte] for byte in col1]
    else:
        col2 = [random.choice([1, -1]) for byte in col1]
    return col1, col2, fname, c_iter

def gen_taint_info_single_mode(mode, df1, fname):
    df = df1
    if mode == 'grad':
        processed_df = get_nonzero(df)
    else:
        processed_df = df
    hot_bytes = processed_df.groupby(["deriv_byte", 'file_id', 'inst_id']).agg(lambda x: tuple(x)).groupby(['deriv_byte']).size().sort_values(ascending=False)

    k_bytes = len(hot_bytes)
    #k_bytes = min(len(hot_bytes), len(hot_bytes2))
    if(k_bytes > 512):
        k_bytes = 512
    print('hot bytes num' + str(k_bytes))
    c_iter = int(math.log(k_bytes,2))
    col1 = list(hot_bytes.index[:k_bytes])

    col2 = [random.choice([1, -1]) for byte in col1]
    return col1, col2, fname, c_iter

def gen_taint_info(mode, df1, fname, df2):
    #if k_bytes is None:
    #    k_bytes = os.path.getsize(fname) // 8
    df = df1
    if mode == 'grad':
        processed_df = get_nonzero(df)
        other_processed_df = get_labeled(df2)
    elif mode == 'taint':
        processed_df = get_labeled(df)
        other_processed_df = get_nonzero(df2)
    else:
        raise Exception("mode must be taint or grad")

    #import ipdb
    #ipdb.set_trace()
    # bytes -> count
    hot_bytes = processed_df.groupby(["deriv_byte", 'file_id', 'inst_id']).agg(lambda x: tuple(x)).groupby(['deriv_byte']).size().sort_values(ascending=False)

    hot_bytes2 = other_processed_df.groupby(["deriv_byte", 'file_id', 'inst_id']).agg(lambda x: tuple(x)).groupby(['deriv_byte']).size().sort_values(ascending=False)
    # get top K bytes
    k_bytes = min(len(hot_bytes), len(hot_bytes2))
    if(k_bytes > 1000):
        k_bytes = 512
    c_iter = int(math.log(k_bytes,2))
    col1 = list(hot_bytes.index[:k_bytes])

    final_changes_per_byte = {}
    import time
    t0 = time.time()
    if(False):
    #if mode == 'grad':
        # check deriv for each byte and take the max among all options
        deriv_for_byte = {}
        for idx, row in processed_df.groupby(["deriv_byte", 'file_id', 'inst_id']).agg([lambda x: tuple(x)]).iterrows():
            current_max = 0
            for x in row.rhs_ndx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            for x in row.rhs_pdx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            for x in row.lhs_ndx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
            for x in row.lhs_pdx[0]:
                x = float(x)
                if np.abs(current_max) <= np.abs(x):
                    current_max = x
#            ln = tuple([float(x) for x in row.lhs_ndx[0]])
#            lp = tuple([float(x) for x in row.lhs_pdx[0]])
#            rn = tuple([float(x) for x in row.rhs_ndx[0]])
#            rp = tuple([float(x) for x in row.rhs_pdx[0]])
            #             if sum([np.mean(ln) + np.mean(lp) + np.mean(rn) + np.mean(rp)]) != 0.0:
#            deriv_for_byte[idx[0]] = np.mean(ln) + np.mean(lp) + np.mean(rn) + np.mean(rp)
            deriv_for_byte[idx[0]] = current_max

        final_changes_per_byte = {}
        for key, val in deriv_for_byte.items():
            if val >= 0.0:
                final_changes_per_byte[key] = 1
            else:
                final_changes_per_byte[key] = -1
        col2 = [final_changes_per_byte[byte] for byte in col1]
    else:
        col2 = [random.choice([1, -1]) for byte in col1]
    return col1, col2, fname, c_iter

def label_dir_single_mode(mode, file_dir, grad_dir, k_bytes):

    print("Generating taint_info_p under %s" % (str(mode)))
    with open("taint_info_p", 'w') as csvfile:
        file_list = glob(file_dir+'/*')
        #for f in glob(file_dir+'/*'):
        for f in file_list:
            fname = os.path.basename(f)
            #if fname not in ['/local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf/id:000291,src:000000,op:havoc,rep:128,+cov']:
            #    continue
            #continue
            print( fname)
            csvname = grad_dir+'/'+fname+'.csv'
            df1 = pd.read_csv(csvname)
            if mode == 'grad':
                processed_df = get_nonzero(df1)
                if(len(processed_df) == 0):
                    continue
            col1, col2, fname, c_iter = gen_taint_info_single_mode2(mode, df1, f)
            for val in col1:
                csvfile.write(str(val))
                csvfile.write(",")

            csvfile.write("|")
            for val in col2:
                csvfile.write(str(val))
                csvfile.write(",")
            csvfile.write('|')
            fname = 'seeds/' + fname.split('/')[-1]
            csvfile.write(fname)
            csvfile.write('|')
            csvfile.write(csvname)
            csvfile.write('|')
            csvfile.write(str(c_iter))
            csvfile.write("\n")

def label_dir(mode, file_dir, grad_dir, k_bytes, other_dir):

    print("Generating taint_info_p under %s" % (str(mode)))
    with open("taint_info_p", 'w') as csvfile:

        file_list = glob(file_dir+'/*')
        #for f in glob(file_dir+'/*'):
        for f in file_list:
            fname = os.path.basename(f)
            #if fname not in ['/local/dongdong/gradtest/gradtest/exps/programs/readelf/inputs/afl_out/readelf/id:000291,src:000000,op:havoc,rep:128,+cov']:
            #    continue
            #continue
            print( fname)
            csvname = grad_dir+'/'+fname+'.csv'
            df1 = pd.read_csv(csvname)
            df2 = pd.read_csv(other_dir+'/'+ fname+'.csv')
            if mode == 'grad':
                processed_df = get_nonzero(df1)
                other_processed_df = get_labeled(df2)
            elif mode == 'taint':
                processed_df = get_labeled(df1)
                other_processed_df = get_nonzero(df2)
            else:
                raise Exception("mode must be taint or grad")
            if(len(processed_df) == 0) or (len(other_processed_df)==0):
                continue

            col1, col2, fname, c_iter = gen_taint_info(mode, df1, f, df2)
            for val in col1:
                csvfile.write(str(val))
                csvfile.write(",")

            csvfile.write("|")
            for val in col2:
                csvfile.write(str(val))
                csvfile.write(",")
            csvfile.write('|')
            csvfile.write(fname)
            csvfile.write('|')
            csvfile.write(csvname)
            csvfile.write('|')
            csvfile.write(str(c_iter))
            csvfile.write("\n")

def label_dir2(mode, file_dir, grad_dir, k_bytes):

    cnt = 0
    for f in glob(file_dir+'/*'):
        fname = os.path.basename(f)
        csvname = grad_dir+'/'+fname+'.csv'
        label_file(mode, f, csvname, k_bytes, new_name="taint_info_p%s" % (str(cnt)))
        cnt += 1

def label_file(mode, fname, grad_file, k_bytes, new_name="taint_info_p"):

    print("Generating taint_info_p under %s" % (str(mode)))
    print(grad_file)
    col1, col2, _ = gen_taint_info(mode, pd.read_csv(grad_file), fname, k_bytes)

    with open(new_name, 'w') as csvfile:
        for val in col1:
            csvfile.write(str(val))
            csvfile.write(",")

        csvfile.write("|")
        for val in col2:
            csvfile.write(str(val))
            csvfile.write(",")
        csvfile.write('|')
        csvfile.write(fname)
        csvfile.write('|')
        csvfile.write(grad_file)
        csvfile.write("\n")


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['grad', 'taint', 'both'])
    parser.add_argument('datafile')
    parser.add_argument('infile', help='target file or directory of files')
    parser.add_argument('--kbytes', dest='kbytes', help='number hot bytes to select',
            type=int, default=None)
    args = parser.parse_args(argv)

    mode = args.mode
    dfname = args.datafile
    fname = args.infile
    k_bytes = args.kbytes

    if os.path.isdir(fname):
        label_dir2(mode, fname, dfname, k_bytes)
    else:
        label_file(mode, fname, dfname, k_bytes)


if __name__ == "__main__":
    main()

