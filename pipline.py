# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:52:41 2020

@author: ludiv



TO DO:
1. requirement
2. README
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
#import ezodf #conda install -c conda-forge ezodf 
driver = webdriver.Chrome("./chromedriver_win32/chromedriver")


''' *****************************************'''
''' ************* DataGouv ******************'''
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

    #driver.get('https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/')
siteweb ='https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/'
detail = 'DataGouv_donnes_hospitalieres_covid'
DataGouvExtraction(siteweb,site, detail)

siteweb = 'https://www.data.gouv.fr/fr/datasets/donnees-des-urgences-hospitalieres-et-de-sos-medecins-relatives-a-lepidemie-de-covid-19/'
detail = 'DataGouv_donnes_urgences_et_sos_medecin_covid'
DataGouvExtraction(siteweb,site, detail)



''' *****************************************'''
''' *********** Geodes **********************'''
''' *****************************************'''
import time
# driver.get('https://geodes.santepubliquefrance.fr/#c=indicator&i=covid_hospit_incid.incid_rea&s=2020-04-28&selcodgeo=02&t=a01')
site = 'Geodes'


def extractDataFromSiteGeodes(site):
    driver.get(siteweb)
    time.sleep(10)
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

#For all sickness and weeks'
medicalType=["_sos", "_pass_sau", "_hospit_sau"]
#BRONCHITE, GRIPPE et  PNEUMOPATHIE
#COVID : nombre de test virologique effectués en ville et nombre de test positifs ?
sickness=[ "asthme", "bronchite", "grippe","pneumopathie"]
sickAndtypes = ["prop_"+ i+ j for i in sickness for j in medicalType]
print(sickAndtypes)
weeks=[str(2019)+'-S0'+str(i) for i in range(1,10)]+[str(2019)+'-S'+str(i) for i in range(10,55)]+[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,19)]
print(weeks)
#tous ages confondus, - de 15 ans, entre 15 et 65, plus de 65
#?????????
base="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
sitesweb=[base[:-62]+sickAndtype+base[-40:-37]+str(week)+base[-29:] for sickAndtype in sickAndtypes for week in weeks]
print(sitesweb)

#just for test rewrite sitesWeb with just one site
sitesweb=["https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"]
#For extract column from all sites and add to csv 
column=extractDataFromSiteGeodes(siteweb)
#write on CSV with ludi code!!!





''' *****************************************'''
''' ************* Get informations ********'''
''' *****************************************'''
#On a l'age par tranche de 5 ans et sexe au 1er janvier 2020 (et 2019):
# https://www.insee.fr/fr/statistiques/1893198 :Estimation de population par département, sexe et âge quinquennal - Années 1975 à 2020 (csv a telecharger)
#--> on peut donc avoir le sexe, age, population

''' ************** FirstJan2020 *******************'''
#1. Take csv from  https://www.insee.fr/fr/statistiques/1893198 :Estimation de population par département, sexe et âge quinquennal - Années 1975 à 2020 (csv a telecharger)
#### trop long donc je l'ai mis a la main
PATHData = './Data/Insee/demography.xls'
# if os.path.exists(PATHData)==False:
#     driver.get('https://www.insee.fr/fr/statistiques/1893198')
#     ref = driver.find_element_by_xpath('//a[@href="/fr/statistiques/fichier/1893198/estim-pop-dep-sexe-aq-1975-2020.xls"]')
#     r = requests.get(ref, stream=True,allow_redirects=True)
#     open(PATHData, 'wb').write(r.content) 

#2. open xls
demo = pd.read_excel(io=PATHData, sheet_name='2020') #we can choose the year here.

#3. convert in dataframe
def cleanDemo(df):
    age = []
    for i in range(21):
        aa=df.iloc[3,i+2]
        if i==0 or i==1:
            age.append('{}_{}'.format(aa[0],aa[4]))
        elif i==19:
            age.append('{}{}_{}'.format(aa[0],aa[1],'plus'))
        elif i == 20:
            age.append('total')
        else:
            age.append('{}{}_{}{}'.format(aa[0],aa[1],aa[5],aa[6]))

    col = ['code','label']
    for i in range(21):    
        col.append('E'+age[i])
    for i in range(21):    
        col.append('H'+age[i])
    for i in range(21):    
        col.append('F'+age[i])
    df.columns = col
    df = df.iloc[4:,:]
    df  = df.drop([100,106,107,108,109])
    df.index = df.loc[:,'code']
    df = df.drop(['code'],axis=1)
    return df
demo = cleanDemo(demo) #all data of the population/sex/age on the 1rst of January of the chosen year

#4. It will be the Base where we will add variation of other weeks for sexe, age and demog.
FirstJan2020 = pd.DataFrame(index=demo.index,
    columns=['label','population','sex', 'age']) #Abstract of the informations on the 1rst of January of the chosen year
FirstJan2020.loc[:,'label']=demo.loc[:,'label']

#5.population (number)
FirstJan2020.loc[:,'population'] = demo.loc[:,'Etotal']

#6.sex (% women on the total of population)
wom = demo.loc[:,'Ftotal']
tot = demo.loc[:,'Etotal']
rate = 100*wom/tot
FirstJan2020.loc[:,'sex'] = rate

#7.age (depend of what we want, for exemple if we want the rate of more than 65 years)
more = demo.loc[:,'E65_69'] +  demo.loc[:,'E70_74'] 
+ demo.loc[:,'E75_79'] +  demo.loc[:,'E80_84']
+ demo.loc[:,'E85_89'] +  demo.loc[:,'E90_94'] +  demo.loc[:,'E95_plus']
tot = demo.loc[:,'Etotal']
rate = 100*more/tot
FirstJan2020.loc[:,'age'] = rate

''' ************** Population *******************'''
#1. find population's evolution per weeks (or days and sum or death and birth) per departements
#2.calculs to have to population of the weeks
#3. create a dataframe with as index the code and as columns the weeks


''' ************** sex *******************'''
#1. find sex's evolution per weeks (or days and sum or death and birth) per departements
#2.calculs to have to population of the weeks
#3. create a dataframe with as index the code and as columns the weeks


''' ************** age *******************'''
#1. find age's evolution per weeks (or days and sum or death and birth) per departements
#2.calculs to have to population of the weeks
#3. create a dataframe with as index the code and as columns the weeks

''' *****************************************'''
''' *** Create a unify csv for each week ****'''
''' *****************************************'''
#1. choose the weeks to handle
weeks =['2020_S{}'.format(i) for i in range(1,17)]

2. #choose the columns
colUnif = ['label','sex', 'age','covid_sos','covid_urg','covid_hosp','asthme_sos',	'asthme_urg','asthme_hosp']
for week in weeks:
    #3. create a dataframe with departements as index 
    dataUnif = pd.DataFrame(index=demo.index,
        columns=colUnif)
    dataUnif.loc[:,'label']=demo.loc[:,'label']

    #4. add each columns


    #5. save as a csv with the name = [YEAR]_S[week].csv
    dataUnif.to_csv('./Data/Unify/weeks/{}.csv'.format(week))

#6. create a xcel with each leaf = one csv
#7.think about how to do the update automatically

df = pd.read_csv(fileToWrite)
dataframe=

dataUnif.loc[:,'label']=demo.loc[:,'label']
















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