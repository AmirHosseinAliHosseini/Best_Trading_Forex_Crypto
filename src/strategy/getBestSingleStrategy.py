import vectorbt as vbt
import pandas as pd
import numpy as np
import talib as tb
import sys

sys.path.append('./params')
import strategyParameters as sparam
import utils as ut

import indicatorFactory as ind

def getBestIndexs(folder, strategyName, pairs, candle, data, entries, exits, takeProfit, fees):
    maxret = pd.DataFrame(columns=['index', 'returns'])
    pairData = data

    for tp in takeProfit:
        for sl in takeProfit:
            pf = vbt.Portfolio.from_signals(data, entries, exits, sl_stop = sl, tp_stop = tp, fixed_fees = fees)
            returns = pf.total_return()
            sorted = returns.sort_values(ascending=False)
            sorted = sorted[:sparam.numberOfBestChosen]

            records = pf.orders.records_readable
            records = records.rename(columns={'Timestamp' : 'OpenTime'})

            for idxmax in sorted.index:
                record = records[records.Column == idxmax].set_index('OpenTime')
                
                pairData = pd.concat([pairData, record['Side']], axis=1).fillna(0)
                pairData['Side'] = (np.where(pairData['Side'] == 'Sell', -1, np.where(pairData['Side'] == 'Buy', 1, pairData['Side']))).astype(int)

                nameCol = '-'.join(map(str, idxmax))
                nameCol = f'{strategyName}-{nameCol}-{round(sl, sparam.roundNumber[folder] - 1)}-{round(tp, sparam.roundNumber[folder] - 1)}-{round(returns[idxmax], sparam.roundNumber[folder])}'
                
                pairData = pairData.rename(columns={'Side': nameCol})
                
                maxret.loc[len(maxret)] = [nameCol, round(returns[idxmax], sparam.roundNumber[folder])]
                    
    maxret = maxret.sort_values(by=['returns'], ascending=False)
    maxret = maxret[:sparam.numberOfBestChosen]
    
    finalData = pairData['Close']
    for imax in np.arange(len(maxret)):
        finalData = pd.concat([finalData, pairData[maxret.iloc[imax]['index']]], axis=1)
    
    finalData.to_pickle(ut.getSingleStrategyFileName(folder, pairs, strategyName, candle))

#..........................SMA..........................

def SMA_1(folder, pairs, candle, bound, data, maWindow_1 = sparam.maWindow_1, maWindow_2 = sparam.maWindow_2, takeProfit = None, fees = None):
    data = data['Close']

    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('SMA1 backtest: ', (len(maWindow_1) * len(maWindow_2) * len(takeProfit) * len(takeProfit)))

    res = ind.ind_SMA_1.run(data, maWindow_1, maWindow_2, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'SMA1', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)
    return

def SMA_2(folder, pairs, candle, bound, data, maWindow_1 = sparam.maWindow_1, maWindow_2 = sparam.maWindow_2, maWindow_3 = sparam.maWindow_3, takeProfit = None, fees = None):
    data = data['Close']
    
    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]
    
    print('SMA2 backtest: ', (len(maWindow_1) * len(maWindow_2) * len(maWindow_3) * len(takeProfit) * len(takeProfit)))

    res = ind.ind_SMA_2.run(data, maWindow_1, maWindow_1, maWindow_1, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'SMA2', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)
    
    return

#..........................RSI..........................

def RSI_1(folder, pairs, candle, bound, data, rsiWindow = sparam.rsiWindow, lowerBound = sparam.lowerBound, upperBound = sparam.upperBound, takeProfit = None, fees = None):
    data = data['Close']
    
    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('RSI1 backtest: ', (len(rsiWindow) * len(lowerBound) * len(upperBound) * len(takeProfit) * len(takeProfit)))
    
    res = ind.ind_RSI_1.run(data, rsiWindow, lowerBound, upperBound, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'RSI1', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)
        
    return

def RSI_2(folder, pairs, candle, bound, data, rsiWindow = sparam.rsiWindow, lowerBound = sparam.lowerBound, upperBound = sparam.upperBound, takeProfit = None, fees = None):
    data = data['Close']
    
    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('RSI2 backtest: ', (len(rsiWindow) * len(lowerBound) * len(upperBound) * len(takeProfit) * len(takeProfit)))
    
    res = ind.ind_RSI_2.run(data, sparam.rsiWindow, sparam.lowerBound, sparam.upperBound, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'RSI2', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)

    return

#.........................RSI_MA........................

def RSI_MA_1(folder, pairs, candle, bound, data, rsiWindow = sparam.rsiWindow, maWindow = sparam.maWindow, lowerBound = sparam.lowerBound, upperBound = sparam.upperBound, takeProfit = None, fees = None):
    data = data['Close']

    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('RSI_MA1 backtest: ', (len(rsiWindow) * len(maWindow) * len(lowerBound) * len(upperBound) * len(takeProfit) * len(takeProfit)))
    
    res = ind.ind_RSI_MA_1.run(data, rsiWindow, maWindow, lowerBound, upperBound, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'RSI_MA1', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)

    return

def RSI_MA_2(folder, pairs, candle, bound, data, rsiWindow = sparam.rsiWindow, maWindow = sparam.maWindow, lowerBound = sparam.lowerBound, upperBound = sparam.upperBound, takeProfit = None, fees = None):
    data = data['Close']
    
    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('RSI_MA2 backtest: ', (len(rsiWindow) * len(maWindow) * len(lowerBound) * len(upperBound) * len(takeProfit) * len(takeProfit)))
    
    res = ind.ind_RSI_MA_2.run(data, sparam.rsiWindow, sparam.maWindow, sparam.lowerBound, sparam.upperBound, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'RSI_MA2', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)

    return

#..........................MACD.........................

def MACD_1(folder, pairs, candle, bound, data, fastWindow = sparam.fastWindow, slowWindow = sparam.slowWindow, signalWindow = sparam.signalWindow, histDiff = sparam.histDiff, takeProfit = None, fees = None):
    data = data['Close']
    
    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('MACD1 backtest: ', (len(fastWindow) * len(slowWindow) * len(signalWindow) * len(histDiff) * len(takeProfit) * len(takeProfit)))
    
    res = ind.ind_MACD_1.run(data, fastWindow, slowWindow, signalWindow, histDiff, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'MACD1', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)

    return

def MACD_2(folder, pairs, candle, bound, data, fastWindow = sparam.fastWindow, slowWindow = sparam.slowWindow, signalWindow = sparam.signalWindow, histDiff = sparam.histDiff, takeProfit = None, fees = None):
    data = data['Close']
    
    if takeProfit is None:
        takeProfit = sparam.takeProfit[folder][candle]

    if fees is None:
        fees = sparam.fees[folder]

    print('MACD2 backtest: ', (len(fastWindow) * len(slowWindow) * len(signalWindow) * len(histDiff) * len(takeProfit) * len(takeProfit)))
    
    res = ind.ind_MACD_2.run(data, fastWindow, slowWindow, signalWindow, histDiff, param_product = True)

    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        ret = res.value[start: end]
        entries = ret == 1
        exits = ret == -1

        getBestIndexs(folder, 'MACD2', pairs[i], candle, data[start:end], entries, exits, takeProfit, fees)

    return

#..........................ADX..........................

def ADX(folder, pairs, candle, bound, data, timePeriod = sparam.timePeriod, adxBound = sparam.adxBound):

    print('ADX backtest: ', (len(timePeriod) * len(adxBound)))
    
    for i in np.arange(len(pairs)):
        start = bound[i]
        end = bound[i + 1]
        pairData = data.iloc[start:end]
        adx = pairData

        adx = pairData['Close']
        for tp in timePeriod:
            for adx_b in adxBound:
                adx_ = pd.DataFrame((tb.ADX(pairData['High'], pairData['Low'], pairData['Close'], timeperiod = tp) > adx_b).astype(int), columns=[f'ADX-{tp}-{adx_b}'])
                adx = pd.concat([adx, adx_], axis=1)
        adx['No-ADX'] = 1
    
        adx.to_pickle(ut.getSingleStrategyFileName(folder, pairs[i], 'ADX', candle))

    return
