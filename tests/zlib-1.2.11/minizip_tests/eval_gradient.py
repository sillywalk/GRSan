import sys, os
import pandas as pd
from subprocess import call, run

def eval_grad(exe, infile):

    size = os.path.getsize(infile)

    branch_data = None

    for i in range(size):
        print(i)
        run(['rm', 'input.txt'], check=False)
        run(['cp', infile, 'input.txt.gz'])
        run([exe, '-d', '-m', str(i), 'input.txt.gz'])

        # aggregate output
        df = pd.read_csv('branches.csv')
        df['deriv_byte'] = i

        if branch_data is None:
            branch_data = df
        else:
            branch_data = pd.concat([branch_data, df])

    branch_data.to_csv(infile+'.branch_gradient.csv')

if __name__ == '__main__':
    exe = sys.argv[1]
    infile = sys.argv[2]

    eval_grad(exe, infile)



