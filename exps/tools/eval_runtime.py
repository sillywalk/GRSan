import sys, os
import pandas as pd
from subprocess import call, run, DEVNULL, CalledProcessError, Popen
from tqdm import tqdm_notebook, tqdm
from glob import glob
from joblib import Parallel, delayed
import time, tempfile, argparse
import programs

MAX_ITER = 6000

def eval_file(program, infile, mode, label=True, opt=True):

    env = os.environ.copy()
    env['GR_MODE_PERF'] = '1'

    if opt:
        env['DFSAN_OPTIONS'] = "reuse_labels=0"


    _, ext = os.path.splitext(infile)

    tmpfile = 'input'+ext
    run(['cp', infile, tmpfile])

    cmd = programs.get_cmd(program, mode, infile, 0)
    if mode in [programs.TAINT, programs.GRAD]:
        if label:
            cmd[-2] = "$i"
        else:
            del cmd[-2]
            del cmd[-2]

    # del cmd[-2]
    # del cmd[-2]
    cmd = " ".join(cmd)

    size = os.path.getsize(infile)
    iters = min(size-1, MAX_ITER)
    print(infile, iters)

    try:
        fullcmd =  "for i in {0.."+str(iters)+"}; do "+cmd+">/dev/null; done;"
        if (iters < 1000):
            fullcmd = "for j in {0..5}; do " + fullcmd + "done;"
            iters = iters*5
            nsamples = 5
        else:
            nsamples = 2
        # fullcmd = cmd
        # fullcmd =  "for i in {0.."+str(iters)+"}; do "+cmd+"; done;"
        print(fullcmd)
        total_time = 0.0

        for i in range(nsamples):
            # prep any cache
            run_res = run(cmd, shell=True, env=env, executable='/bin/bash', capture_output=True)

            start = time.time()
            run_res = run(fullcmd, shell=True, env=env, executable='/bin/bash', capture_output=True)
            elapsed = time.time() - start
            total_time += elapsed

            if run_res.returncode:
                print('Error',str(run_res.returncode)+':', " ".join(programs.get_cmd(program, mode, infile)))
                # print('stdout:', run_res.stdout.decode('utf-8', errors='ignore'))
                print('stderr:', run_res.stderr.decode('utf-8', errors='ignore'))

    except Exception as e:
        print('Error:', " ".join(programs.get_cmd(program, mode, infile)))
        print(e)
        return 0

    # sanity check we're not recording
    # assert(not (os.path.exists('branches.csv')))
    # assert(not (os.path.exists('func_args.csv')))
    meantime = total_time / nsamples * 1000.0 # convert to ms
    per_byte_time = meantime / iters

    return per_byte_time

def process_file(mode, program, infile, label=True, opt=True):
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as run_dir:
        infile = os.path.abspath(infile)
        os.chdir(run_dir)
        meantime = eval_file(program, infile, mode, label, opt=opt)

    os.chdir(cwd)

    return meantime


def full_eval(program, infile, opt=True):
    base_rtime = process_file('base', program, infile)
    # grad_rtime_nolabel = process_file('grad', program, infile, label=False, opt=opt)
    grad_rtime = process_file('grad', program, infile, opt=opt)
    # taint_rtime_nolabel = process_file('taint', program, infile, label=False, opt=opt)
    taint_rtime = process_file('taint', program, infile, opt=opt)


    # rtimes = pd.DataFrame({'type':['base', 'dfsan_unlabeled', 'dfsan', 'grsan_unlabeled', 'grsan']})
    rtimes = pd.DataFrame({'type':['base', 'dfsan', 'grsan']})
    # rtimes['runtime'] = pd.Series([base_rtime, taint_rtime_nolabel, taint_rtime, grad_rtime_nolabel, grad_rtime], rtimes.index)
    rtimes['runtime'] = pd.Series([base_rtime, taint_rtime, grad_rtime], rtimes.index)
    rtimes = rtimes.round(3)

    base_time = rtimes.at[0, 'runtime']
    rtimes['overhead'] = (rtimes['runtime'] - base_time)/base_time * 100.0

    size = os.path.getsize(infile)
    rtimes['fsize'] = size

    print(program)
    print(rtimes)
    print('relative:', (rtimes.at[2, 'runtime'] - rtimes.at[1, 'runtime'])/rtimes.at[0, 'runtime'] * 100)
    print()

    return rtimes


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['base', 'grad', 'taint', 'full'])
    parser.add_argument('program', choices=programs.valid_programs)
    parser.add_argument('infile', help='target file or directory of files')
    parser.add_argument('-o', dest='outfile', help='specify name of result file')
    parser.add_argument('--no-opt', dest='opt', action='store_false',  help='dont use optimization')
    args = parser.parse_args(argv)

    mode = args.mode
    program = args.program
    infile = args.infile
    name = os.path.basename(infile)

    if mode == 'full':
        rtimes = full_eval(program, infile)
        if args.outfile is not None:
            rtimes.to_csv(args.outfile)
        else:
            rtimes.to_csv(name+'_overhead.csv')
        print(rtimes)

    else:
        rtime = process_file(mode, program, infile, opt=args.opt)
        print(mode, rtime)


if __name__ == '__main__':
    main()

