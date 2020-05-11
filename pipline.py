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
import time
#import ezodf #conda install -c conda-forge ezodf 
driver = webdriver.Chrome("./chromedriver_win32/chromedriver")

CHANGE = False #put CHANGE to True if there were changes in the columns or indexes of the csv
# after replace CHANGE by a method that check differences


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

#7.age TO MODIFY: change to have age moyen
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

### https://www.insee.fr/fr/information/4470857#tableau-figure_evol
### Fichier de décès quotidiennes: 1 Marzo-mayo, 2018-2020
### Source : Insee, état civil

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
weeks=[str(2019)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,55)]+[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,19)]
print(weeks)

#2. choose the columns
colUnif = ['label','sex', 'mean_age',
'covid_sos_moins15','covid_sos_15_65','covid_sos_plus65','covid_sos_all',
'covid_urg_moins15','covid_urg_15_65','covid_urg_plus65','covid_urg_all',
'covid_hosp_moins15','covid_hosp_15_65','covid_hosp_plus65','covid_hosp_all',
'covid_villeTest_moins15','covid_villeTest_15_65','covid_villeTest_plus65','covid_villeTest_all',
'covid_villePos_moins15','covid_villePos_15_65','covid_villePos_plus65','covid_villePos_all',


'asthme_sos_moins15','asthme_sos_15_65','asthme_sos_plus65','asthme_sos_all',
'asthme_urg_moins15', 'asthme_urg_15_65', 'asthme_urg_plus65', 'asthme_urg_all',
'asthme_hosp_moins15','asthme_hosp_15_65','asthme_hosp_plus65','asthme_hosp_all',


'bronchite_sos_moins15','bronchite_sos_15_65','bronchite_sos_plus65','bronchite_sos_all',
'bronchite_urg_moins15', 'bronchite_urg_15_65', 'bronchite_urg_plus65', 'bronchite_urg_all',
'bronchite_hosp_moins15','bronchite_hosp_15_65','bronchite_hosp_plus65','bronchite_hosp_all',

'grippe_sos_moins15','grippe_sos_15_65','grippe_sos_plus65','grippe_sos_all',
'grippe_urg_moins15', 'grippe_urg_15_65', 'grippe_urg_plus65', 'grippe_urg_all',
'grippe_hosp_moins15','grippe_hosp_15_65','grippe_hosp_plus65','grippe_hosp_all',


'pneumopathie_sos_moins15','pneumopathie_sos_15_65','pneumopathie_sos_plus65','pneumopathie_sos_all',
'pneumopathie_urg_moins15', 'pneumopathie_urg_15_65', 'pneumopathie_urg_plus65', 'pneumopathie_urg_all',
'pneumopathie_hosp_moins15','pneumopathie_hosp_15_65','pneumopathie_hosp_plus65','pneumopathie_hosp_all'

]
for week in weeks:
    #3. create a dataframe with departements as index 
    dataUnif = pd.DataFrame(index=demo.index,
        columns=colUnif)
    dataUnif.loc[:,'label']=demo.loc[:,'label']

    #4. add each columns 
    #age, sexe, popu


    #5. save as a csv with the name = [YEAR]_S[week].csv
    if os.path.exists('./Data/Unify/weeks/{}.csv'.format(week))==False or CHANGE==True:
        dataUnif.to_csv('./Data/Unify/weeks/{}.csv'.format(week))

#6. create a xcel with each leaf = one csv
#7.think about how to do the update automatically
#df = pd.read_csv(fileToWrite)






''' *****************************************'''
''' ************* DataGouv ******************'''
''' *****************************************'''
# def DataGouvExtraction(siteweb,site, detail):
#     driver = webdriver.Chrome("./chromedriver_win32/chromedriver")
#     driver.get(siteweb)
#     #resources-list
#     resourceClass = driver.find_element_by_xpath("//div[@class='resources-list']")
#     #just display the text in this resources_list to try
#     # h4 = resourceClass.find_element_by_xpath(".//h4[@class='resource-type']")
#     # h4.text
#     # #card with the files inside. It should be  for loop with @class = instead of id= but for the moment class doesn't work
#     articles = resourceClass.find_elements_by_xpath(".//article")
#     #Now for all articles that e want on the page
#     dossier = 'Data/'+ site+'/'+ detail
#     os.makedirs(dossier, exist_ok=True) 
#     for i in range(len(articles)):
#         article = articles[i]
#         #obtain the name of the csv
#         classN = article.find_element_by_class_name('ellipsis')
#         name = classN.text
#         PATHData = dossier + '/' + name
#         if os.path.exists(PATHData)==False:      
#             #obtain the href
#             id_article = article.get_attribute('id') # display the id of the current article
#             footer = article.find_element_by_xpath(".//footer")
#             toolbar = footer.find_elements_by_xpath(".//div")
#             classlink = toolbar[1].find_elements_by_xpath(".//a")
#             ref = classlink[1].get_attribute('href') #Link to download 
#             # download the file
#             r = requests.get(ref, allow_redirects=True)
#             open(PATHData, 'wb').write(r.content)
# site = 'DataGouv'
#     #driver.get('https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/')
# siteweb ='https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/'
# detail = 'DataGouv_donnes_hospitalieres_covid'
# DataGouvExtraction(siteweb,site, detail)

# siteweb = 'https://www.data.gouv.fr/fr/datasets/donnees-des-urgences-hospitalieres-et-de-sos-medecins-relatives-a-lepidemie-de-covid-19/'
# detail = 'DataGouv_donnes_urgences_et_sos_medecin_covid'
# DataGouvExtraction(siteweb,site, detail)



''' *****************************************'''
''' *********** Geodes **********************'''
''' *****************************************'''

print('EXTRACT FROM GEODES')
driver.get('https://geodes.santepubliquefrance.fr/#c=indicator&i=covid_hospit_incid.incid_rea&s=2020-04-28&selcodgeo=02&t=a01')
site = 'Geodes'

def extractDataFromSiteGeodes(siteweb):
    driver.get(siteweb)
    time.sleep(30)
    python_button = driver.find_element_by_xpath("//a[@id= 'tm_table']")
    python_button.click()
    time.sleep(5)
    python_button = driver.find_element_by_xpath("//th[@class= 'dt-head-left sorting_asc']")
    python_button.click()
    table = driver.find_element_by_xpath("//tbody")
    rows = table.find_elements_by_xpath("//tr[@role= 'row']")
    text = [x.text for x in rows]
    col=["".join(text[i].split()[0]) for i in range(2,103)]#50= N/A-divisionpar0 #2-102
    labels = []
    rows=[]
    for i in range(2,103):
        if i != 101 and i != 92:
            label = "".join(text[i].split()[1])
            row = "".join(text[i].split()[2:])
        elif i == 92:
            label = "".join(text[i].split()[1:4])
            row = "".join(text[i].split()[4:])
        elif i == 101:
            label = "".join(text[i].split()[1:3])
            row = "".join(text[i].split()[3:])
        labels.append(label)
        rows.append(row)
    data = pd.DataFrame(columns = ['label','data'],index = col)
    data.loc[:,'label'] = labels
    data.loc[:,'data'] = rows
    return data


# Test function: It works!
# siteweb='https://geodes.santepubliquefrance.fr/#c=indicator&i=covid_hospit_incid.incid_rea&s=2020-04-28&selcodgeo=02&t=a01'
# data=extractDataFromSiteGeodes(siteweb)
# print(data)


''' Recupére les colonnes avec extractDataFromSiteGeodes pour chaque patho, age et object et semaine'''

driver = webdriver.Chrome("./chromedriver_win32/chromedriver")
base="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"

weeks=['2020-S15']

for week in weeks:
    # recupérer le csv de la semaine
    csv = pd.read_csv('./Data/Unify/weeks/{}.csv'.format(week))
    # recuperer le dataframe pour chaque colonne avec extractDataFromSiteGeodes
    ages = ['_all']
    objects = ['_sos']
    pathology = ['asthme']
    # ages = ['_all','_moins15','_plus65','_15_65']
    # objects = ['_sos','_','_urg','_hosp']
    # pathology = ['asthme','grippe','bronchite', 'pneumopathie', 'covid']
    for patho in pathology:
        for ob in objects:
            for age in ages:
                ''' To complet here''' 
                if ob == '_sos':
                    sursaud_type = '_sos.'
                    medicalType = '_sos'
                elif ob == '_urg':
                    sursaud_type = '_sau.'
                    medicalType = '_pass_sau'
                elif ob == '_hosp':
                    sursaud_type = '_sau.'
                    medicalType= '_hospit_sau' 
                sickAndtype = "prop_"+ patho + medicalType
                #print('****',week, patho,ob,age)
                if age == '_all':
                    ageCODE = '0'
                elif age == '_moins15':
                    ageCODE = 'A'
                elif age == '_15_65':
                    ageCODE = 'B'
                elif age == '_plus65':
                    ageCODE = 'C'
                
                siteweb=base[:-78]+ ageCODE + base[-77:-67] + sursaud_type + sickAndtype +base[-40:-37]+str(week)+base[-29:]
                print(siteweb)
                columnP=extractDataFromSiteGeodes(siteweb) # output = dataframe 
                print(columnP)
                name = patho + ob + age
                csv.loc[:,name]=columnP.loc[:,'data'] # pb: n'enregistre pas dans le dataframe, a voir
    csv.to_csv('./Data/Unify/weeks/{}.csv'.format(week))
    print("termina")



##### EROR: aléatoire: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//th[@class= 'dt-head-left sorting_asc']"}
##### Expand sleep time to 20 seconds... geodes page is slow






# Two data at same time
# c=indicator&f2=C&i=covid_hospit_incid.incid_hosp&i2=sursaud_sau.prop_bronchite_hospit_sau&s=2020-05-10&s2=2020-S18&selcodgeo=50&t=a01&t2=a01

#JUST EXAMPLES FROM internet here
# aaa = resourceClass.find_element_by_css_selector('.card.resource-card a').get_attribute('href')
# get_div = resourceClass.find_elements_by_tag_name('a',href=True)