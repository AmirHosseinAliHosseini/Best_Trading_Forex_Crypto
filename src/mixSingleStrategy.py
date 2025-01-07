import pandas as pd
import numpy as np
import sys
import os

sys.path.append('./params')
import gereralParameters as gparam
import strategyParameters as sparam
import utils as ut

def mixStrategy(folder, pair, strategy, candle):
    if os.path.exists(ut.getMixSingleStrategyFileName(folder, pair, strategy[0], candle)) == True:
        return
    
    data = pd.read_pickle(ut.getSingleStrategyFileName(folder, pair, f'{strategy[1][0]}', candle))

    if (len(strategy) < 2):
        return

    for i in np.arange(1, len(strategy[1])):
        data2 = pd.read_pickle(ut.getSingleStrategyFileName(folder, pair, f'{strategy[1][i]}', candle))
        data = pd.concat([data, data2.drop('Close', axis=1)], axis=1)

    data[f'No-{strategy[0]}'] = 1
    data.to_pickle(ut.getMixSingleStrategyFileName(folder, pair, strategy[0], candle))

def run():
    print('\n\nStart mixing group strategies:')
    for folder in gparam.folders:
        for pair in gparam.pairs[folder]:
            for cndl in gparam.Candle:
                for str in sparam.categoryStrategy:
                    print(folder, pair, cndl[0], str[0])
                    mixStrategy(folder, pair, str, cndl[0])
    print('\n\nThe mix of strategies were finished.')
                    
if __name__ == "__main__":
    run()