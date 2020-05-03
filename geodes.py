# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:52:41 2020

@author: Vane
"""

from selenium import webdriver
import time
import csv
import pandas as pd
driver = webdriver.Chrome("./chromedriver_win32/chromedriver")

def extractDataFromSiteGeodes(siteweb):
    driver.get(siteweb)
    time.sleep(5)
    python_button = driver.find_element_by_xpath("//a[@id= 'tm_table']")
    python_button.click()
    time.sleep(5)
    python_button = driver.find_element_by_xpath("//th[@class= 'dt-head-left sorting_asc']")
    python_button.click()
    table = driver.find_element_by_xpath("//tbody")
    rows = table.find_elements_by_xpath("//tr[@role= 'row']")
    text = [x.text for x in rows]
    column=["".join(text[i].split()[2:]) for i in range(2,103)]#50= N/A-divisionpar0 #2-102
    return column

def writecsv(fileToWrite, column, nameColumn, numberOfColumn):
    df = pd.read_csv(fileToWrite)
    df[nameColumn] = column
    df.to_csv(fileToWrite, index=numberOfColumn)


siteweb="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
fileToWrite='./data/example/2020_Copy.csv'
numberOfColumn=3
nameColumn="asthme_hosp"
column=extractDataFromSiteGeodes(siteweb)
print(column)
writecsv(fileToWrite, column, nameColumn, numberOfColumn)


#ASTHME
baseAsthme="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
base=baseAsthme
weeks=[str(2019)+'-S0'+str(i) for i in range(1,10)]+[str(2019)+'-S'+str(i) for i in range(10,55)]+[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,19)]
sitesweb=[base[:-37]+str(week)+base[-29:] for week in weeks]
print(sitesweb)
# siteweb=base[:-37]+str(2019)+'-S0'+str(1)+base[-29:]
# print(siteweb)

