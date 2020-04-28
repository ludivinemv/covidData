# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:52:41 2020

@author: ludiv
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
driver = webdriver.Chrome("./chromedriver_win32/chromedriver")




''' *****************************************'''
''' *************Site 1**********************'''
''' *****************************************'''
def DataGouvExtraction(siteweb,site, detail):
    driver = webdriver.Chrome("./chromedriver_win32/chromedriver")
    driver.get(siteweb)
    #resources-list
    resourceClass = driver.find_element_by_xpath("//div[@class='resources-list']")
    #just display the text in this resources_list to try
    # h4 = resourceClass.find_element_by_xpath(".//h4[@class='resource-type']")
    # h4.text
    # #card with the files inside. It should be  for loop with @class = instead of id= but for the moment class doesn't work
    articles = resourceClass.find_elements_by_xpath(".//article")
    #Now for all articles that e want on the page
    dossier = 'Data/'+ site+'/'+ detail
    os.makedirs(dossier, exist_ok=True) 
    for i in range(len(articles)):
        article = articles[i]
        #obtain the name of the csv
        classN = article.find_element_by_class_name('ellipsis')
        name = classN.text
        PATHData = dossier + '/' + name
        if os.path.exists(PATHData)==False:      
            #obtain the href
            id_article = article.get_attribute('id') # display the id of the current article
            footer = article.find_element_by_xpath(".//footer")
            toolbar = footer.find_elements_by_xpath(".//div")
            classlink = toolbar[1].find_elements_by_xpath(".//a")
            ref = classlink[1].get_attribute('href') #Link to download 
            # download the file
            r = requests.get(ref, allow_redirects=True)
            open(PATHData, 'wb').write(r.content)
site = 'DataGouv'
#content = driver.page_source
# pour ce site csv a telecharger sont:
# dans la class='resources-list'
# article id='resource-NUMBERs' class='card resource-card'
# <article id="resource-63352e38-d353-4b54-bfd1-f1b3ee1cabd7" class="card resource-card ">
# en dessous, il y a card body (on en veut pas)
# et <footer> --> <div class="resource-card-actions btn-toolbar">
# en dessous <a href="http..." class = "btn btn-sm btn-primary" download>Télécharger</a>

    #driver.get('https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/')
siteweb ='https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/'
detail = 'DataGouv_donnes_hospitalieres_covid'
DataGouvExtraction(siteweb,site, detail)

siteweb = 'https://www.data.gouv.fr/fr/datasets/donnees-des-urgences-hospitalieres-et-de-sos-medecins-relatives-a-lepidemie-de-covid-19/'
detail = 'DataGouv_donnes_urgences_et_sos_medecin_covid'
DataGouvExtraction(siteweb,site, detail)





''' *****************************************'''
''' *************Site 2**********************'''
''' *****************************************'''
driver.get('https://geodes.santepubliquefrance.fr/#c=indicator&i=covid_hospit_incid.incid_rea&s=2020-04-28&selcodgeo=02&t=a01')
site = 'Geodes'

















#JUST EXAMPLES FROM internet here

# aaa = resourceClass.find_element_by_css_selector('.card.resource-card a').get_attribute('href')
# get_div = resourceClass.find_elements_by_tag_name('a',href=True)
'''************ With beautiful soup*****************'''

#soup = BeautifulSoup(content)
# listhref = []
# for link in soup.find_all('a',href=True):
#     listhref.append(link.get('href'))



# for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
#     name=a.find('div', attrs={'class':'_3wU53n'})
#     price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
#     rating=a.find('div', attrs={'class':'hGSR34 _2beYZw'})
# products.append(name.text)
# prices.append(price.text)
# ratings.append(rating.text)

# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
# df.to_csv('products.csv', index=False, encoding='utf-8')






# #example with 1 article:
# article = articles[0]
# id_article = article.get_attribute('id') # display the id of the current article
# footer = article.find_element_by_xpath(".//footer")
# toolbar = footer.find_elements_by_xpath(".//div")
# classlink = toolbar[1].find_elements_by_xpath(".//a")
# ref = classlink[1].get_attribute('href') #Link to download 

# #obtain the name of the csv
# classN = article.find_element_by_class_name('ellipsis')
# name = classN.text
# # download the file
# r = requests.get(ref, allow_redirects=True)
# open(name, 'wb').write(r.content)