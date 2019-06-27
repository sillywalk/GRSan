import glob
from subprocess import run
import os, sys
import pandas as pd
INPUT_DIR = "UNUSED/"
OUT_DIR = "seeds"

def fuzz(mode, fuzzer, exe, infile, total_mutations):
    if not os.path.exists("./taint_info_p"):
        print("Use generate_taint_info.py to generate taint_info_p")
        sys.exit(1)
    # make infile dir
    run(['rm', '-rf', INPUT_DIR])
    run(['mkdir', INPUT_DIR])

    # make seed dir
    run(['rm', '-rf', OUT_DIR])
    run(['mkdir', OUT_DIR])
    if os.path.isdir(infile):
        fsize = -1
        for ifile in glob.glob(infile + '/*'):
            fname = os.path.basename(ifile)
            run(['cp', ifile, OUT_DIR+"/" + fname])
            fsize = max(fsize, os.path.getsize(ifile))
    else:
        fname = os.path.basename(infile)
        run(['cp', infile, OUT_DIR+"/" + fname])

        fsize = os.path.getsize(infile)

    run(['rm', '-rf', 'seeds_'+mode])
    # run fuzzer and parse results
    flags = os.environ['GRADTEST_FLAGS'] if 'GRADTEST_FLAGS' in os.environ and os.environ['GRADTEST_FLAGS'] else ''
    if flags:
        lst = [fuzzer, '-i', INPUT_DIR, '-o', OUT_DIR, '-l', str(fsize),'-n', str(total_mutations), exe, flags, '@@']
    else:
        lst = [fuzzer, '-i', INPUT_DIR, '-o', OUT_DIR, '-l', str(fsize),'-n', str(total_mutations), exe, '@@']
    print("Executing ", str(lst))
    res = run(lst, capture_output=True)
    res_l = res.stdout.split()
    ret_str = res.stdout.decode('utf-8').split('\n')[:-1]
    ret_strr = [line for line in ret_str if line.find('coverage') >= 0 ]
    print("####################################################")
    for ele in ret_strr:
        print('##'+ele+'##')
    print("####################################################")
    coverage = [(int(ret_strr[0].split(' ')[2]), int(ret_strr[0].split(' ')[-1].strip('.'))), (int(ret_strr[-1].split(' ')[2]), int(ret_strr[-1].split(' ')[-1].strip('.')))]
    #coverage = [(int(res_l[i-2].decode('utf-8').strip('.')), int(res_l[i+1].decode('utf-8').strip('.')) ) for i, x in enumerate(res_l) if x == b'coverage']


    if len(coverage) != 2:
        print(res)
        raise Exception("Error during fuzzing, output: "+res.stdout.decode('utf-8')+' '+res.stderr.decode('utf-8'))
    return coverage

if __name__=='__main__':
    if len(sys.argv) != 5:
        print('usage: python '+sys.argv[0]+' <mode> <fuzzer> <test_exe> <input_files>')
        sys.exit(1)

    mode = sys.argv[1]
    fuzzer = sys.argv[2]
    test_exe = sys.argv[3]
    infile = sys.argv[4]
    print(fuzz(mode, fuzzer, test_exe, infile))
