import pandas as pd
import random


class DataCrawler:
    @staticmethod
    def loadData(fileName, randomNum):
        num_lines = sum(1 for l in open(fileName))
        # idx = random.sample(range(2, 10), 10 - 3 - 1)
        # print(idx)
        # idx.remove(9)
        # print(idx)
        skip_idx = random.sample(range(2, num_lines), num_lines - randomNum - 2)
        data = pd.read_csv(fileName, skiprows=skip_idx)
        print(data)

if __name__ == "__main__":
    DataCrawler.loadData("yellow_tripdata_2017-11.csv", 10)
