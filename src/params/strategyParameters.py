import numpy as np

#General strategy setting
takeProfit = {
    'crypto': {
    'H4'  : np.arange(0.10, 0.35, 0.05),
    'H1'  : np.arange(0.10, 0.35, 0.05),
    'M30' : np.arange(0.05, 0.25, 0.05),
    'M15' : np.arange(0.05, 0.20, 0.03),
    'M5'  : np.arange(0.02, 0.12, 0.02),
    'M1'  : np.arange(0.01, 0.06, 0.01) 
    },

    'forex': {
    'H4'  : np.arange(0.0050, 0.0160, 0.0020),
    'H1'  : np.arange(0.0050, 0.0160, 0.0020),
    'M30' : np.arange(0.0030, 0.0120, 0.0020),
    'M15' : np.arange(0.0020, 0.0100, 0.0015),
    'M5'  : np.arange(0.0010, 0.0080, 0.0010),
    'M1'  : np.arange(0.0008, 0.0040, 0.0003) 
    }
}

fees = {
    'crypto': 0.01,
    'forex': 0.0006
}

roundNumber = {
    'crypto': 3,
    'forex': 5
}

numberOfBestChosen = 5
savedFinalReturns = 500
strategyMixedGap = np.arange(0, 6, 1)

#Category of strategies
categoryStrategy = [('SMA', ['SMA1', 'SMA2']), ('RSI', ['RSI1', 'RSI2', 'RSI_MA1', 'RSI_MA2']), ('MACD', ['MACD1', 'MACD2']), ('ADX',['ADX'])]

#Option for strategies
#..........................SMA..........................

maWindow_1 = np.arange(5, 21, 3) #6
maWindow_2 = np.arange(15, 42, 3) #9
maWindow_3 = np.arange(25, 100, 5) #15

#.........................RSI_MA........................

rsiWindow = np.arange(8, 24, 2) #8
maWindow = np.arange(8, 20, 2) #6
upperBound = np.arange(60, 95, 5) #7
lowerBound = np.arange(10, 40, 5) #6

#..........................MACD.........................

fastWindow = np.arange(8, 20, 2) #6
slowWindow = np.arange(20, 34, 2) #7
signalWindow = np.arange(7, 18, 2) #6
histDiff = np.arange(3, 7, 1) #4

#..........................ADX..........................

timePeriod = np.arange(12, 20, 2) #4
adxBound = np.arange(20, 40, 5) #4