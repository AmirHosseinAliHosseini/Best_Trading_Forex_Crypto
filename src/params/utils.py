import pandas as pd
import datetime as dt
from dateutil.parser import parse

def getUtcFromString(strDate):
    d = parse(strDate)
    return d.replace(tzinfo = dt.timezone.utc)
    
def getHisDataFilename(folder, pair, candle):
    return f'../data/{folder}/downloaded/{pair}-{candle}.pkl'

def openfile(folder, pair, candle):
    return pd.read_pickle(f'../data/{folder}/downloaded/{pair}-{candle}.pkl')

def getSingleStrategyFileName(folder, pair, strategy, candle):
    return f'../data/{folder}/singleStrategy/{pair}-{candle}-{strategy}.pkl'

def getMixSingleStrategyFileName(folder, pair, strategy, candle):
    return f"../data/{folder}/mixSingleStrategy/{pair}-{candle}-{strategy}.pkl"

def getApplyGapStrategyFileName(folder, pair, strategy, candle, gap):
    return f"../data/{folder}/applyGapStrategy/{pair}-{candle}-{strategy}-G{gap}.pkl"

def getMUltiStrategyFileName(folder, pair, candle):
    return f"../data/{folder}/multiStrategy/{pair}-{candle}.xlsx"
