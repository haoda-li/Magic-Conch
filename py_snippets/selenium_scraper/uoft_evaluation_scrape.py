import selenium
import time
import json
import argparse

import re
from os import listdir
import os
import pandas as pd

from bs4 import BeautifulSoup
from requests import get


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from preparedriver import prepare_driver


""" Scrape UofT Course Evaluation
"""


def scrape(driver, path):
    driver.get("https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=RzzZcfLdM2FeMolqQu&userid=HpZf268Q2pOk3ecPriBU-rriu3vO-Gi&lng=en")
    WebDriverWait(driver, timeout=10).\
                  until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gData')))
    s = Select(driver.find_element_by_css_selector('#fbvGridPageSizeSelectBlock > select'))
    s.select_by_value('100')

    data = []
    for i in range(1, 236):
        time.sleep(3)
        WebDriverWait(driver, timeout=10).\
                  until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gData')))
        data += [e.text for e in driver.find_elements_by_css_selector(".gData")]

        page = driver.find_element_by_css_selector("#gridPaging__getFbvGrid")
        page.send_keys(Keys.BACK_SPACE)
        page.send_keys(Keys.BACK_SPACE)
        page.send_keys(Keys.BACK_SPACE)
        page.send_keys(str(i))
        page.send_keys(Keys.ENTER)
        if len(data) >= 1000:
            with open(path + "t" + str(i) + ".txt", "w") as f:
                for line in data:
                    f.write(line + "\n")
            data.clear()
    with open(path + "t" + str(i) + ".txt", "w") as f:
        for line in data:
            f.write(line + "\n")

            
def save(path):
    files = [path + f for f in listdir("../scraped/")]

    d = {
        "course_name": [],
        "course": [],
        "prof": [],
        "term": [],
        "year": [],
        "q1": [],
        "q2": [],
        "q3": [],
        "q4": [],
        "q5": [],
        "q6": [],
        "enthusiasm": [],
        "workload": [],
        "recommend": [],
        "number_student": [],
        "number_response": []
    }

    keys = list(reversed(list(d.keys())))

    for f in files:
        if f[11] != "t":
            continue
        with open(f, "r") as f:
            for line in f:
                want = list(reversed(line[:-1].split(" ")))
                for i in range(len(keys) - 3):
                    d[keys[i]].append(want[i])
                rest = " ".join(list(reversed(want[i+1: -2])))
                find = re.search("\S\S\S\d\d\d\S\d.*LEC\d\d\d\d", rest)
                if not find:
                    for i in range(len(keys) - 3):
                        d[keys[i]].pop()
                else:
                    d['course_name'].append(rest[:find.start()].strip())
                    d['course'].append(rest[find.start():find.end()][:8])
                    d['prof'].append(rest[find.end():])
    df = pd.DataFrame(d)
    df = df.drop_duplicates()
    df.to_csv(path + "evaluation.csv", index=False)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape UofT course evaluation')
    parser.add_argument('-p', help='Give a folder path', metavar="path")
    parser.add_argument('-d', help='Give a link to Chrome driver', metavar="driver")
    args = parser.parse_args()
    driver = prepare_driver(args.d.replace("\\", "/")) if args.d else prepare_driver()
    path = args.p.replace("\\", "/") if args.p else "./scraped/"
    if not os.path.isdir(path):
        os.mkdir(path)
    scrape(driver, path)
    save(path)