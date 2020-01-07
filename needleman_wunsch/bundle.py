import os
import sys
import pandas as pd
import datetime
import csv
import argparse
import Ruler

def data_initialization(datafile):
    """ From a .txt file containing strings to compare, it creates a list of strings,
    without empty strings """
    f = open(datafile, "r")
    lines = f.readlines()
    dataset = [y for y in [x.strip() for x in lines] if y != '']
    if len(dataset) % 2 != 0:
        dataset.pop() 
    return dataset

def strings_comparison(str1, str2):
    ruler = Ruler(str1, str2):
    ruler.compute()
    print("======== distance = " + ruler.distance)
    top, bottom = ruler.report()
    print(top)
    print(bottom)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", help="sequences to analyze")
    args = parser.parse_args()
    datafile = args.datafile
    dataset = data_initialization(datafile)
    for i in range(0, len(dataset), 2):
        strings_comparison(dataset[i], dataset[i + 1])
    return 0


if __name__ == '__main__':
    sys.exit(main())
