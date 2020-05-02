# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:52:41 2020

@author: Vane
"""

from selenium import webdriver
import time
import csv
driver = webdriver.Chrome("./chromedriver_win32/chromedriver")

siteweb="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
driver.get(siteweb)
time.sleep(5)
python_button = driver.find_element_by_xpath("//a[@id= 'tm_table']")
python_button.click()
python_button = driver.find_element_by_xpath("//th[@class= 'dt-head-left sorting_asc']")
python_button.click()
table = driver.find_element_by_xpath("//tbody")
rows = table.find_elements_by_xpath("//tr[@role= 'row']")
text = [x.text for x in rows]
column=["".join(text[i].split()[2:]) for i in range(2,102)]#50= N/A-divisionpar0 #2-102
print(column)
column=zip(["".join(text[i].split()[2:]) for i in range(2,102)])#50= N/A-divisionpar0 #2-102
print(column)

#write column on csv 
with open('2020-s16.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    for row in column:
        writer.writerow(row)


