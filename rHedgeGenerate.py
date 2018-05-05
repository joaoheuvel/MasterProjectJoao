import csv
import math
import numpy as np
import statsmodels.api as sm
from scipy.stats import kurtosis, skew


def calc_rhedge():
    # We first raed the data from the files and store them in the appropriate variables
    currencies, r_msci, r_cf = read_data()

    # Then we initialize the variables which are going to be used in the calculations
    w_hedge = []
    r_hedge = []
    skewness_data = []
    kurtosis_data = []
    sharpe = []

    # And then make them into appropriate sized 2D arrays for all the currencies
    for j in range(0, r_cf.__len__()):
        w_hedge.append([])
        r_hedge.append([])
        skewness_data.append([])
        kurtosis_data.append([])
        sharpe.append([])

    # Here we set the interval that we are using for our moving window
    interval = 60

    # The outer loop is to loop through and calculate the data for all currencies
    for i in range(0, r_cf.__len__()):
        # The inner loop is to loop through all the months and calculate data
        for month in range(interval+1, r_msci.__len__()):
            # We take the interval-sized data for r_cf and r_msci
            x = r_cf[i][month - interval - 1:month - 1]
            y = r_msci[month - interval - 1:month - 1]

            # And calculate Skew, Kurtosis and Sharpe's Ratio
            skewness_data[i].append(skew(x))
            kurtosis_data[i].append(kurtosis(x))
            sharpe[i].append((math.sqrt(interval) * (np.mean(x) / np.std(x))))

            # We then make an OLS Regression model and then retrieve the parameters of the equation
            model = sm.OLS(y, x).fit()
            w_hedge_val = -model.params
            # The r_hedge is then calculated
            r_hedge_val = r_msci[month] + (w_hedge_val)*r_cf[i][month]

            # And these values are then stored in the 2D arrays
            w_hedge[i].append(w_hedge_val)
            r_hedge[i].append(r_hedge_val)

    # We then pass all the data to the write_csv() and create CSV files for all the currencies
    write_csv(currencies, w_hedge, r_hedge, skewness_data, kurtosis_data, sharpe)
    # We then print the numbers for data we processed and exit the function
    print("Total currencies: %d" % (i + 1))
    print("Total months: %d" % (month - interval))


def write_csv(currencies, w_hedge, r_hedge, skewness_data, kurtosis_data, sharpe):
    # This function is used to create the CSV files for all currencies
    for i in range(0, currencies.__len__()):
        # We first open the CSV file
        output_file = open("output/%s_hedged_data.csv" % currencies[i], "w", encoding="utf8")
        # We then write the titles to each CSV file
        output_file.write("w_hedge, r_hedge, skewness, kurtosis, sharpe\n")

        # And finally print all the data that we calculated in the CSV files
        for j in range(0, w_hedge[0].__len__()):
            output_file.write("%f, %f, %f, %f, %f\n" % (w_hedge[i][j], r_hedge[i][j], skewness_data[i][j], kurtosis_data[i][j], sharpe[i][j]))

        # And we close the files
        output_file.close()


def read_data():
    # We open the CSV file that we are supposed to read
    input_file = open("testData.csv", "rt", encoding="utf8")
    # And we create a reader object for the file
    reader = csv.reader(input_file)

    # We initialise all the variables that are going to be used for reading
    currencies = 0
    r_msci = []
    r_cf = []
    i = 0

    # We read one line at a time and separate the data of each currency
    for row in reader:
        if i is 0:
            # In this case, we are reading the first row which contains the titles of the column. So we separate the row
            # and then extract the currency names from the same
            i = 1
            currencies = row[1:]
            for j in range(0, row.__len__() - 1):
                # Here we create an appropriate sized 2-dimensional array for all the currencies that we have to process
                r_cf.append([])
        else:
            # Here, we add the data from the rows into appropriate variables for each currency
            r_msci.append(float(row[0]))
            for j in range(1, row.__len__()):
                r_cf[j - 1].append(float(row[j]))

    # We close the input file
    input_file.close()

    # We then return all the variables to the calling function
    return currencies, r_msci, r_cf


def main():
    # Calling the calc_rhedge() function
    calc_rhedge()


main()
