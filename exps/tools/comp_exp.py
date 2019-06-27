import pandas as pd
import tempfile
import numpy as np
from subprocess import run, DEVNULL
import os, sys
from glob import glob
from tqdm import tqdm_notebook, tqdm
from grad_utils import *
import programs, argparse

import eval_gradient as eg


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




def test_branch(program, f_id, b_id, orig_trace, byte_inds, infile):
    changes = [0, 255] + [1,2,4,8,16,32,64,128]# + list(range(1,254))
    valid_byte_inds = []
    
    orig_trace_b = orig_trace[(orig_trace.file_id == f_id) & (orig_trace.inst_id == b_id)]

    _, ext = os.path.splitext(infile)
    tmpfile = 'input' + ext
    # for byte index

    orig_blob_data = None
    with open(infile, 'rb') as tf:
        orig_blob_data = bytearray(tf.read())
 

    for byte_ind in byte_inds:
        # for 0, 255, other changes?
        found = False
        for change in changes:
            # read and modify template, write output
            blob_data = bytearray(orig_blob_data)
            if change in [0, 255]:
                blob_data[byte_ind] = change
            else:
                blob_data[byte_ind] = blob_data[byte_ind] ^ change
            
            with open(tmpfile, 'wb') as outfile:
                outfile.write(blob_data)
            
            # run([program, "taint", '0', tmpfile])

            env = os.environ.copy()
            env['DFSAN_OPTIONS'] = "func_logfile='',always_record_branches=1" # turn off func recording
            run(programs.get_cmd(program, programs.GRAD, tmpfile), env=env, 
                    stdout=DEVNULL, stderr=DEVNULL)
            
            # load branches, check if any branch values changed
            trace = pd.read_csv('branches.csv')
            trace_b = trace[(trace.file_id == f_id) &(trace.inst_id == b_id)]

            for i in range((len(trace_b))):
                if i < len(orig_trace_b):
                    row = trace_b.iloc[i]
                    origrow = orig_trace_b.iloc[i]

                    if (row.lhs_val != origrow.lhs_val or 
                        row.rhs_val != origrow.rhs_val):
                        valid_byte_inds.append(byte_ind)
                        found = True
                        break
            if found:
                break
                
    return valid_byte_inds
                        
def test_branches(program, df, infile, args):
    # get labels:
    df_l = get_labeled(df)

    _, ext = os.path.splitext(infile)
    tmpfile = 'input' + ext

    df_l_g = None

    work_dir = '/dev/shm/'
    # if program == 'jpeg':
        # work_dir = '/tmp/'

    infile = os.path.abspath(infile)
    fsize = os.path.getsize(infile)

    cwd = os.getcwd()
    with tempfile.TemporaryDirectory(prefix=work_dir) as run_dir:
        os.chdir(run_dir)
        
        # get trace:
        print(infile, tmpfile)

        run(['cp', infile, tmpfile])
        # run([program, "taint", '1000000', tmpfile])

        env = os.environ.copy()
        env['DFSAN_OPTIONS'] = "func_logfile='',always_record_branches=1" # turn off func recording
        print(programs.get_cmd(program, programs.GRAD, tmpfile))
        res = run(programs.get_cmd(program, programs.GRAD, tmpfile), env=env, stdout=DEVNULL)

        if res.returncode:
            print('ERROR RUNNING BASELINE:', res.returncode)
            print(res.stderr.decode('utf-8', 'ignore'))
        # baseline_trace_df = pd.read_csv('branches.csv')

        baseline_trace = pd.read_csv('branches.csv')
        
        result = []
        
        df_l_g = df_l.groupby(['file_id', 'inst_id']).agg(lambda x: tuple(x))

        for (f_id, b_id), row in tqdm(df_l_g.iterrows(), total=df_l_g.shape[0]):
            
            # test_bytes = row.deriv_byte
            # if args.all_bytes:
            test_bytes = list(range(fsize))
            # print(test_bytes, row)
            # print(len(test_bytes), len(fsize))
            
            valid_bytes = test_branch(program, f_id, b_id, baseline_trace, test_bytes, infile)
            result.append(valid_bytes)


        df_l_g['valid_bytes'] = pd.Series(result, df_l_g.index)

    os.chdir(cwd)
    return df_l_g


def set_floats(df):
    for fcol in ['lhs_val', 'rhs_val', 'lhs_pdx', 'lhs_ndx', 'rhs_pdx', 'rhs_ndx']:
        try:
            df[fcol] = df[fcol].apply(np.float)
        except Exception as e:
            print(e)
            print(fcol)
            raise e
        
    return df

def run_comp(program, files, args):
    grad_data = []
    taint_data = []
    results = []
    for file in files:
        print(file)
        file = os.path.abspath(file)
        dataset_path = os.path.dirname(file)
        fname = os.path.basename(file)
        # grad_df = eg.eval_grad(program, file)
        # taint_df = eg.eval_taint(program, file)
        grad_path = dataset_path  +'_grad/'
        taint_path = dataset_path  + '_taint/'

        try:
            grad_df = pd.read_csv(grad_path + fname + '.csv')
        except FileNotFoundError:
            grad_df, _, _ = eg.process_file('grad', program, dataset_path+'/'+fname, record_funcs=False)
            run(['mkdir', grad_path])
            grad_df.to_csv(grad_path+'/'+fname+'.csv')

        try:
            taint_df = pd.read_csv(taint_path + fname + '.csv')
        except FileNotFoundError:
            taint_df, _, _ = eg.process_file('taint', program, dataset_path+'/'+fname, record_funcs=False)
            run(['mkdir', taint_path])
            taint_df.to_csv(taint_path+'/'+fname+'.csv')
        

        
        grad_df = set_floats(grad_df)
        taint_df = set_floats(taint_df)
        
        try:
            grad_df_l = get_labeled(grad_df)
            grad_df_nz = get_nonzero(grad_df_l)
            taint_df_l = get_labeled(taint_df)
        except Exception as e:
            print(e)
            grad_df.to_csv(fname+'_grad_err.csv')
            taint_df.to_csv(fname+'_taint_err.csv')
            continue

        print(file)
        df = test_branches(program, pd.concat((grad_df_nz, taint_df_l)), file, args)

        taint_df_l_g = taint_df_l.groupby(['file_id', 'inst_id']).agg(lambda x: tuple(x))
        df = df.assign(taint_bytes=taint_df_l_g.deriv_byte)
        
        grad_df_nz_g = grad_df_nz.groupby(['file_id', 'inst_id']).agg(lambda x: tuple(x))
        df = df.assign(grad_bytes=grad_df_nz_g.deriv_byte)

        df['taint_precision'] = df.apply(lambda row: precision(row.taint_bytes, row.valid_bytes), axis=1)
        df['taint_recall'] = df.apply(lambda row: recall(row.taint_bytes, row.valid_bytes), axis=1)
        df['grad_precision'] = df.apply(lambda row: precision(row.grad_bytes, row.valid_bytes), axis=1)
        df['grad_recall'] = df.apply(lambda row: recall(row.grad_bytes, row.valid_bytes), axis=1)
    
        df['file'] = os.path.basename(file)
        
        
        results.append(df)
        grad_data.append(grad_df_l)
        taint_data.append(taint_df_l)
        
        
    return pd.concat(results), pd.concat(grad_data), pd.concat(taint_data)



def main(argv=sys.argv[1:]):
    # if len(sys.argv) != 3:
        # print("usage: python comp_exp.py program dataset_dir")
        # sys.exit(1)
    # program = sys.argv[1]
    # dataset_path = sys.argv[2]

    parser = argparse.ArgumentParser()
    parser.add_argument('program', choices=programs.valid_programs)
    parser.add_argument('comp_input', help='target directory of fidataset_nameles')
    parser.add_argument('-a', dest='all_bytes', action='store_true')
    args = parser.parse_args(argv)

    program = args.program
    dataset_path = args.comp_input


    
    if os.path.isdir(dataset_path):
        dataset_files = glob(dataset_path+'/*')
        dataset_name = dataset_path.strip('/').split('/')[-1]
    elif os.path.isfile(dataset_path):
        dataset_files = [dataset_path]
        dataset_name = os.path.basename(dataset_path)
    else:
        print('Invalid path not directory or file!', dataset_path)
        sys.exit(1)
    
    results, grad_data, taint_data = run_comp(program, dataset_files, args)
    summary = stat_summary(results)

    grad_data.to_csv('grad_data.'+dataset_name+'.csv')
    taint_data.to_csv('taint_data.'+dataset_name+'.csv')
    results.to_csv('comp_results.'+dataset_name+'.csv')
    summary.to_csv('comp_summary.'+dataset_name+'.csv')

    print(summary)


if __name__ == '__main__':
    main()
