import sys, os
import pandas as pd
import numpy as np
from subprocess import call, run, DEVNULL, CalledProcessError
from tqdm import tqdm_notebook, tqdm, trange
from glob import glob
from joblib import Parallel, delayed
import time, tempfile, argparse
import programs

def eval_file_fast(program, infile, mode, progbar=True, n_samples=1,
        record_branches=True, record_funcs=True, record_labels=False
                  , opts=argparse.Namespace()):

    # if mode == 'grad':
        # mode = 'gradient'

    size = os.path.getsize(infile)

    branch_data = []
    func_data = []
    label_data = []
    
    _, ext = os.path.splitext(infile)

    tmpfile = 'input'+ext
    run(['cp', infile, tmpfile])

    env = os.environ.copy()

    loop_iter = range(size)
    if progbar:
        loop_iter = trange(size)
        print('eval', infile, mode+'...')

    for i in loop_iter:
        options = []
        # options = ['reuse_labels=false']
        if record_branches: options += ["branch_logfile=branches_{}.csv".format(i)]
        else: options += ["branch_logfile=''"]
        if record_funcs: options += ["func_logfile=func_args_{}.csv".format(i)]
        else: options += ["func_logfile=''"]
        if record_labels: options += ["dump_labels_at_exit=labels_{}.csv".format(i)]
        else: options += ["dump_labels_at_exit=''"]
        options += ["and_nsamples={}".format(n_samples)]
        if ('shr_samples' in opts):
            options += ["shr_nsamples={}".format(opts.shr_samples)]
        env['DFSAN_OPTIONS'] = ",".join(options) if len(options) > 1 else options
        if i == 0:
            print(env['DFSAN_OPTIONS'])

        cmd = programs.get_cmd(program, mode, infile, i)
        if i == 0:
            print(cmd)
        # run_res = run([exe, mode, str(i), tmpfile], env=env, capture_output=True)
        run_res = run(cmd, env=env, capture_output=True)
        if run_res.returncode:
            print('Error retcode: {}, stderr: {}'.format(run_res.returncode, run_res.stderr.decode('utf=8')))

        

    for i in range(size):
        # aggregate output
        if record_branches:
            try:
                df = pd.read_csv('branches_'+str(i)+'.csv', dtype={'file_id':np.uint64})
                if(df.file_id.dtype == 'uint64'):
                    df['deriv_byte'] = i
                    branch_data.append(df)
                else:
                    print('skipping byte data for invalid file_id type', i, df.file_id.dtype)
            except Exception as e:
                print('warning: branches_'+str(i)+'.csv missing')
                print(e)

        if record_labels:
            try:
                df = pd.read_csv('labels_'+str(i)+'.csv')
                df['deriv_byte'] = i
                label_data.append(df)
            except:
                print('warning: labels_'+str(i)+'.csv missing')
        
        if mode == 'grad' and record_funcs:
            try:
                df = pd.read_csv('func_args_'+str(i)+'.csv')
                df['deriv_byte'] = i
                func_data.append(df)
            except:
                print('warning: func_args_'+str(i)+'.csv missing')

    branch_df = pd.concat(branch_data) if branch_data else None
    func_df = pd.concat(func_data) if func_data else None
    label_df = pd.concat(label_data) if label_data else None


    return branch_df, func_df, label_df


def process_file(mode, program, infile, working_dir="/dev/shm/",  n_samples=1,
        record_branches=True, record_funcs=True, record_labels=False, opts=argparse.Namespace()):
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory(prefix=working_dir) as run_dir:
        infile = os.path.abspath(infile)
        os.chdir(run_dir)
        bdf, fdf, ldf = eval_file_fast(program, infile, mode,  n_samples=n_samples,
                record_branches=record_branches, record_funcs=record_funcs, record_labels=record_labels,
                                      opts=opts)
        # bdf, fdf = eval_file2(exe, infile, mode)

    os.chdir(cwd)

    return bdf, fdf, ldf


def process_dir_file(mode, program, res_dir, func_dir, lbl_dir, f, working_dir="/dev/shm/",
        record_branches=True, record_funcs=True, progbar=False, n_samples=1,
        record_labels=False, opts=argparse.Namespace()):
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory(prefix=working_dir) as run_dir:
        res_dir = os.path.abspath(res_dir)
        func_dir = os.path.abspath(func_dir)
        lbl_dir = os.path.abspath(lbl_dir)
        fpath = os.path.abspath(f)
        fname = os.path.basename(f)

        os.chdir(run_dir)
        try:
            grad_df, func_df, lbl_df = eval_file_fast(program, fpath, mode, n_samples=n_samples,
                    progbar=progbar, record_branches=record_branches, record_funcs=record_funcs,
                                                      record_labels=record_labels, opts=opts)

            if grad_df is not None:
                grad_df.to_csv(res_dir+'/'+fname+'.csv')
            if func_df is not None:
                func_df.to_csv(func_dir+'/'+fname+'.csv')
            if lbl_df is not None:
                print(lbl_dir+'/'+fname+'.csv')
                lbl_df.to_csv(lbl_dir+'/'+fname+'.csv')
        except Exception as e:
            print(e)
            
    os.chdir(cwd)
    

def eval_dir(mode, program, dirpath, working_dir="/dev/shm/",  n_samples=1,
        record_branches=True, record_funcs=True, record_labels=False, opts=argparse.Namespace()):
    start_t = time.time()
    # res_dir = os.path.basename(dirpath.rstrip('/'))+'_'+mode
    dirpath = os.path.abspath(dirpath)
    res_dir = dirpath.rstrip('/')+'_'+mode
    func_dir = res_dir + '_funcs'
    lbl_dir = res_dir + '_lbls'
    if record_branches:
        run(['mkdir', res_dir])
    if record_funcs:
        run(['mkdir', func_dir])
    if record_labels:
        run(['mkdir', lbl_dir])

    files = glob(dirpath+'/*')

    Parallel(n_jobs=16, prefer="processes")(delayed(process_dir_file)(mode, program, res_dir, func_dir, lbl_dir, f, working_dir,
        record_branches, record_funcs, record_labels=record_labels, progbar=True, n_samples=n_samples,
                                                                     opts=opts) for f in files)

    run_t = time.time() - start_t
    print(f'completed in {run_t} seconds')


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['grad', 'taint', 'both'])
    parser.add_argument('program', choices=programs.valid_programs)
    parser.add_argument('infile', help='target file or directory of files')
    parser.add_argument('--working-dir', dest='working_dir', default="/dev/shm/",
            help='base dir to use for working tmp dirs')
    parser.add_argument('--drop-branches', dest='drop_branches', action='store_true')
    parser.add_argument('--drop-funcs', dest='drop_funcs', action='store_true')
    parser.add_argument('--drop-labels', dest='keep_labels', action='store_false')
    parser.add_argument('--and-samples', dest='n_samples', type=int, default=1)
    parser.add_argument('--shr-samples', dest='shr_samples', type=int, default=1)
    args = parser.parse_args(argv)

    mode = args.mode
    program = args.program
    infile = args.infile
    name = os.path.basename(infile)
    working_dir = args.working_dir
    n_samples = args.n_samples
    print('n_samples', n_samples)

    record_branches = not args.drop_branches
    record_funcs = not args.drop_funcs
    record_labels = args.keep_labels

    if os.path.isdir(infile):
        if mode == "both":
            eval_dir('grad', program, infile, working_dir=working_dir, record_branches=record_branches,  n_samples=n_samples,
                    record_funcs=record_funcs, record_labels=record_labels, opts=args)
            eval_dir('taint', program, infile, working_dir=working_dir, record_branches=record_branches,  n_samples=n_samples,
                    record_funcs=record_funcs, record_labels=record_labels, opts=args)
        else:
            eval_dir(mode, program, infile, working_dir=working_dir, record_branches=record_branches,  n_samples=n_samples,
                    record_funcs=record_funcs, record_labels=record_labels, opts=args)
    else:
        if mode == 'both':
            bdf, fdf, ldf = process_file('grad', program, infile, working_dir=working_dir, record_branches=record_branches,  n_samples=n_samples,
                    record_funcs=record_funcs, record_labels=record_labels)
            if bdf is not None:
                bdf.to_csv(name+'_grad.csv')
            if fdf is not None:
                fdf.to_csv(name+'_func_grad.csv')
            if ldf is not None:
                ldf.to_csv(name+'_labels.csv')
            bdf, fdf, ldf = process_file('taint', program, infile, working_dir=working_dir, record_branches=record_branches,  n_samples=n_samples,
                    record_funcs=record_funcs, record_labels=record_labels)
            if bdf is not None:
                bdf.to_csv(name+'_taint.csv')
            if fdf is not None:
                fdf.to_csv(name+'_func_taint.csv')
            if ldf is not None:
                ldf.to_csv(name+'_labels.csv')
        else:
            bdf, fdf, ldf = process_file(mode, program, infile, working_dir=working_dir, record_branches=record_branches,  n_samples=n_samples,
                    record_funcs=record_funcs, record_labels=record_labels)
            if bdf is not None:
                bdf.to_csv(name+'_' + mode + '.csv')
            if fdf is not None:
                fdf.to_csv(name+'_func_' + mode + '.csv')
            if ldf is not None:
                ldf.to_csv(name+'_labels.csv')


if __name__ == '__main__':
    main()

