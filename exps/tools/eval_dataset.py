import sys, argparse, os, shutil
from glob import glob
from subprocess import call, run, DEVNULL, CalledProcessError
from joblib import Parallel, delayed

import eval_gradient as eg

def eval_dataset_dir(mode, dirpath):
    # get wrapper exe
    program = os.path.basename(dirpath.rstrip('/'))
    # wrapper_exe = dirname + '.sh'
    # if not shutil.which(wrapper_exe):
        # print(wrapper_exe+' not found!')
        # return

    # call eval dir
    eg.eval_dir(mode, program, dirpath, record_funcs=False)

def main(argv = sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['grad', 'taint', 'both'])
    parser.add_argument('dataset_dir', help='dataset directory')
    args = parser.parse_args(argv)

    mode = args.mode
    dataset_dir = args.dataset_dir

    dirs = [os.path.abspath(os.path.join(dataset_dir, d)) 
            for d in os.listdir(dataset_dir)]


    # for d in dirs:
        # eval_dataset_dir(mode, d)
    if mode == 'both':
        Parallel(n_jobs=6, prefer="processes")(delayed(eval_dataset_dir)('grad', d) for d in dirs)
        Parallel(n_jobs=6, prefer="processes")(delayed(eval_dataset_dir)('taint', d) for d in dirs)
    else:
        Parallel(n_jobs=6, prefer="processes")(delayed(eval_dataset_dir)(mode, d) for d in dirs)

if __name__ == '__main__':
    main()

