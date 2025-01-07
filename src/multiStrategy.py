from multiprocessing import Pool
from functools import partial
import pandas as pd
import numpy as np
import vectorbt as vbt
import datetime
import sys
import os

sys.path.append('./params')
import gereralParameters as gparam
import strategyParameters as sparam
import utils as ut

allTrade = 41 * 81 * 41 * 17

def calMultiStrategy(sma, rsi, macd, adx, close, icolSMA, icolRSI, icolMACD, fees): 
    
    value = (sma > 0) * (rsi > 0) * (macd > 0) * (adx > 0)
    entries = value == True

    if icolSMA == 'No-SMA':
        sma = sma * -1
    if icolRSI == 'No-RSI':
        rsi = rsi * -1
    if icolMACD == 'No-MACD':
        macd = macd * -1

    value1 = ((sma < 0) * (rsi < 0) * (macd < 0)) * (adx > 0)
    exits = value1 == True

    pf = vbt.Portfolio.from_signals(close, entries, exits, fixed_fees = fees)
    return pf.total_return(), pf.stats().to_string()

def runThread(folder, pair, cndl, fees, startTime, ithread):
    closeData = pd.read_pickle(ut.getHisDataFilename(folder, pair, cndl))['Close']
    rets = pd.DataFrame(columns=['SMA', 'RSI', 'MACD', 'ADX', 'FixGap', 'return', 'status'])

    counter = 0
    
    for iMixGap in sparam.strategyMixedGap:
        SMA_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, pair, 'SMA', cndl, iMixGap))
        RSI_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, pair, 'RSI', cndl, iMixGap))
        MACD_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, pair, 'MACD', cndl, iMixGap))
        ADX_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, pair, 'ADX', cndl, iMixGap))
        
        icolADX = ADX_Data.columns[ithread]
        ADX_Data = ADX_Data[icolADX]

        for icolSMA in SMA_Data.columns:
            for icolRSI in RSI_Data.columns:
                for icolMACD in MACD_Data.columns:
                    ret, status = calMultiStrategy(SMA_Data[icolSMA], RSI_Data[icolRSI], MACD_Data[icolMACD], ADX_Data, 
                                                closeData, icolSMA, icolRSI, icolMACD, fees)
                    rets.loc[len(rets)] = [icolSMA, icolRSI, icolMACD, icolADX, iMixGap, ret, status]
                    
            if ithread == 0:
                counter += 81 * 41 * 17
                print(f'\tprocessed: {round((counter / allTrade) * 100, 2)} % \tTime : {datetime.datetime.now() - startTime}', flush = True)
    
    return rets

def runMultiStrategy(folder, pair, cndl, fees):
    if os.path.exists(ut.getMUltiStrategyFileName(folder, pair, cndl)) == True:
        return

    rets = pd.DataFrame(columns=['SMA', 'RSI', 'MACD', 'ADX', 'FixGap', 'return', 'status'])

    t1 = datetime.datetime.now()

    with Pool() as p:
        func = partial(runThread, folder, pair, cndl, fees, t1)
        rets = p.map(func, np.arange(123))
        
    final = pd.DataFrame(columns=['SMA', 'RSI', 'MACD', 'ADX', 'FixGap', 'return', 'status'])
    for iret in np.arange(len(rets)):
        final = pd.concat([final, rets[iret]])
    final = final.sort_values(by='return', ascending=False)
    final = final[:500]
    final.to_excel(ut.getMUltiStrategyFileName(folder, pair, cndl))

    print(pair, cndl, f'Time : {datetime.datetime.now() - t1}')

def runThread_(startTime, ithread):
    idx = ithread

    iPair = idx % 8
    iCont = iPair
    idx //= 8
    if iPair < 3:
        folder = gparam.folders[0]
    else:
        folder = gparam.folders[1]
        iPair -= 3
    iPair = gparam.pairs[folder][iPair]

    fees = sparam.fees[folder]
    
    iCndl = idx % 5
    iCont = iCont * 5 + iCndl
    iCndl = gparam.Candle[iCndl][0]
    idx //= 5

    idx *= 2
    iMixGap = idx

    print(f'starting {iPair}(Candle({iCndl}), Gap({iMixGap}, {iMixGap + 1})):')

    closeData = pd.read_pickle(ut.getHisDataFilename(folder, iPair, iCndl))['Close']
    rets = pd.DataFrame(columns=['SMA', 'RSI', 'MACD', 'ADX', 'FixGap', 'return', 'status'])
    
    while iMixGap <= idx + 1:
        counter = 0
        SMA_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, iPair, 'SMA', iCndl, iMixGap))
        RSI_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, iPair, 'RSI', iCndl, iMixGap))
        MACD_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, iPair, 'MACD', iCndl, iMixGap))
        ADX_Data = pd.read_pickle(ut.getApplyGapStrategyFileName(folder, iPair, 'ADX', iCndl, iMixGap))
        
        for icolSMA in SMA_Data.columns:
            for icolRSI in RSI_Data.columns:
                for icolMACD in MACD_Data.columns:
                    for icolADX in ADX_Data.columns:
                        ret, status = calMultiStrategy(SMA_Data[icolSMA], RSI_Data[icolRSI], MACD_Data[icolMACD], ADX_Data[icolADX], 
                                                    closeData, icolSMA, icolRSI, icolMACD, fees)
                        rets.loc[len(rets)] = [icolSMA, icolRSI, icolMACD, icolADX, iMixGap, ret, status]
                        
            counter += 81 * 41 * 17
            print(f'\t{iPair}(Candle({iCndl}), Gap({iMixGap})) processed: {round((counter / allTrade) * 100, 2)} % \tTime : {datetime.datetime.now() - startTime}', flush = True)
        iMixGap += 1
    return rets

def run():
    print('\n\nStart combining strategies:')
    t1 = datetime.datetime.now()

    with Pool() as p:
        func = partial(runThread_, t1)
        rets = p.map(func, np.arange(120))



    
    # for folder in gparam.folders:
    #     for pair in gparam.pairs[folder]:
    #         for cndl in gparam.Candle:
    #             print(folder, pair, cndl)
    #             runMultiStrategy(folder, pair, cndl[0], sparam.fees[folder])
    print('\n\nFinished combination of strategies.')
            
if __name__ == "__main__":
    run()