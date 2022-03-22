import os
import random
import time
import csv

import requests

from scraper import runNewsScrape






def prevState():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir_path = dir_path + '\\data' 
    print(data_dir_path)
    if os.path.isdir(data_dir_path):
        
        f_path = data_dir_path + "\\last_index_update.csv"

        if not os.listdir(data_dir_path):
            print("Directory is empty")

        else:
            print("Directory is not empty")
            with open(f_path, mode="r") as f:
                last_update = f.readlines()[-1]
                return last_update

    else:
        print("Given directory doesn't exist")

def checkState(url):
    
    # read in the last news update from data directory
    # this contains the last headline from the site
    prev_data = prevState()

    latest_data = runNewsScrape(url)

    # fetch last headline which can either be
    # (1) the same headline, no email is needed
    if prev_data == latest_data:
        return True
    else:
        # (2) a different headline, email is needed 
        return False
    

def main():

    url = "https://www.dax-indices.com/news"
    

    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir_path = dir_path + '\\data' 
    
    if os.path.isdir(data_dir_path):
        
        f_path = data_dir_path + "\\last_index_update.csv"

        if not os.listdir(data_dir_path):
            print("Directory is empty")

        else:
            print("Directory is not empty")
            data = []
            with open(f_path, encoding="utf-8", mode="r" ) as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    if row:
                        print("\n", row) 
                        data.append(row)   
            return data[-1]

    else:
        print("Given directory doesn't exist")

if __name__ == "__main__":
    print("start")
    main()
    print("done")