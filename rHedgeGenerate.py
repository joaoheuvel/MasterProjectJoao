import csv
import math
import numpy as np
import statsmodels.api as sm
from scipy.stats import kurtosis, skew
import pandas as pd


def calc_rhedge():
    currencies, r_msci, r_cf = read_data()

    w_hedge = []
    r_hedge = []
    skewness_data = []
    kurtosis_data = []
    sharpe = []

    for j in range(0, r_cf.__len__()):
        w_hedge.append([])
        r_hedge.append([])
        skewness_data.append([])
        kurtosis_data.append([])
        sharpe.append([])

    interval = 60

    for i in range(0, r_cf.__len__()):
        for month in range(interval+1, r_msci.__len__()):

            x = r_cf[i][month-interval-1:month-1]
            y = r_msci[month-interval-1:month-1]

            skewness_data[i].append(skew(x))
            kurtosis_data[i].append(kurtosis(x))
            sharpe[i].append((math.sqrt(interval) * (np.mean(x) / np.std(x))))

            model = sm.OLS(y, x).fit()
            w_hedge_val = -model.params
            r_hedge_val = r_msci[month] + (w_hedge_val)*r_cf[i][month]

            w_hedge[i].append(w_hedge_val)
            r_hedge[i].append(r_hedge_val)

    write_csv(currencies, w_hedge, r_hedge, skewness_data, kurtosis_data, sharpe)
    print("Total currencies: %d" % (i + 1))
    print("Total months: %d" % (month - interval))


def write_csv(currencies, w_hedge, r_hedge, skewness_data, kurtosis_data, sharpe):


    for i in range(0, currencies.__len__()):
        output_file = open("output/%s_hedged_data.csv" % currencies[i], "w", encoding="utf8")
        output_file.write("w_hedge, r_hedge, skewness, kurtosis, sharpe\n")

        for j in range(0, w_hedge[0].__len__()):
            output_file.write("%f, %f, %f, %f, %f\n" % (w_hedge[i][j], r_hedge[i][j], skewness_data[i][j], kurtosis_data[i][j], sharpe[i][j]))


    output_file.close()


def read_data():
    input_file = open("testData.csv", "rt", encoding="utf8")
    reader = csv.reader(input_file)

    currencies = 0
    r_msci = []
    r_cf = []
    i = 0

    for row in reader:
        if i is 0:
            i = 1
            currencies = row[1:]
            for j in range(0, row.__len__() - 1):
                r_cf.append([])
        else:
            r_msci.append(float(row[0]))
            for j in range(1, row.__len__()):
                r_cf[j - 1].append(float(row[j]))

    return currencies, r_msci, r_cf


def main():
    calc_rhedge()


main()
