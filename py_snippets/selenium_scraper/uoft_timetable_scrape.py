from preparedriver import prepare_driver

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re
import time
import csv
import argparse


def scrape(driver, path="courses.txt"):
    with open(path, "r") as f:
        courses = [line[:-1] for line in f]
    f = open("./course_avalibility.csv", "w", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(['course', 'lecture', 'time', 'place', 'prof', 'avaliable', 'class_size', 'waitlist'])

    driver.get("https://timetable.iit.artsci.utoronto.ca/")
    WebDriverWait(driver, timeout=10).\
                  until(EC.presence_of_all_elements_located((By.ID, 'courseCode')))

    for course_name in courses:
        print("current:",course_name, end="\r")
        c_input = driver.find_element_by_css_selector("#courseCode")
        c_input.clear()
        c_input.send_keys(course_name)
        driver.find_element_by_css_selector("#searchButton").click()
        time.sleep(2)
        WebDriverWait(driver, timeout=10).\
                      until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sectionData')))
        lecs = driver.find_elements_by_css_selector(".sectionData ")
        for l in lecs:
            if "sectionEnrol" in l.get_attribute("class"):
                continue
            infos = [i.text for i in l.find_elements_by_css_selector("td")]
            row = [course_name]
            if infos[0][:3] != "LEC":
                continue
            infos[1] = infos[1].replace("\n", "; ")
            infos[2] = infos[2].replace("\n", "; ")
            if "no" in infos[-2].lower():
                infos[-1] = 0
            else:
                infos[-1] = int(re.findall("\d+", infos[-2])[0])
            infos[-3], infos[-2] = [int(x) for x in re.findall("\d+", infos[-3])]
            writer.writerow([course_name] + infos)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape UofT time table')
    parser.add_argument('-p', help='Give a text file of courses, one course for each line', metavar="path")
    parser.add_argument('-d', help='Give a link to Chrome driver', metavar="driver")
    args = parser.parse_args()
    driver = prepare_driver(args.d.replace("\\", "/")) if args.d else prepare_driver()
    scrape(driver, args.p.replace("\\", "/")) if args.p else scrape(driver)
    
    
    