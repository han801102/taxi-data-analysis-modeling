from DataSampling import DataSampling
from datetime import datetime
from pandas import DataFrame
import pandas as pd


class TaxiDataAnalysis:
    def __init__(self, sourceDataFile, destDataFile, selectedCols, dataNum):
        self.sourceDataFile = sourceDataFile
        self.destDataFile = destDataFile
        self.selectedCols = selectedCols
        self.dataNum = dataNum

    def analyze(self):
        self.__preProcessTaxiData()

    def __preProcessTaxiData(self):
        data = DataSampling.loadData(sourceDataFile, dataNum, selectedCols)
        self.__convertTimeToDayOrNight(data)
        self.__createPaymentDummyData(data)
        DataSampling.saveData(destDataFile, data)

    def __convertTimeToDayOrNight(self, data):
        dateFormat = "%Y-%m-%d %H:%M:%S"
        data["day_night"] = [
            1 if 18 > datetime.strptime(row, dateFormat).hour > 6 else 0
            for row
            in data["tpep_pickup_datetime"]]
        data.drop('tpep_pickup_datetime', 1, inplace=True)

    def __createPaymentDummyData(self, data):
        paymentTypes = data.payment_type.unique()
        for payment in paymentTypes:
            data["payment_type_%s" % payment] = data.apply(
                lambda x: 1 if x["payment_type"] == payment else 0, 1)

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
    sourceDataFile = "yellow_tripdata_2017-11.csv"
    destDataFile = "taxi-result.csv"
    dataNum = 10000
    TaxiDataAnalysis(
        sourceDataFile,
        destDataFile,
        selectedCols,
        dataNum).analyze()
