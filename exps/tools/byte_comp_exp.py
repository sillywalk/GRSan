import pandas as pd
import numpy as np
from subprocess import run, DEVNULL
import os, sys
from glob import glob
from tqdm import tqdm_notebook, tqdm
import grad_utils as gutils
import programs, argparse, tempfile

import eval_gradient as eg

def get_branch(df, f_id, b_id):
    return df[(df.file_id == f_id) &(df.inst_id == b_id)]

def test_byte(program, byte_ind, orig_trace, infile):
    changes = [0, 255] + [1,2,4,8,16,32,64,128]# + list(range(1,254))
    actual_branches = []
    
    
    test_branches = [ind for ind, _ in orig_trace.groupby(['file_id', 'inst_id']).agg(lambda x:()).iterrows()]
    

    _, ext = os.path.splitext(infile)
    tmpfile = 'input' + ext
    
    for change in changes:
        
        with open(infile, 'rb') as tf:
            blob_data = bytearray(tf.read())
        if change in [0, 255]:
            blob_data[byte_ind] = change
        else:
            blob_data[byte_ind] = blob_data[byte_ind] ^ change

        with open(tmpfile, 'wb') as outfile:
            outfile.write(blob_data)

        # run([program, "taint", '0', tmpfile], stdout=DEVNULL, stderr=DEVNULL)

        env = os.environ.copy()
        env['DFSAN_OPTIONS'] = "func_logfile=''" # turn off func recording
        # print(programs.get_cmd(program, programs.TAINT, byte_ind))
        run(programs.get_cmd(program, programs.TAINT, tmpfile, byte_ind), env=env, 
                stdout=DEVNULL, stderr=DEVNULL)
        


        # load branches, check if any branch values changed
        try:
          trace = pd.read_csv('branches.csv')
        
          result = {}
          
                  
          for (f_id, b_id) in test_branches:
              
              if (f_id, b_id) in actual_branches:
                  continue # already found this branch
                  
              orig_trace_b = get_branch(orig_trace, f_id, b_id)
              trace_b = get_branch(trace, f_id, b_id)
          
              for i in range((len(trace_b))):
                  if i < len(orig_trace_b):
                      row = trace_b.iloc[i]
                      origrow = orig_trace_b.iloc[i]

                      if (row.lhs_val != origrow.lhs_val or 
                          row.rhs_val != origrow.rhs_val):
                          actual_branches.append((f_id, b_id))
                          break
        except Exception as e:
          print('Branch check error!', e)
               
    actual_branches = [(byte_ind, f_id, b_id, 1) for (f_id, b_id) in actual_branches]
    return actual_branches


def test_bytes(program, infile, working_dir='/tmp/'):

    cwd = os.getcwd()
    print(infile)
    infile = os.path.abspath(infile)
    print(infile)

    df_actual = pd.DataFrame()

    with tempfile.TemporaryDirectory(prefix=working_dir) as run_dir:
        os.chdir(run_dir)

        _, ext = os.path.splitext(infile)
        tmpfile = 'input' + ext
        
        # get trace:
        run(['cp', infile, tmpfile])
        
        
        result = []
                     
        infile_len = os.path.getsize(infile)
        print('evaluating input bytes for', infile)
        for byte_ind in tqdm(range(infile_len)):
            cmd = programs.get_cmd(program, programs.TAINT, infile, byte_ind)
            run(cmd, stdout=DEVNULL, stderr=DEVNULL)
            baseline_trace = pd.read_csv('branches.csv')
            
            actual_branches = test_byte(program, byte_ind, baseline_trace, infile)
            result.extend(actual_branches)
            
        df_actual = pd.DataFrame(result)
        df_actual.columns = ['deriv_byte', 'file_id', 'inst_id', 'actual']


    os.chdir(cwd)

    return df_actual

def set_floats(df):
    for fcol in ['lhs_val', 'rhs_val', 'lhs_pdx', 'lhs_ndx', 'rhs_pdx', 'rhs_ndx']:
        try:
            df[fcol] = df[fcol].apply(np.float)
        except Exception as e:
            print(e)
            print(fcol)
            raise e
        
    return df


def per_byte_stats(pred_df):
    pred_byte_g = pred_df.groupby('deriv_byte').agg(tuple).reset_index()
    pred_byte_g['grad_precision'] = 0.0
    pred_byte_g['grad_recall'] = 0.0
    pred_byte_g['taint_precision'] = 0.0
    pred_byte_g['taint_recall'] = 0.0
    
    for i in range(len(pred_byte_g)):
        row = pred_byte_g.loc[i]
        grad_preds = [(f_id, b_id) for (f_id, b_id, pred) in zip(row.file_id, row.inst_id, row.grad_pred) if pred == 1]
        taint_preds = [(f_id, b_id) for (f_id, b_id, pred) in zip(row.file_id, row.inst_id, row.taint_pred) if pred == 1]
        actual = [(f_id, b_id) for (f_id, b_id, pred) in zip(row.file_id, row.inst_id, row.actual) if pred == 1]
        grad_preds = set(grad_preds)
        taint_preds = set(taint_preds)
        actual = set(actual)
        
        pred_byte_g.loc[i, 'grad_precision'] = gutils.precision(grad_preds, actual)
        pred_byte_g.loc[i, 'grad_recall'] = gutils.recall(grad_preds, actual)
        pred_byte_g.loc[i, 'taint_precision'] = gutils.precision(taint_preds, actual)
        pred_byte_g.loc[i, 'taint_recall'] = gutils.recall(taint_preds, actual)

    return pred_byte_g


def per_branch_stats(pred_df):
    pred_byte_g = pred_df.groupby(['file_id', 'inst_id']).agg(tuple).reset_index()
    pred_byte_g['grad_precision'] = 0.0
    pred_byte_g['grad_recall'] = 0.0
    pred_byte_g['taint_precision'] = 0.0
    pred_byte_g['taint_recall'] = 0.0
    
    for i in range(len(pred_byte_g)):
        row = pred_byte_g.loc[i]
        grad_preds = [byte_ind for (byte_ind, pred) in zip(row.deriv_byte, row.grad_pred) if pred == 1]
        taint_preds = [byte_ind for (byte_ind, pred) in zip(row.deriv_byte, row.taint_pred) if pred == 1]
        actual = [byte_ind for (byte_ind, pred) in zip(row.deriv_byte, row.actual) if pred == 1]
        grad_preds = set(grad_preds)
        taint_preds = set(taint_preds)
        actual = set(actual)
        
        pred_byte_g.loc[i, 'grad_precision'] = gutils.precision(grad_preds, actual)
        pred_byte_g.loc[i, 'grad_recall'] = gutils.recall(grad_preds, actual)
        pred_byte_g.loc[i, 'taint_precision'] = gutils.precision(taint_preds, actual)
        pred_byte_g.loc[i, 'taint_recall'] = gutils.recall(taint_preds, actual)

    return pred_byte_g


def run_byte_comp(program, dataset_path, working_dir='/tmp/'):
    preds_list = []
    byte_stats_list = []
    branch_stats_list = []
    byte_stats_grad_only_list = []
    branch_stats_grad_only_list = []

    dataset_path = dataset_path.rstrip('/')
    files = glob(dataset_path+'/*')
    for file in files:
        fname = os.path.basename(file)
#         grad_df = eg.eval_grad(program, file)
#         taint_df = eg.eval_taint(program, file)
        grad_df = pd.read_csv(dataset_path+'_grad/'+fname+'.csv')
        taint_df = pd.read_csv(dataset_path+'_taint/'+fname+'.csv')
        
        grad_df = set_floats(grad_df)
        taint_df = set_floats(taint_df)
        
        try:
            grad_nz = gutils.get_nonzero(grad_df)
            taint_l = gutils.get_labeled(taint_df)
        except Exception as e:
            print(e)
            grad_df.to_csv(fname+'_grad_err.csv')
            taint_df.to_csv(fname+'_taint_err.csv')
        
#         df = test_branches(program, grad_df_nz, file)
        actual_df = test_bytes(program, file, working_dir=working_dir)
        actual_df.to_csv(dataset_path+'/../actual_df.csv')
        print('aggregating comp results for', dataset_path)
    
        grad_pred = grad_nz[['deriv_byte', 'file_id', 'inst_id']]
        grad_pred.insert(3, 'grad_pred', 1)
        
        taint_pred = taint_l[['deriv_byte', 'file_id', 'inst_id']]
        taint_pred.insert(3, 'taint_pred', 1)

        
        actual_pred = actual_df.set_index(['deriv_byte', 'file_id', 'inst_id'])
        taint_pred = taint_pred.set_index(['deriv_byte', 'file_id', 'inst_id'])
        grad_pred = grad_pred.set_index(['deriv_byte', 'file_id', 'inst_id'])
        
        print(grad_pred)
        print(taint_pred)
        print(actual_pred)
        preds = pd.concat([grad_pred, taint_pred, actual_pred], axis=1)
        preds = preds.fillna(0)
        preds = preds.reset_index()
        
        byte_stats = per_byte_stats(preds)
        branch_stats = per_branch_stats(preds)
        
        byte_stats_grad_only = per_byte_stats(preds[preds.grad_pred == 1])
        branch_stats_grad_only = per_branch_stats(preds[preds.grad_pred == 1])
    
        preds['file'] = fname
        byte_stats['file'] = fname
        branch_stats['file'] = fname
        byte_stats_grad_only['file'] = fname
        branch_stats_grad_only['file'] = fname
        
        preds_list.append(preds)
        byte_stats_list.append(byte_stats)
        branch_stats_list.append(branch_stats)
        byte_stats_grad_only_list.append(byte_stats_grad_only)
        branch_stats_grad_only_list.append(branch_stats_grad_only)
        
    return pd.concat(preds_list), pd.concat(byte_stats_list), pd.concat(branch_stats_list),\
            pd.concat(byte_stats_grad_only_list), pd.concat(branch_stats_grad_only_list)

def main(argv=sys.argv[1:]):
    # if len(sys.argv) != 3:
        # print("usage: python comp_exp.py program dataset_dir")
        # sys.exit(1)
    # program = sys.argv[1]
    # dataset_path = sys.argv[2]

    parser = argparse.ArgumentParser()
    parser.add_argument('program', choices=programs.valid_programs)
    parser.add_argument('comp_input', help='target directory of fidataset_nameles')
    parser.add_argument('--working-dir', dest='working_dir', default="/dev/shm/",
            help='base dir to use for working tmp dirs')
    args = parser.parse_args(argv)

    program = args.program
    dataset_path = args.comp_input
    working_dir = args.working_dir

    
    if os.path.isdir(dataset_path):
        dataset_files = glob(dataset_path+'/*')
#         dataset_name = dataset_path.rstrip('/').split('/')[-1]
        dataset_base, dataset_name = os.path.split(dataset_path.rstrip('/'))
    elif os.path.isfile(dataset_path):
        print('run on directory!')
        sys.exit(1)
    else:
        print('Invalid path not directory or file!', dataset_path)
        sys.exit(1)
        
    # first check if _grad and _taint are set up:
    grad_dir = dataset_base+'/'+dataset_name+'_grad'
    taint_dir = dataset_base+'/'+dataset_name+'_taint'
    if not os.path.isdir(grad_dir):
        print('generating gradient dir for dataset', dataset_path)
        eg.eval_dir('grad', program, dataset_base+'/'+dataset_name)
        
    if not os.path.isdir(taint_dir):
        print('generating taint dir for dataset', dataset_path)
        eg.eval_dir('taint', program, dataset_base+'/'+dataset_name)
    
    preds, byte_stats, branch_stats, byte_stats_grad, branch_stats_grad = run_byte_comp(program, dataset_base+'/'+dataset_name, working_dir=working_dir)
    
    
    byte_summary = gutils.stat_summary(byte_stats)
    branch_summary = gutils.stat_summary(branch_stats)
    byte_grad_summary = gutils.stat_summary(byte_stats_grad)
    branch_grad_summary = gutils.stat_summary(branch_stats_grad)
    
    preds.to_csv('preds.'+program+'.csv')
    byte_stats.to_csv('byte_stats.'+program+'.csv')
    branch_stats.to_csv('branch_stats.'+program+'.csv')
    byte_stats_grad.to_csv('byte_stats_grad.'+program+'.csv')
    branch_stats_grad.to_csv('branch_stats_grad.'+program+'.csv')
    
    byte_summary.to_csv('byte_summary.'+program+'.csv')
    branch_summary.to_csv('branch_summary.'+program+'.csv')
    byte_grad_summary.to_csv('byte_grad_summary.'+program+'.csv')
    branch_grad_summary.to_csv('branch_grad_summary.'+program+'.csv')


if __name__ == '__main__':
    main()
