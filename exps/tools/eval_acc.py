import pandas as pd
import sys, os, argparse, pickle
from grad_utils import precision, recall, stat_summary, get_nonzero

def df_stats(df, gt):
    
    df = get_nonzero(df)
    
#     dftg = dft.groupby(['file_id', 'inst_id']).agg(tuple)

    dfg = df.groupby(['file_id', 'inst_id']).agg(tuple)
    dfg = dfg.reset_index()
    dfg['valid_bytes'] = dfg.apply(lambda row: gt[str(row.file_id)+'-'+str(row.inst_id)], axis=1)
    dfg['grad_precision'] = dfg.apply(lambda row: precision(row.deriv_byte, row.valid_bytes), axis=1)
    dfg['grad_recall'] = dfg.apply(lambda row: recall(row.deriv_byte, row.valid_bytes), axis=1)
    
#     dfg['taint_precision'] = dfg.apply(lambda row: precision(dftg.loc[(row.file_id, row.inst_id), 'deriv_byte'],
#                                                              row.valid_bytes), axis=1)
#     dfg['taint_recall'] = dfg.apply(lambda row: recall(dftg.loc[(row.file_id, row.inst_id), 'deriv_byte'],
#                                                              row.valid_bytes), axis=1)
#     dfg['taint_recall'] = dfg.apply(lambda row: recall(row.deriv_byte, row.valid_bytes), axis=1)

    
    
    
    statsdf = dfg[['grad_precision', 'grad_recall']]
    for col in statsdf.columns:
        statsdf = statsdf[statsdf[col].notnull()]
    p, r = statsdf.grad_precision.mean(), statsdf.grad_recall.mean()

    return dfg, statsdf.mean(), p, r
    



    
    
def main(argv=sys.argv[1:]):

    parser = argparse.ArgumentParser()
    parser.add_argument('grad_data')
    parser.add_argument('ground_truth_pkl')
    args = parser.parse_args(argv)

    grad_data_n = args.grad_data
    gt_pkl = args.ground_truth_pkl
    
    df = pd.read_csv(grad_data_n)
    
    with open(gt_pkl, 'rb') as f:
        gt = pickle.load(f)


    dfg, s, p, r = df_stats(df, gt)
    
    
    print(p, r)
    
    grad_data_bn = os.path.basename(grad_data_n)
    grad_data_bn, _ = os.path.splitext(grad_data_bn)
    
    dfg.to_csv(grad_data_bn + '.agg.csv')
    s.to_csv(grad_data_bn + '.stats.csv')


if __name__ == '__main__':
    main()