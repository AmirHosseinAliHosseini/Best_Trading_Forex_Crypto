import downloadHistoricalData
import singleStrategies
import mixSingleStrategy
import applyGapStrategy
import multiStrategy


if __name__ == "__main__":
    downloadHistoricalData.run()
    
    singleStrategies.run()
    
    mixSingleStrategy.run()
    
    applyGapStrategy.run()
    
    multiStrategy.run()