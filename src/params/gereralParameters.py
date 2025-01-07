#The group of pairs
folders = ['crypto', 'forex']

#Each group's pairs
pairs = {
    'crypto' : ['BTCUSDT', 'ETCUSDT', 'ETHUSDT'],
    'forex' : ['EUR_USD', 'GBP_USD', 'USD_CAD', 'USD_JPY', 'XAU_USD']
}

#Each pair's candle setup
Candle = [ ('H4',  "2020-06-01", "2024-07-01"),
           ('H1',  "2021-06-01", "2024-07-01"), 
           ('M30', "2021-06-01", "2024-07-01"), 
           ('M15', "2023-06-01", "2024-07-01"), 
           ('M5',  "2023-06-01", "2024-07-01"), 
           ('M1',  "2024-01-01", "2024-07-01") ]

#Fees for each group
fees = {
    'crypto': 0.01,
    'forex': 0.0006
}