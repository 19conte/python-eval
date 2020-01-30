#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from ruler import Ruler

def data_initialization(datafile):
    """ From a .txt file containing strings to compare, it creates a list of strings,
    without empty strings. This list has an even length"""

    with open(datafile) as f:
        lines = f.readlines()
        dataset = [y for y in [x.strip() for x in lines] if y != '']
        if len(dataset) % 2 != 0:
            dataset.pop() 
    return dataset

def strings_comparison(str1 : str, str2 : str):
    """ Displays the distance and the alignments between 2 strings """
    
    ruler = Ruler(str1, str2)
    ruler.compute()
    print("======== distance = " + str(ruler.distance))
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
