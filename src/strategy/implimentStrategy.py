import vectorbt as vbt
from numba import njit
import numpy as np

#..........................SMA..........................

SMA = vbt.IndicatorFactory.from_talib('SMA')

@njit
def SMA_Str_1(ma1, ma2):
    trend = np.where(ma1 < ma2, -1, 0)
    trend = np.where(ma1 > ma2, 1, trend)
    return trend

def SMA_Strategy_1(close, maWindow_1 = 5, maWindow_2 = 15):   
    if maWindow_1 >= maWindow_2:
        return np.zeros(len(close))
    
    ma1 = SMA.run(close, maWindow_1).real.to_numpy()
    ma2 = SMA.run(close, maWindow_2).real.to_numpy()

    return SMA_Str_1(ma1, ma2)


@njit
def SMA_Str_2(ma1, ma2, ma3):
    
    trend = np.where((ma1 < ma2) * (ma2 < ma3), -1, 0)
    trend = np.where((ma1 > ma2) * (ma2 > ma3), 1, trend)
    return trend

def SMA_Strategy_2(close, maWindow_1 = 5, maWindow_2 = 15, maWindow_3 = 25):   
    if maWindow_1 >= maWindow_2 or maWindow_2 >= maWindow_3:
        return np.zeros(len(close))
    
    ma1 = SMA.run(close, maWindow_1).real.to_numpy()
    ma2 = SMA.run(close, maWindow_2).real.to_numpy()
    ma3 = SMA.run(close, maWindow_3).real.to_numpy()

    return SMA_Str_2(ma1, ma2, ma3)

#..........................RSI..........................

RSI = vbt.IndicatorFactory.from_talib('RSI')

@njit
def RSI_Str_1(rsi, upperBound, lowerBound):
    rsi_prev = np.roll(rsi, 1)

    trend = np.where((rsi_prev > lowerBound) * (rsi < lowerBound), -1, 0)
    trend = np.where((rsi_prev < upperBound) * (rsi > upperBound), 1, trend)
    return trend

def RSI_Strategy_1(close, rsiWindow = 14, lowerBound = 30 , upperBound = 70):
    rsi = RSI.run(close, rsiWindow).real.to_numpy()

    return RSI_Str_1(rsi, upperBound, lowerBound)


@njit
def RSI_Str_2(rsi, upperBound, lowerBound):
    rsi_prev = np.roll(rsi, 1)

    trend = np.where((rsi_prev > upperBound) * (rsi < upperBound), -1, 0)
    trend = np.where((rsi_prev < lowerBound) * (rsi > lowerBound), 1, trend)
    return trend

def RSI_Strategy_2(close, rsiWindow = 14, lowerBound = 30 , upperBound = 70):
    rsi = RSI.run(close, rsiWindow).real.to_numpy()
    rsi_prev = np.roll(rsi, 1)

    return RSI_Str_2(rsi, upperBound, lowerBound)

#.........................RSI_MA........................

@njit
def RSI_MA_str_1(rsi, ma, upperBound, lowerBound):
    rsi_prev = np.roll(rsi, 1)

    trend = np.where((rsi_prev > ma) * (rsi < ma) * (ma > upperBound), -1, 0)
    trend = np.where((rsi_prev < ma) * (rsi > ma) * (ma < lowerBound), 1, trend)
    return trend

def RSI_MA_Strategy_1(close, rsiWindow = 14, maWindow = 8, lowerBound = 30 , upperBound = 70):
    rsi = RSI.run(close, rsiWindow).real.to_numpy()
    ma = SMA.run(rsi, maWindow).real.to_numpy()

    return RSI_MA_str_1(rsi, ma, upperBound, lowerBound)


@njit
def RSI_MA_str_2(rsi, ma, upperBound, lowerBound):
    rsi_prev = np.roll(rsi, 1)

    trend = np.where((rsi_prev > ma) * (rsi < ma) * (ma < lowerBound), -1, 0)
    trend = np.where((rsi_prev < ma) * (rsi > ma) * (ma > upperBound), 1, trend)
    return trend

def RSI_MA_Strategy_2(close, rsiWindow = 14, maWindow = 8, lowerBound = 30 , upperBound = 70):
    rsi = RSI.run(close, rsiWindow).real.to_numpy()
    ma = SMA.run(rsi, maWindow).real.to_numpy()

    return RSI_MA_str_2(rsi, ma, upperBound, lowerBound)

#..........................MACD.........................

MACD = vbt.IndicatorFactory.from_talib('MACD')

@njit
def MACD_str_1(macd, hist, histDiff):
    histSign = np.where(hist > 0, 1, -1)
    histSum = np.roll(histSign, 1)

    for i in np.arange(2, histDiff + 1):
        histSum += np.roll(histSign, i)

    trend = np.where((macd > 0) * (histSign == -1) * (histSum == histDiff), -1, 0)
    trend = np.where((macd < 0) * (histSign == 1) * (histSum == -histDiff), 1, trend)
    return trend

def MACD_Strategy_1(close, fastWindow = 12, slowWindow = 26 , signalWindow = 9, histDiff = 5):
    macd = MACD.run(close, fastWindow, slowWindow, signalWindow)

    return MACD_str_1(macd.macd.to_numpy(), macd.macdhist.to_numpy(), histDiff)


@njit
def MACD_str_2(macd, hist, histDiff):
    histSign = np.where(hist > 0, 1, -1)
    histSum = np.roll(histSign, 1)

    for i in np.arange(2, histDiff + 1):
        histSum += np.roll(histSign, i)

    trend = np.where((macd < 0) * (histSign == -1) * (histSum == histDiff), -1, 0)
    trend = np.where((macd > 0) * (histSign == 1) * (histSum == -histDiff), 1, trend)
    return trend

def MACD_Strategy_2(close, fastWindow = 12, slowWindow = 26 , signalWindow = 9, histDiff = 5):
    macd = MACD.run(close, fastWindow, slowWindow, signalWindow)

    return MACD_str_2(macd.macd.to_numpy(), macd.macdhist.to_numpy(), histDiff)