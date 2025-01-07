from multiprocessing import Pool
from functools import partial
import pandas as pd
import numpy as np
import datetime
import sys
import os

sys.path.append('./params')
import gereralParameters as gparam
import utils as ut

sys.path.append('./strategy')
import getBestSingleStrategy as bss

def runStrategycandle(folder, pairs, candle):
    print('Calculate strategies:', folder, pairs, candle[0], flush = True)
    #Load data for each candle
    candle = candle[0]
    df = list()
    bound = [0]
    for pair in pairs:
        df.append(ut.openfile(folder, pair, candle))
        bound.append(len(df[-1]))

    data = pd.concat(df)
    bound = np.array(bound).cumsum()

    #run ADX strategy
    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'ADX', candle)) == False:
        t1 = datetime.datetime.now()
        bss.ADX(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    #run SMA strategy
    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'SMA1', candle)) == False:
        t1 = datetime.datetime.now()
        bss.SMA_1(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'SMA2', candle)) == False:
        t1 = datetime.datetime.now()
        bss.SMA_2(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    #run RSI strategy
    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'RSI1', candle)) == False:
        t1 = datetime.datetime.now()
        bss.RSI_1(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'RSI2', candle)) == False:
        t1 = datetime.datetime.now()
        bss.RSI_2(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    #run RSI-MA strategy
    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'RSI_MA1', candle)) == False:
        t1 = datetime.datetime.now()
        bss.RSI_MA_1(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'RSI_MA2', candle)) == False:
        t1 = datetime.datetime.now()
        bss.RSI_MA_2(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)
    
    #run MACD strategy
    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'MACD1', candle)) == False:
        t1 = datetime.datetime.now()
        bss.MACD_1(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)

    if os.path.exists(ut.getSingleStrategyFileName(folder, pairs[-1], 'MACD2', candle)) == False:
        t1 = datetime.datetime.now()
        bss.MACD_2(folder, pairs, candle, bound, data)
        t2 = datetime.datetime.now()
        print('time: ', t2 - t1, flush = True)
 
def run():
    print('\n\nStart the calculation strategies:')
    for folder in gparam.folders:
        #Serial
        for candle in gparam.Candle:
            runStrategycandle(folder, gparam.pairs[folder], candle)
        
        #Parallel
        #with Pool() as p:
        #    func = partial(runStrategycandle, folder, gparam.pairs[folder])
        #    rets = p.map(func, gparam.Candle)
    print('\n\nThe calculated strategies were completed.')
if __name__ == "__main__":
    run()