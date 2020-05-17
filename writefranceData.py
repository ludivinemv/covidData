from selenium import webdriver
import pandas as pd
import requests
import os
import numpy  as np
import time
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def extractFranceData(siteweb):
    driver = webdriver.Chrome("./chromedriver_win32/chromedriver")
    driver.get(siteweb)
    time.sleep(30)
    python_button = driver.find_element_by_xpath("//a[@id= 'tm_fiche']")
    python_button.click()
    time.sleep(10)
    python_button = driver.find_element_by_xpath("//a[@class= 'grille no-print']")
    python_button.click()
    time.sleep(2)
    python_button = driver.find_element_by_xpath("//li[@class= 'menu-selected']")
    python_button.click()
    time.sleep(2)
    table = driver.find_element_by_xpath("//tbody")
    rows = table.find_elements_by_xpath("//tr")#[@role= 'row']
    text = [x.text for x in rows if (x.text.startswith('2019') or x.text.startswith('2020'))]
    values=["".join(text[i].split()[2:3]) for i in range(0,71)]#['00'] #50= N/A-divisionpar0 #2-102
    driver.close()
    return values


def fillCSVs(values,name, weeks):
    for (week, value) in zip(weeks, values):
        csv = pd.read_csv('./Data/Unify/weeks/{}.csv'.format(week))
        csv.loc[101,name]=value
        csv.index = csv.loc[:,'code']
        csv = csv.drop(['code'], axis=1)
        csv.to_csv('./Data/Unify/weeks/{}.csv'.format(week))


def addLineFrance(week):
    csv = pd.read_csv('./Data/Unify/weeks/{}.csv'.format(week))
    csv.loc[101] = ['00']+['France'] + [np.NaN]*(len(list(csv.columns))-2)
    csv.index = csv.loc[:,'code']
    csv = csv.drop(['code'], axis=1)
    csv.to_csv('./Data/Unify/weeks/{}.csv'.format(week))

def createAdressesSitesWeb(week):
    listAdresses=[]
    listNames=[]
    ages = ['_all','_moins15','_plus65','_15_65']
    objects = ['_sos','_urg','_hosp']#,'_']
    pathology = ['asthme','bronchite', 'pneumo', 'grippe'] # [
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
                elif ob == '_hosp' and patho == 'grippe':
                    sursaud_type = '_sau.'
                    medicalType= '_hospi_sau' 
                sickAndtype = "prop_"+ patho + medicalType
                # print('****',week, patho,ob,age)
                if age == '_all':
                    ageCODE = '0'
                elif age == '_moins15':
                    ageCODE = 'A'
                elif age == '_15_65':
                    ageCODE = 'B'
                elif age == '_plus65':
                    ageCODE = 'C'
                
                siteweb=base[:-78]+ ageCODE + base[-77:-67] + sursaud_type + sickAndtype +base[-40:-37]+str(week)+base[-29:]
                name = patho + ob + age
                listAdresses.append(siteweb)
                listNames.append(name)
    return listAdresses,listNames
                    #print(siteweb)


def createAdressesSitesWebCovid(week):
    listAdresses=[]
    listNames=[]
    ages = ['_all','_moins15','_plus75','_15_44','_45_64','_65_74']
    objects = ['_sos','_urg','_hosp','_villeNbTest','_villeTauxPos','_villeNbPos']
    for ob in objects:
        for age in ages:
            if ob == '_sos':
                sursaud_type = 'sursaud_corona_hebdo.prop_corona_sos'
            elif ob == '_urg':
                sursaud_type = 'sursaud_corona_hebdo.prop_corona_pass_sau'
            elif ob == '_hosp':
                sursaud_type = 'sursaud_corona_hebdo.prop_corona_hospit_sau'
            elif ob == '_villeTauxPos':
                sursaud_type = 'covid_troislabo_heb.tx_pos'
            elif ob == '_villeNbTest':
                sursaud_type = 'covid_troislabo_heb.nb_test'
            elif ob == '_villeNbPos':
                sursaud_type = 'covid_troislabo_heb.nb_pos'

            if age == '_all':
                ageCODE = '0'
            elif age == '_moins15':
                ageCODE = 'A'
            elif age == '_15_44':
                ageCODE = 'B'
            elif age == '_45_64':
                ageCODE = 'C'
            elif age == '_65_74':
                ageCODE = 'D'
            elif age == '_plus75':
                ageCODE = 'E'
            siteweb=base[:-78]+ ageCODE + base[-77:-74] + sursaud_type  +base[-40:-37]+str(week)+base[-29:]
            name = 'covid' + ob + age
            listAdresses.append(siteweb)
            listNames.append(name)
    return listAdresses,listNames


def writeFrance(listAdresses, listNames, weeks):
    falla=[]
    for adress, name in zip(listAdresses, listNames):
        try:
            value=extractFranceData(siteweb) # output = dataframe 
            values2=values[-18:]
            print(name)
            fillCSVs(values2,name,weeks)
            print('**CSVs saved ')
        except :
            print('**fail ',name)
            falla = np.append(name)
            np.save('./Data/falla.npy',falla)
            pass
    return falla 



#[str(2019)+'-S0'+str(i) for i in range(1,10)]+[str(2019)+'-S'+str(i) for i in range(10,55)]+
weeks=[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,19)]

## ADD FRANCE LINE
for week in weeks:
    addLineFrance(week)

##Write columns france
week='2020-S18'
base="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
listAdresses,listNames=createAdressesSitesWeb(week)
listAdressesCovid,listNamesCovid=createAdressesSitesWebCovid(week)
print(len(listAdressesCovid)) #48 AND 36

writeFrance(listAdresses, listNames, weeks)
