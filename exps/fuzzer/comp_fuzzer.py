from glob import glob
from subprocess import run
import generate_fuzzer_info as fg
import eval_grad as eg
import os, sys
import pandas as pd
pd.set_option('display.max_columns', None)
from run_fuzzer import fuzz

def compare_fuzz(fuzzer, exe, infile, grad_file, taint_file, k_bytes):

    print("Gradient mode")
    if os.path.isdir(grad_file) and os.path.isdir(infile):
        fg.label_dir('grad', infile, grad_file, k_bytes, taint_file)
    else:
        print("Assuming both grad_file and infile are files, not directories")
        fg.label_file('grad', infile, grad_file, k_bytes)


    #import pdb
    #pdb.set_trace()

    grad_cov = fuzz('grad', fuzzer, exe, infile, 0)
    graddirpath = 'seeds_grad'
    run(['rm', '-rf', 'seeds_grad', 'taint_info_grad'])
    run(['mv', 'seeds', 'seeds_grad'])
    run(['mv', 'taint_info', 'taint_info_grad'])
    run(['rm', '-f', 'taint_info_p'])

    tt_num = grad_cov[1][0]

    print("Taint mode")
    if os.path.isdir(infile) and os.path.isdir(taint_file):
        fg.label_dir('taint', infile, taint_file, k_bytes, grad_file)
    else:
        print("Assuming both grad_file and infile are files, not directories")
        fg.label_file('taint', infile, taint_file, k_bytes)

    #import pdb
    #pdb.set_trace()
    taint_cov = fuzz('taint', fuzzer, exe, infile, tt_num)
    if not os.listdir('./crashes'):
        for f in os.listdir('./crashes/'):
            shutils.move('./crashes/'+f, './crashes/'+exe+'_'+f)

    run(['rm', '-rf', 'seeds_taint', 'taint_info_taint'])
    run(['mv', 'seeds', 'seeds_taint'])
    run(['mv', 'taint_info', 'taint_info_taint'])
    run(['rm', '-f', 'taint_info_p'])

    try:
        taint_execs_per_edge = (taint_cov[1][0] - taint_cov[0][0]) / (taint_cov[1][1] - taint_cov[0][1])
        grad_execs_per_edge = (grad_cov[1][0] - grad_cov[0][0]) / (grad_cov[1][1] - grad_cov[0][1])
    except Exception as e:
        print(taint_cov)
        print(grad_cov)
        print(e)
        taint_execs_per_edge = -1
        grad_execs_per_edge = -1
    res = pd.DataFrame([{'file':os.path.basename(infile),
                        'taint_cov_orig': taint_cov[0][1],
                        'taint_exec_orig': taint_cov[0][0],
                        'taint_cov_final': taint_cov[1][1],
                        'taint_exec_final': taint_cov[1][0],
                        'grad_cov_orig':grad_cov[0][1],
                        'grad_exec_orig':grad_cov[0][0],
                        'grad_cov_final':grad_cov[1][1],
                        'grad_exec_final':grad_cov[1][0],
                        'taint_execs_per_edge': taint_execs_per_edge,
                        'grad_execs_per_edge': grad_execs_per_edge
                       }])
    return res, graddirpath, taintdirpath

def grad_fuzz(fuzzer, exe, infile, grad_file, taint_file, k_bytes, tt_num):

    print("Gradient mode")
    if os.path.isdir(grad_file) and os.path.isdir(infile):
        fg.label_dir_single_mode('grad', infile, grad_file, k_bytes)
    else:
        print("Assuming both grad_file and infile are files, not directories")
        fg.label_file('grad', infile, grad_file, k_bytes)
    grad_cov = fuzz('grad', fuzzer, exe, infile, tt_num)
    if not os.listdir('./crashes'):
        for f in os.listdir('./crashes/'):
            shutils.move('./crashes/'+f, './crashes/'+exe+'_'+f)

    graddirpath = 'seeds_grad'
    run(['mv', 'seeds', 'seeds_grad'])
    run(['mv', 'taint_info', 'taint_info_grad'])
    run(['rm', '-f', 'taint_info_p'])

    tt_num = grad_cov[1][0]
    return graddirpath, tt_num

def taint_fuzz(fuzzer, exe, infile, grad_file, taint_file, k_bytes, tt_num):


    print("Taint mode")
    if os.path.isdir(infile) and os.path.isdir(taint_file):
        fg.label_dir_single_mode('taint', infile, taint_file, k_bytes)
    else:
        print("Assuming both grad_file and infile are files, not directories")
        fg.label_file('taint', infile, taint_file, k_bytes)
    taint_cov = fuzz('taint', fuzzer, exe, infile, tt_num)
    if not os.listdir('./crashes'):
        for f in os.listdir('./crashes/'):
            shutils.move('./crashes/'+f, './crashes/'+exe+'_'+f)

    tt_num = taint_cov[1][0]
    graddirpath = 'seeds_taint'
    run(['mv', 'seeds', 'seeds_taint'])
    run(['mv', 'taint_info', 'taint_info_taint'])
    run(['rm', '-f', 'taint_info_p'])

    return graddirpath, tt_num
if __name__=='__main__':
    if len(sys.argv) not in [6, 7, 8]:
        print('usage: python '+sys.argv[0]+' <fuzzer> <test_exe> <input_files> <grad_files> <taint_files> [k_bytes]')
        sys.exit(1)

    fuzzer = sys.argv[1]
    test_exe = sys.argv[2]
    infile = sys.argv[3]
    grad_file = sys.argv[4]
    taint_file = sys.argv[5]
    k_bytes = None
    script = sys.argv[7]

    graddirpath = infile
    taintdirpath = infile
    grad_tt_num = 3586
    taint_tt_num = 3739

    graddirpath = 'seeds_grad'
    taintdirpath = 'seeds_taint'
    graddirpath, grad_tt_num = grad_fuzz(fuzzer, test_exe, graddirpath, graddirpath + '_grad', graddirpath + '_taint', k_bytes, grad_tt_num)
    taintdirpath, taint_tt_num = taint_fuzz(fuzzer, test_exe, taintdirpath, taintdirpath + '_grad', taintdirpath + '_taint', k_bytes, taint_tt_num)
    eg.eval_dir("taint", script, taintdirpath)
    eg.eval_dir("grad", script, graddirpath)
    graddirpath, grad_tt_num = grad_fuzz(fuzzer, test_exe, graddirpath, graddirpath + '_grad', graddirpath + '_taint', k_bytes, grad_tt_num)
    taintdirpath, taint_tt_num = taint_fuzz(fuzzer, test_exe, taintdirpath, taintdirpath + '_grad', taintdirpath + '_taint', k_bytes, taint_tt_num)
    eg.eval_dir("taint", script, taintdirpath)
    eg.eval_dir("grad", script, graddirpath)

    '''
    for i in range(3):

        #graddirpath, grad_tt_num = grad_fuzz(fuzzer, test_exe, graddirpath, grad_file, taint_file, k_bytes, grad_tt_num)
        if(i==0):
            graddirpath, grad_tt_num = grad_fuzz(fuzzer, test_exe, graddirpath, grad_file, taint_file, k_bytes, grad_tt_num)
            taintdirpath, taint_tt_num = taint_fuzz(fuzzer, test_exe, taintdirpath, grad_file, taint_file, k_bytes, taint_tt_num)
            #import ipdb
            #ipdb.set_trace()
        else:
            graddirpath, grad_tt_num = grad_fuzz(fuzzer, test_exe, graddirpath, graddirpath + '_grad', graddirpath + '_taint', k_bytes, grad_tt_num)
            taintdirpath, taint_tt_num = taint_fuzz(fuzzer, test_exe, taintdirpath, taintdirpath + '_grad', taintdirpath + '_taint', k_bytes, taint_tt_num)

    #df, graddirpath, taintdirpath = compare_fuzz(fuzzer, test_exe, infile, grad_file, taint_file, k_bytes)
        #if i != 0:
        eg.eval_dir("taint", script, taintdirpath)
        eg.eval_dir("grad", script, graddirpath)
    '''
    #eval_grad grad $(pwd)/../exps/programs/zlib/bin/zlib.sh grad_dir/ #
    #eval_grad taint $(pwd)/../exps/programs/zlib/bin/zlib.sh taint_dir/ #
    #eg.eval_dir("grad", script, 'seeds')

    #0. copy crash inputs to treasure boxes.
    #1. obtain total number of mutations for current round
    #2. eval_grad on both corpus
    #3. pass the number of mutaions to fuzzing module, start next round fuzzing
    #print(df.to_csv())
