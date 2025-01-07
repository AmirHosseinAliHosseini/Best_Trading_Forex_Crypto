import pandas as pd
import datetime as dt
from dateutil.parser import parse
import requests
import sys
import os

sys.path.append('../params')
import utils as ut

import apiParameters as api

class OandaAPI():
    def __init__(self):
        self.session = requests.Session()
        self.increments = {
                'H4'  : 240,
                'H1'  : 60,
                'M30' : 30,
                'M15' : 15,
                'M5'  : 5,
                'M1'  : 1
                }

    def fetchCandles(self, pair, candle, startDate, endDate, asDf = False):
        url = f"{api.OANDA_URL}/instruments/{pair}/candles"

        params = dict(
            granularity = candle,
            price = "MBA"
        )

        params['to'] = int(endDate.timestamp())
        params['from'] = int(startDate.timestamp())
        
        response = self.session.get(url, params = params, headers = api.SECURE_HEADER)
        
        if response.status_code != 200:
            print(response.status_code, response.content)
            return response.status_code, None

        if asDf == True:
            jsonData = response.json()['candles']
            return response.status_code, self.candlesToDf(jsonData)
        else:
            return response.status_code, response.json()
    
    def candlesToDf(self, jsonData):
        ourData = []
        for candle in jsonData:
            if candle['complete'] == False:
                continue
            newDict = {}
            newDict['OpenTime'] = candle['time']
            newDict['Open'] = float(candle['mid']['o'])
            newDict['High'] = float(candle['mid']['h'])
            newDict['Low'] = float(candle['mid']['l'])
            newDict['Close'] = float(candle['mid']['c'])
            newDict['volume'] = candle['volume']
            ourData.append(newDict)
        df = pd.DataFrame.from_dict(ourData)
        df['OpenTime'] = [parse(x) for x in df.OpenTime]
        return df
    
    def createFile(self, pair, candle, startDate, endDate):
        if os.path.exists(ut.getHisDataFilename('forex', pair, candle)):
            return

        endDate = ut.getUtcFromString(endDate)
        startDate = ut.getUtcFromString(startDate)
    
        candleCount = 5000
        stepDate = self.increments[candle] * candleCount
    
        candleDfs = []
        dateTo = startDate
        while dateTo < endDate:
            dateTo = startDate + dt.timedelta(minutes = stepDate)
            if dateTo > endDate:
                dateTo = endDate
            
            code, df = self.fetchCandles(pair, candle, startDate, dateTo, asDf = True)
            
            if df is not None and df.empty == False:
                candleDfs.append(df)
            elif code != 200:
                print("ERROR", pair, candle, startDate, dateTo)
                break
    
            startDate = dateTo
        
        finalDf = pd.concat(candleDfs)
        finalDf.set_index('OpenTime', inplace = True)
        finalDf.to_pickle(ut.getHisDataFilename('forex', pair, candle))