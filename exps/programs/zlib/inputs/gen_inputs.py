import sys, os
from subprocess import run


exe = sys.argv[1]
infile = sys.argv[2]

for f in ['', '-f']:
    for r in ['', '-r']:
        for h in ['', '-h']:
            for comp in ['-1', '-5', '-9']:
                print(f, r, h, comp)
                run(['cp', infile, 'tmp'])
                run(filter(None, [exe, h, f, r, comp, infile]))
                if os.path.isfile(infile+'.gz'):
                    run(['mv', infile+'.gz', infile+f+r+h+comp+'.gz'])
                else:
                    print(f, r, h, comp, ' FAILED')
                run(['cp', 'tmp', infile])


