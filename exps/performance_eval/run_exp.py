import sys, argparse, os
from glob import glob
import pandas as pd
from eval_runtime import full_eval


def full_eval_safe(program, infile):
    try:
        return full_eval(program, infile)
    except Exception as e:
        print('Error on', program, infile)
        print(e)
        return pd.DataFrame([])



def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='out_dir', help='output dir for exp')
    parser.add_argument('-i', dest='input', help='output dir for exp')
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    input_dir = args.input

    if out_dir is None:
        out_dir = 'results'

    if input_dir is None:
        input_dir = 'input'
 
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

 
    # jpeg = full_eval_safe('jpeg', glob(input_dir+'/'
    # zlib = full_eval_safe('zlib',       
    # mupdf = full_eval_safe('mupdf',     
    # libxml = full_eval_safe('libxml',   
    # readelf = full_eval_safe('readelf', 
    # objdump = full_eval_safe('objdump', 
    # strip = full_eval_safe('strip',     



    # jpeg = full_eval_safe('jpeg', './inputs/sky.jpg')
    # zlib = full_eval_safe('zlib', './inputs/zlib_5kb.gz')
    # mupdf = full_eval_safe('mupdf', './inputs/testpdf.pdf')
    # libxml = full_eval_safe('libxml', './inputs/fp40_fixed.htm')
    # readelf = full_eval_safe('readelf', './inputs/radix_sort')
    # objdump = full_eval_safe('objdump', './inputs/basic')
    # strip = full_eval_safe('strip', './inputs/radix_sort')

    # jpeg.to_csv(out_dir+'/jpeg.csv')
    # zlib.to_csv(out_dir+'/zlib.csv')
    # mupdf.to_csv(out_dir+'/mupdf.csv')
    # libxml.to_csv(out_dir+'/libxml.csv')
    # readelf.to_csv(out_dir+'/readelf.csv')
    # objdump.to_csv(out_dir+'/objdump.csv')
    # strip.to_csv(out_dir+'/strip.csv')

    # results = [zlib, jpeg, mupdf, libxml, readelf, objdump, strip]
    results = []
    programs = ['zlib', 'jpeg', 'mupdf', 'libxml', 'readelf', 'objdump', 'strip']
    
    for program in programs:
        res = full_eval_safe(program, glob(input_dir+'/'+program+'/*')[0])
        results.append(res)

    rows = []
    for result, program in zip(results, programs):
        try:
            result.index = result.type
            row = { 'program': program,
                    'base_runtime': result.at['base','runtime'],
                    # 'taint_unlabeled_runtime': result.at['dfsan_unlabeled','runtime'],
                    # 'taint_unlabeled_overhead': result.at['dfsan_unlabeled','overhead'],
                    'taint_runtime': result.at['dfsan','runtime'],
                    'taint_overhead': result.at['dfsan','overhead'],
                    # 'grad_unlabeled_runtime': result.at['grsan_unlabeled','runtime'],
                    # 'grad_unlabeled_overhead': result.at['grsan_unlabeled','overhead'],
                    'grad_runtime': result.at['grsan','runtime'],
                    'grad_overhead': result.at['grsan','overhead'],
                    'rel_overhead': (result.at['grsan','runtime'] - result.at['dfsan', 'runtime'])/result.at['dfsan', 'runtime'] * 100.0}
            rows.append(row)
        except:
            pass

    summary = pd.DataFrame(rows)
    summary.index = summary.program
    # summary['relative_overhead'] = (summary['grad_overhead'] - summary['taint_overhead'])/(summary['taint_overhead']+1)
    summary2 = summary[['base_runtime',  
                         'taint_runtime', 'taint_overhead',
                        'grad_runtime', 'grad_overhead', 'rel_overhead']]
    summary2 = summary2.round(3)

    # summary2 = summary[['base_runtime', 'taint_unlabeled_runtime', 'taint_unlabeled_overhead',
                        # 'grad_unlabeled_runtime', 'grad_unlabeled_overhead', 'taint_runtime', 'taint_overhead',
                        # 'grad_runtime', 'grad_overhead', 'relative_overhead']]
    summary2.index = summary.program
    # summary.drop('program', 1)
    summary2.to_csv(out_dir+'/summary.csv')
    print('-'*50)
    print('SUMMARY:')
    print(summary2)


if __name__ == '__main__':
    main()

