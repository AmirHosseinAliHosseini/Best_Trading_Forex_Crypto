import sys

sys.path.append('./params')
import gereralParameters as gparam

sys.path.append('./api')
import oandaAPI
import binanceAPI

API = {
    'crypto' : binanceAPI.BinanceAPI(),
    'forex' : oandaAPI.OandaAPI()
}

def run():
    print('\n\nStart the historical data download:')
    for folder in gparam.folders:
        for pair in gparam.pairs[folder]:
            for cndl in gparam.Candle:
                print('Downloading:', folder, pair, cndl[0])
                API[folder].createFile(pair, cndl[0], cndl[1], cndl[2])
    print('\n\nDownload finished.')
    
if __name__ == "__main__":
    run()