import csv
import numpy as np
from scipy.stats import kurtosis, skew


def read_data():
    input_file = open("msci.csv", "rb")
    reader = csv.reader(input_file)

    data = []

    for row in reader:
        data.append(float(row[0]))

    print data
    print "\nMean: %f" % np.mean(data)
    print "Standard Deviation: %f" % np.std(data)
    print "Kurtosis: %f" % kurtosis(data)
    print "Skew: %f" % skew(data)

    input_file.close()


def main():
    read_data()


main()
