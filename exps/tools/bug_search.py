import pandas as pd
import numpy as np
from subprocess import CalledProcessError, run
import sys, os
from os import path
from tqdm import tqdm
from glob import glob
from joblib import Parallel, delayed
import eval_gradient as eg
import argparse, itertools
import uuid, json

# grab next adjacent
def split_adj(dbytes):
    if len(dbytes) == 1:
        return dbytes, []
    
    for i, b in enumerate(dbytes[1:]):
        if (dbytes[i] + 1 != b):
            return dbytes[:i+1], dbytes[i+1:]
        
    return dbytes, []


def adj_search(orig_input, func_df):
    dfnz = func_df[(np.abs(func_df.ndx) >= 0.1) & (np.abs(func_df.pdx) >= 0.1)]
    dbytes = sorted(dfnz.deriv_byte.unique())
    test_inputs = []
    summaries = []
    while dbytes:
        adj_b, dbytes = split_adj(dbytes)
        print(adj_b)
        for c in (0, 255):
            test_input = bytearray(orig_input)
            for b in adj_b:
                test_input[b] = c
            test_inputs.append(test_input)
            summaries.append(str((adj_b, [c for b in adj_b])))
    return test_inputs, summaries

def get_combs2(items, md):
    combs = []
    for i, item in enumerate(items):
        for item2 in items[i+1:i+md+1]:
            combs.append((item, item2))
    return combs

def get_combs3(items, md):
    combs = []
    for i, item in enumerate(items):
        for j, item2 in enumerate(items[i+1:i+md]):
            for k, item3 in enumerate(items[j+1:i+md+1]):
                combs.append((item, item2, item3))
    return combs


def adj_comb2_search(orig_input, func_df):
    dfnz = func_df[(np.abs(func_df.ndx) >= 0.1) | (np.abs(func_df.pdx) >= 0.1)]
    dbytes = sorted(dfnz.deriv_byte.unique())
    test_inputs = []
    adj_bytes = []
    while dbytes:
        adj_b, dbytes = split_adj(dbytes)
        adj_bytes.append(adj_b)
    for comb in get_combs2(adj_bytes, 4):
        for cs in itertools.product((0, 255), (0, 255)):
            test_input = bytearray(orig_input)
            for adj_b, c in zip(comb, cs):
                for b in adj_b:
                    test_input[b] = c
            test_inputs.append(test_input)
    return test_inputs


def adj_comb3_search(orig_input, func_df):
    dfnz = func_df[(np.abs(func_df.ndx) >= 0.1) | (np.abs(func_df.pdx) >= 0.1)]
    dbytes = sorted(dfnz.deriv_byte.unique())
    test_inputs = []
    adj_bytes = []
    while dbytes:
        adj_b, dbytes = split_adj(dbytes)
        adj_bytes.append(adj_b)
    for comb in get_combs3(adj_bytes, 3):
        for cs in ((0, 0, 0), (255, 255, 255)):
            test_input = bytearray(orig_input)
            for adj_b, c in zip(comb, cs):
                for b in adj_b:
                    test_input[b] = c
            test_inputs.append(test_input)
    return test_inputs


def per_byte_search(orig_input, func_df):
    test_inputs = []
    for b in func_df.deriv_byte.unique():
        new_input = bytearray(orig_input)
        for c in (0, 255):
            new_input[b] = c
            test_inputs.append( new_input)
    return test_inputs


def bug_search(mode, wrapper_exe, func_arg_df, crash_dir, infile):
    if (len(func_arg_df) == 0):
        print('no data for '+infile+'!')
        return

    
    _, ext = path.splitext(infile)
    infilename = os.path.basename(infile)
    
    tmpfile = uuid.uuid4().hex + ext
    
    with open(infile, 'rb') as tf:
        orig_fdata = bytearray(tf.read())
   
    crash_i = 0
    with open('bug.log', 'w') as logf:
        with open(crash_dir+'/'+infilename+'.summary', 'w') as summaryf:
            # test_inputs = per_adj_search(orig_fdata, func_arg_df)
            test_inputs, change_summaries = adj_search(orig_fdata, func_arg_df)
            for test_input, change_summary in tqdm(zip(test_inputs, change_summaries)):
                logf.write('bytes ' + str(test_input) + "\n")
                      
                with open(tmpfile, 'wb') as outfile:
                    outfile.write(test_input)

                logf.write(str(test_input) + "\n")
                    
                # capture output
                try:
                    res = run([wrapper_exe, "bug", '0', tmpfile], capture_output=True, check=True)
                except CalledProcessError as e:
                    stdout = e.stdout.decode('utf-8')
                    stderr = e.stderr.decode('utf-8')
                    logf.write('ret:'+ str(e.returncode) + "\n")
                    logf.write(stdout + "\n")
                    logf.write(stderr + "\n")
                    if ("Sanitizer" in stdout or "Sanitizer" in stderr):
                        summary = [line for line in stderr.split("\n") if "SUMMARY" in line]
                        summaryf.write(json.dumps({'input':change_summary, 'summary':summary}) + "\n")
                        # print('bug!', end='')
                        # if error, save input + output to crashes dir
                        with open(crash_dir+'/'+infilename+'.input.'+str(crash_i), 'wb') as outfile:
                            outfile.write(test_input)
                        # with open(crash_dir+'/'+infilename+'.stdout.'+str(crash_i), 'wb') as outfile:
                            # outfile.write(e.stdout)
                        with open(crash_dir+'/'+infilename+'.stderr.'+str(crash_i), 'wb') as outfile:
                            outfile.write(e.stderr)

                        crash_i += 1

            # clean up
            run(['rm', tmpfile])
            print('found ' + str(crash_i) + ' bugs!')
    
                    
def dir_bug_search(mode, wrapper_exe, input_dir):
    input_dir = input_dir.rstrip('/')
    dataset_path, dataset_name = path.split(input_dir)
    crash_dir = dataset_name + '_crashes_' + mode
    data_dir = path.join(dataset_path, dataset_name + '_' + mode + '_funcs')
    
    if not path.isdir(data_dir):
        eg.eval_dir(mode, wrapper_exe, input_dir)
    
    if not path.isdir(crash_dir):
        os.mkdir(crash_dir)
    
    infiles = glob(input_dir+'/*')
    Parallel(n_jobs=10, prefer="threads")(
         delayed(bug_search)(mode, wrapper_exe,
         pd.read_csv(path.join(data_dir, path.basename(f)+'.csv')),
         crash_dir, f) for f in infiles)
        

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['grad', 'taint', 'both'])
    parser.add_argument('wrapper_exe')
    parser.add_argument('input_dir')
    args = parser.parse_args()
    
    if args.mode == 'both':
        dir_bug_search('grad', args.wrapper_exe, args.input_dir)
        dir_bug_search('taint', args.wrapper_exe, args.input_dir)
    else:
        dir_bug_search(args.mode, args.wrapper_exe, args.input_dir)
        
        
if __name__ == '__main__':
    main()
    
        
