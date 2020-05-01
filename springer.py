from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
driver = webdriver.Chrome("./chromedriver_win32/chromedriver")


df = pd.read_excel (r'Free+English+textbooks.xlsx')
links = df.iloc[:,18]
for i in range(348,len(links)):
    link = links.iloc[i]
    title = df.iloc[i,0]
    PATHData = 'C:/Users/ludiv/Documents/Aide_au_diag/doc_a_lire/new/springer/'+title+'.pdf'
    if os.path.exists(PATHData)==False:
        driver.get(link)
        button = driver.find_element_by_xpath("//a[@title='Download this book in PDF format']")

        ref = button.get_attribute('href')
        r = requests.get(ref, allow_redirects=True)
        open(PATHData, 'wb').write(r.content)

for i in range(348,len(links)):
    link = links.iloc[i]
    title = df.iloc[i,0]
    driver.get(link)
    try:        
        PATHData = 'C:/Users/ludiv/Documents/Aide_au_diag/doc_a_lire/new/springer/EPUB/'+title+'.EPUB'
        if os.path.exists(PATHData)==False:
            button = driver.find_element_by_xpath("//a[@title='Download this book in EPUB format']")

            ref = button.get_attribute('href')
            r = requests.get(ref, allow_redirects=True)
            open(PATHData, 'wb').write(r.content)
    except:
        pass
