import selenium
import time
import json

import re
from os import listdir
import pandas as pd

from bs4 import BeautifulSoup
from requests import get

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

""" Scrape UofT Course Evaluation
"""

def prepare_driver(path, headless=True):
    """ Initiate the Chrome driver installed in path
    """
    
    options = Options()
    # make the Chrome driver runs in the background
    if headless:
        options.add_argument('-headless')
    options.add_argument("--lang=en-US")
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(path, options=options)
    return driver


def scrape(path="./scraped/", driver):
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

            
def save(path="./scraped/"):
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
    driver = prepare_driver("./chromedriver")
    scrape(driver = driver)
    save()