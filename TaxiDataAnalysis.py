from DataSampling import DataSampling
from datetime import datetime
from pandas import DataFrame
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from math import sqrt


class TaxiDataAnalysis:
    def __init__(self, sourceDataFile, destDataFile, selectedCols, dataNum):
        self.sourceDataFile = sourceDataFile
        self.destDataFile = destDataFile
        self.selectedCols = selectedCols
        self.dataNum = dataNum

    def plotFareAndTipDistribution(self):
        data = self.__getProcessedTaxiData()
        plt.scatter(data.fare_amount.tolist(), data.tip_amount.tolist())
        plt.xlabel("Fair_amount")
        plt.ylabel("Tip_amount")
        plt.title("Distribution of the Fare_amounts and Tip_amounts")
        plt.show()

    def preditByLinearRegression(self):
        data = self.__getProcessedTaxiData()
        features = ["day_night", "passenger_count",
                    "trip_distance", "PULocationID", "DOLocationID"]
        X = pd.concat([data[features], data.filter(regex="payment_type_.*")], axis=1)
        y = data["fare_amount"]

        kfold = KFold(5, False)
        mse = []
        for train, test in kfold.split(X, y):
            linearRegression = LinearRegression()
            linearRegression.fit(X.iloc[train], y.iloc[train])
            y_pred = linearRegression.predict(X.iloc[test])
            mse.append(self.__measureMeanSquaredError(y.iloc[test], y_pred))

        print(mse)
        print("Linear regression average mse: %d" % np.mean(mse))
        print("Linear regression average standard deviation: %d" % np.std(mse))

    def preditByKNNRegression(self):
        data = self.__getProcessedTaxiData()
        features = ["day_night", "passenger_count",
                    "trip_distance", "PULocationID", "DOLocationID"]
        X = pd.concat([data[features], data.filter(regex="payment_type_.*")], axis=1)
        y = data["fare_amount"]

        kfold = KFold(5, False)
        splitFold = kfold.split(X, y)

        mse = []
        for train, test in splitFold:
            testIdx = test[:len(test)//2]
            kOptimizeIdx = test[len(test)//2:]
            k = self.__getOptimalK(X.iloc[train],
                                   y.iloc[train],
                                   X.iloc[kOptimizeIdx],
                                   y.iloc[kOptimizeIdx])

            regressor = KNeighborsRegressor(k)
            regressor.fit(X.iloc[train], y.iloc[train])
            y_pred = regressor.predict(X.iloc[testIdx])
            mse.append(self.__measureMeanSquaredError(y.iloc[testIdx], y_pred))

        print(mse)
        print("KNN average mse: %d" % np.mean(mse))
        print("KNN average standard deviation: %d" % np.std(mse))

    def __getProcessedTaxiData(self):
        if not os.path.exists(destDataFile):
            return self.__preProcessTaxiData()
        else:
            return DataSampling.loadProcessedData(destDataFile)

    def __preProcessTaxiData(self):
        data = DataSampling.loadData(sourceDataFile, dataNum, selectedCols)
        self.__convertTimeToDayOrNight(data)
        self.__createPaymentDummyData(data)
        self.__calculateTipRate(data)
        DataSampling.saveData(destDataFile, data)
        return data

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

    def __calculateTipRate(self, data):
        data["tip_rate_20"] = data.apply(
            lambda x: 0 if x.fare_amount == 0 or x.tip_amount / x.fare_amount < 0.2 else 1, 1)

    def __plotPredictComparison(self, actual, predicted):
        resultDataFrame = pd.DataFrame({'Actual': actual, 'Predicted': predicted})
        resultDataFrame.head(50).plot(kind='bar', figsize=(10, 8))
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.show()

    def __measureMeanSquaredError(self, actual, predicted):
        return mean_squared_error(actual, predicted)

    def __getOptimalK(self, X, y, kOptimizeX, kOptimizey):
        rmse = []
        for k in range(1, 11):
            regressor = KNeighborsRegressor(n_neighbors=k)
            regressor.fit(X, y)
            y_pred = regressor.predict(kOptimizeX)
            error = sqrt(mean_squared_error(kOptimizey, y_pred))
            rmse.append(error)
        return rmse.index(min(rmse)) + 1

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
    taxiDataAnalysis = TaxiDataAnalysis(
        sourceDataFile,
        destDataFile,
        selectedCols,
        dataNum)
    # taxiDataAnalysis.plotFareAndTipDistribution()
    taxiDataAnalysis.preditByLinearRegression()
    taxiDataAnalysis.preditByKNNRegression()
