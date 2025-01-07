import vectorbt as vbt
import implimentStrategy as strategy

#..........................SMA..........................

ind_SMA_1 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['maWindow_1', 'maWindow_2'], 
    output_names = ['value']
).from_apply_func(strategy.SMA_Strategy_1,
    maWindow_1 = 5,
    maWindow_2 = 15,
    keep_pd = True,
)

ind_SMA_2 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['maWindow_1', 'maWindow_2', 'maWindow_3'], 
    output_names = ['value']
).from_apply_func(strategy.SMA_Strategy_2,
    maWindow_1 = 5,
    maWindow_2 = 15,
    maWindow_3 = 25,
    keep_pd = True,
)

#..........................RSI..........................

ind_RSI_1 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['rsiWindow', 'lowerBound', 'upperBound'], 
    output_names = ['value']
).from_apply_func(strategy.RSI_Strategy_1,
    rsiWindow = 14,
    lowerBound = 30,
    upperBound = 70,
    keep_pd = True,
)

ind_RSI_2 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['rsiWindow', 'lowerBound', 'upperBound'], 
    output_names = ['value']
).from_apply_func(strategy.RSI_Strategy_2,
    rsiWindow = 14,
    lowerBound = 30,
    upperBound = 70,
    keep_pd = True,
)

#.........................RSI_MA........................

ind_RSI_MA_1 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['rsiWindow', 'maWindow', 'lowerBound', 'upperBound'], 
    output_names = ['value']
).from_apply_func(strategy.RSI_MA_Strategy_1,
    rsiWindow = 14,
    maWindow = 8,
    lowerBound = 30,
    upperBound = 70,
    keep_pd = True,
)

ind_RSI_MA_2 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['rsiWindow', 'maWindow', 'lowerBound', 'upperBound'], 
    output_names = ['value']
).from_apply_func(strategy.RSI_MA_Strategy_2,
    rsiWindow = 14,
    maWindow = 8,
    lowerBound = 30,
    upperBound = 70,
    keep_pd = True,
)

#..........................MACD.........................

ind_MACD_1 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['fastWindow', 'slowWindow', 'signalWindow', 'histDiff'], 
    output_names = ['value']
).from_apply_func(strategy.MACD_Strategy_1,
    fastWindow = 12,
    slowWindow = 26,
    signalWindow = 9,
    histDiff = 5,
    keep_pd = True,
)

ind_MACD_2 = vbt.IndicatorFactory(class_name = 'Combination', short_name = 'comb',
    input_names = ['close'],
    param_names = ['fastWindow', 'slowWindow', 'signalWindow', 'histDiff'], 
    output_names = ['value']
).from_apply_func(strategy.MACD_Strategy_2,
    fastWindow = 12,
    slowWindow = 26,
    signalWindow = 9,
    histDiff = 5,
    keep_pd = True,
)
