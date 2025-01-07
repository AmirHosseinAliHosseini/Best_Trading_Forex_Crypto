import pandas as pd
import numpy as np
import sys
import os

sys.path.append('./params')
import gereralParameters as gparam
import strategyParameters as sparam
import utils as ut

def gap(data, gap):
    newdata = data.shift(gap)

    for i in np.arange(gap - 1, -1, -1):
        nextsma = data.shift(i)
        newdata = np.where((newdata == 1) + (nextsma == 1), 1 , newdata)
        newdata = np.where((newdata == -1) + (nextsma == -1), -1 , newdata)

    return newdata

def applyGap(folder, pair, strategy, candle):
    data = pd.read_pickle(ut.getMixSingleStrategyFileName(folder, pair, strategy[0], candle))
    close = data['Close']
    data = data.drop('Close', axis=1)
    
    for iGap in sparam.strategyMixedGap:
        if os.path.exists(ut.getApplyGapStrategyFileName(folder, pair, strategy[0], candle, iGap)) == False:
            newData = pd.DataFrame(close)
            
            for icol in data.columns:
                newcol = gap(data[icol], iGap)
                newData.insert(len(newData.columns), icol, newcol)
            
            newData = newData.drop('Close', axis=1)
            newData.to_pickle(ut.getApplyGapStrategyFileName(folder, pair, strategy[0], candle, iGap))

def run():
    print('\n\nApply a gap to the strategy signal:')
    for folder in gparam.folders:
        for pair in gparam.pairs[folder]:
            for gra in gparam.Candle:
                for str in sparam.categoryStrategy:
                    print(folder, pair, gra[0], str[0])
                    applyGap(folder, pair, str, gra[0])
    print('\n\nFinish the gap on the strategy signal.')
                    
if __name__ == "__main__":
    run()