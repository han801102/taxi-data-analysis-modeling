import pandas as pd
import random


class DataSampling:
    @staticmethod
    def loadData(fileName, randomNum, selectedCols):
        num_lines = sum(1 for l in open(fileName))
        skip_idx = random.sample(range(2, num_lines),
                                 num_lines - randomNum - 2)
        return pd.read_csv(fileName, skiprows=skip_idx, usecols=selectedCols)

    @staticmethod
    def loadProcessedData(fileName):
        return pd.read_csv(fileName)

    @staticmethod
    def saveData(fileName, data):
        data.to_csv(fileName, index=False)

if __name__ == "__main__":
    selectedCols = ["VendorID",
                    "tpep_pickup_datetime",
                    "passenger_count",
                    "trip_distance",
                    "PULocationID",
                    "DOLocationID",
                    "payment_type",
                    "fare_amount",
                    "tip_amount"]
    fileName = "yellow_tripdata_2017-11.csv"
    data = DataSampling.loadData(fileName, 10, selectedCols)
