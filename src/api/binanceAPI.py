import pandas as pd
from datetime import datetime
from dateutil import relativedelta
import sys
import os

sys.path.append('../params')
import utils as ut

import apiParameters as api

class BinanceAPI():
    def __init__(self):
        self.Candle = {
                'H4'  : '4h',
                'H1'  : '1h',
                'M30' : '30m',
                'M15' : '15m',
                'M5'  : '5m',
                'M1'  : '1m' 
                }

    def createFile(self, pair, candle , startDate, endDate):
        if os.path.exists(ut.getHisDataFilename('crypto', pair, candle)):
            return
               
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        deltaDate = relativedelta.relativedelta(datetime.strptime(endDate, "%Y-%m-%d"), startDate)
        months = deltaDate.years * 12 + deltaDate.months

        finalDf = pd.DataFrame({'OpenTime':[], 'Open':[], 'High':[], 'Low':[], 'Close':[], 'Volume':[], 'CloseTime':[],
                            'QuoteVolume':[], 'NumTrades':[], 'TakerBuyBaseVol':[], 'TakerBuyQuoteVol':[], 'Unused':[]})

        cndl = self.Candle[candle]
        nextDate = startDate
        for m in range(months):        
            queryString = f'{api.BINANCE_URL}/{pair}/{cndl}/{pair}-{cndl}-{nextDate.strftime("%Y-%m")}.zip'
            data = pd.read_csv(queryString,
                            names=['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 
                                'QuoteVolume', 'NumTrades', 'TakerBuyBaseVol', 'TakerBuyQuoteVol', 'Unused'])
            
            finalDf = finalDf.append(data, ignore_index=True)
            nextDate = nextDate + relativedelta.relativedelta(months=1, day=1)

        finalDf['OpenTime'] = pd.to_datetime(finalDf['OpenTime'], unit = 'ms')
        finalDf.set_index('OpenTime', inplace = True)
        finalDf = finalDf[['Open', 'High', 'Low', 'Close', 'Volume']]
        finalDf.to_pickle(ut.getHisDataFilename('crypto', pair, candle))
        return