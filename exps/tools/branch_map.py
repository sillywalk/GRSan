import sys, re

import pandas as pd
import argparse


def build_branch_map(log_file):
    with open(log_file, 'r') as f:
        branch_map = []
        for line in f:
            if (line.startswith('branch: id')):
                line = line.strip()
                line = re.split(" |:", line)
                branch_id = line[3]
                file_id = line[4]
                file_name = line[5]
                line_number = line[6]
                try:
                    branch_map.append(
                            {
                                'branch_id':branch_id,
                                'file_id':file_id,
                                'file_name':file_name,
                                'line_number':int(line_number)
                            })
                except:
                    print('branch map error: could not parse', line)
    return pd.DataFrame(branch_map)

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file')
    args = parser.parse_args(argv)

    branch_map_df = build_branch_map(args.log_file)
    branch_map_df.to_csv('branch_map.csv')


if __name__ == '__main__':
    main()


