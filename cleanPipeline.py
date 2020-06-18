"""
Created on Mon Apr 27 17:52:41 2020

@author: ludiv
"""

''' A FAIRE
 '''
from selenium import webdriver
import pandas as pd
import requests
import os
import numpy  as np
import time
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from zipfile import ZipFile


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

def castingColumn(column):
    castData=[]
    for i in range(len(column)):
        string = column[i].replace(',','.')
        try:
            string_int = float(string)
            castData.append(string_int)
        except ValueError:
            # Handle the exception
            castData.append(np.nan)
    return castData

def extractDataFromSiteGeodes(siteweb,CHOOSE_CHROMEDRIVER):
    driver = webdriver.Chrome("./chromedriver_win32_{}/chromedriver".format(CHOOSE_CHROMEDRIVER))
    driver.get(siteweb)
    time.sleep(12)
    #France
    python_button = driver.find_element_by_xpath("//a[@id= 'tm_fiche']")
    python_button.click()
    time.sleep(7)
    france = driver.find_element_by_xpath("//button[@class= 'valref-button1 disabled w100']")
    if len(france.text.split())!=3:
        if france.text.split()[3]=="pour":
            franceValue = "".join(france.text.split()[2:3])
        else:
            franceValue = "".join(france.text.split()[2:4]) 
    else:
        franceValue=france.text.split()[2]
    #France
    python_button = driver.find_element_by_xpath("//a[@id= 'tm_table']")
    python_button.click()
    time.sleep(5)
    python_button = driver.find_element_by_xpath("//th[@class= 'dt-head-left sorting_asc']")
    python_button.click()
    table = driver.find_element_by_xpath("//tbody")
    rows = table.find_elements_by_xpath("//tr[@role= 'row']")
    text = [x.text for x in rows]
    code=["".join(text[i].split()[0]) for i in range(2,len(text))]#['00'] #50= N/A-divisionpar0 #2-102
    #castData=castingData(col))
    labels = []
    rowsA=[]
    weird = ['975','974','90']
    for i in range(2,len(text)):
        if "".join(text[i].split()[0]) not in weird:
            label = "".join(text[i].split()[1])
            row = "".join(text[i].split()[2:])
        elif "".join(text[i].split()[0]) =='975' or "".join(text[i].split()[0]) =='90':
            label = "".join(text[i].split()[1:4])
            row = "".join(text[i].split()[4:])
        elif "".join(text[i].split()[0]) =='974':
            label = "".join(text[i].split()[1:3])
            row = "".join(text[i].split()[3:])
        labels.append(label)
        rowsA.append(row)
    #France
    labels=["France"]+labels
    rowsA=[franceValue]+rowsA
    cols=['00']+code
    #France
    data = pd.DataFrame(columns = ['label','data'],index = cols)
    data.loc[:,'label'] = labels #
    data.loc[:,'data'] = rowsA #
    driver.close()
    return data

def FirstJan(year):
    #1. Take csv from  https://www.insee.fr/fr/statistiques/1893198 :Estimation de population par département, sexe et âge quinquennal - Années 1975 à 2020 (csv a telecharger)
    PATHData = './Data/Insee/demography.xls'
    # if os.path.exists(PATHData)==False:
    #     driver.get('https://www.insee.fr/fr/statistiques/1893198')
    #     ref = driver.find_element_by_xpath('//a[@href="/fr/statistiques/fichier/1893198/estim-pop-dep-sexe-aq-1975-2020.xls"]')
    #     r = requests.get(ref, stream=True,allow_redirects=True)
    #     open(PATHData, 'wb').write(r.content) 
    #2. open xls
    demo = pd.read_excel(io=PATHData, sheet_name=year) #we can choose the year here.
    #3. convert in dataframe
    demo = cleanDemo(demo) #all data of the population/sex/age on the 1rst of January of the chosen year
    demoP = demo.append(pd.Series(name='975'))
    demoP = demo.append(pd.Series(name='977'))
    demoP = demo.append(pd.Series(name='978'))
    demoP.loc['975','label']= 'Saint-Pierre et Miquelon'
    demoP.loc['977','label']= 'Saint-Barthélemy'
    demoP.loc['978','label']= 'Saint-Martin'

    #4. It will be the Base where we will add variation of other weeks for sexe, age and demog.
    ide=["00"]+[demoP.index[i] for i in range(len(demoP.index))]
    frframe=pd.DataFrame(index=["00"],
    columns=['label','population','Women_rate', 'NbMoins_15_ans', 'Nb15_65_ans', 'NbPlus_65_ans'])
    frframe.loc['00','label']='France'
    #FirstJan2020 = pd.concat([frframe,demo]) 
    FirstJan2020 = pd.DataFrame(index=demoP.index,
       columns=['label','population','Women_rate', 'NbMoins_15_ans', 'Nb15_65_ans', 'NbPlus_65_ans']) #Abstract of the informations on the 1rst of January of the chosen year
    FirstJan2020.loc[:,'label']=demoP.loc[:,'label']
    #5.population (number)
    FirstJan2020.loc[:,'population'] = demoP.loc[:,'Etotal']
    #6.sex (% women on the total of population)
    wom = demo.loc[:,'Ftotal']
    tot = demo.loc[:,'Etotal']
    FirstJan2020.loc[:,'Women_rate'] = 100*wom/tot
    #7.age TO MODIFY: change to have age moyen
    more = demo.loc[:,'E65_69'] +  demo.loc[:,'E70_74'] 
    + demo.loc[:,'E75_79'] +  demo.loc[:,'E80_84']
    + demo.loc[:,'E85_89'] +  demo.loc[:,'E90_94'] +  demo.loc[:,'E95_plus']
    # tot = demo.loc[:,'Etotal']
    # rate = 100*more/tot
    FirstJan2020.loc[:,'NbPlus_65_ans'] = more
    less = demo.loc[:,'E0_4'] +  demo.loc[:,'E5_9'] 
    + demo.loc[:,'E10_14'] 
    FirstJan2020.loc[:,'NbMoins_15_ans'] = less
    FirstJan2020.loc[:,'Nb15_65_ans'] = tot - less - more
    
    frframe1 = pd.concat([frframe,FirstJan2020]) 
    frframe1.iloc[0,1:]=np.sum(frframe1.iloc[1:,1:])
    frframe1.iloc[0,2]=np.mean(frframe1.iloc[1:,2])
    frframe1.index.name ='code'
    return frframe1, demoP

def createCSV(weeks, demo, colUnif,file,CHANGE):
    for week in weeks:
        #3. create a dataframe with departements as index 
        dataUnif = pd.DataFrame(index=demo.index,  columns=colUnif)
        dataUnif.loc[:,'label']=demo.loc[:,'label']
        
        ide=["00"]+[demo.index[i] for i in range(len(demo.index))]
        frframe=pd.DataFrame(index=["00"], columns=colUnif)
        frframe.loc['00','label']='France'
        dataUnif = pd.concat([frframe,dataUnif]) 
        #5. save as a csv with the name = [YEAR]_S[week].csv
        dataUnif.index.name ='code'

        if os.path.exists('./Data/Unify/{}/{}.csv'.format(file,week))==False or CHANGE==True:
            dataUnif.to_csv('./Data/Unify/{}/{}.csv'.format(file,week))

''' Recupére les colonnes avec extractDataFromSiteGeodes pour chaque patho, age et object et semaine'''
def obtainDataWeek(week,AlreadyDone,fail,base,CHOOSE_CHROMEDRIVER):
    # for week in weeks:
    # recuperer le dataframe pour chaque colonne avec extractDataFromSiteGeodes
    ages = ['_all','_moins15','_plus65','_15_65']
    objects = ['_sos','_urg','_hosp']#,'_']
    pathology = ['asthme','grippe','bronchite', 'pneumo']#'grippe'] # [
    for patho in pathology:
        for ob in objects:
            for age in ages:
                done = week + patho+age+ ob
                print('****',done)
                if done not in AlreadyDone:
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
                    
                    try:
                        data=extractDataFromSiteGeodes(siteweb,CHOOSE_CHROMEDRIVER) # output = dataframe 
                        name = patho + ob + age
                        #write on csv
                        csv = pd.read_csv('./Data/Unify/weeks/{}.csv'.format(week))
                        csv.index = csv.loc[:,'code']
                        csv = csv.drop(['code'], axis=1)
                        csv.loc[:,name]=castingColumn(data.loc[:,'data'])
                        #dataWeek[name] = data 
                        csv.to_csv('./Data/Unify/weeks/{}.csv'.format(week))
                        AlreadyDone = np.append(AlreadyDone,done)
                        np.save('./Data/AlreadyDone.npy',AlreadyDone)
                    
                        print('**csv saved ')
                    except :
                        print('**fail ',done)
                        fail = np.append(fail,done)
                        np.save('./Data/fail.npy',fail)

                        pass
                else:
                    print('** Already done ',done)
    return fail, AlreadyDone  

def deleteAll():
    zipObj = ZipFile('DataBackup{}.zip'.format(time.time()), 'w')   
    pathw = './Data/Unify/weeks/'
    pathc = './Data/Unify/covid/'
    for csv in os.listdir(pathw):
        zipObj.write(pathw+csv)
        os.remove(pathw+csv)
    for csv in os.listdir(pathc):
        zipObj.write(pathc+csv)
        os.remove(pathc+csv)
    if os.path.exists('./Data/Unify/fail.npy'):
        zipObj.write('./Data/Unify/fail.npy')
        os.remove('./Data/Unify/fail.npy')
    if os.path.exists('./Data/Unify/AlreadyDone.npy'):
        zipObj.write('./Data/Unify/AlreadyDone.npy')
        os.remove('./Data/Unify/AlreadyDone.npy')
    # close the Zip File
    zipObj.close()

#Fast debugger
#base="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
#week="2020-S17"
#AlreadyDone = []
#fail = []
#obtainDataWeek(week,AlreadyDone,fail,base,CHOOSE_CHROMEDRIVER)

def obtainDataWeekCovid(week,AlreadyDone,fail,base,CHOOSE_CHROMEDRIVER):
    # for week in weeks:
    # recuperer le dataframe pour chaque colonne avec extractDataFromSiteGeodes
    ages = ['_all','_moins15','_plus75','_15_44','_45_64','_65_74']
    objects = ['_sos','_urg','_hosp','_villeNbTest','_villeTauxPos','_villeNbPos','_nouvRea']

    #write on csv
    for ob in objects:
        if ob != '_nouvRea':
            for age in ages:
                done = week + 'covid'+age+ ob
                print('****',done)
                if done not in AlreadyDone:
                    csv = pd.read_csv('./Data/Unify/covid/{}.csv'.format(week))
                    csv.index = csv.loc[:,'code']
                    csv = csv.drop(['code'], axis=1)
                    ''' To complet here''' 
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
                    ####En cours: récupérer les deux ages et regrouper ou alors recup tous les ages
                    try:
                        data=extractDataFromSiteGeodes(siteweb,CHOOSE_CHROMEDRIVER) # output = dataframe 
                        name = 'covid' + ob + age
                        csv.loc[:,name]=castingColumn(data.loc[:,'data'])
                        #dataWeek[name] = data 
                        csv.to_csv('./Data/Unify/covid/{}.csv'.format(week))
                        AlreadyDone= np.append(AlreadyDone,done)
                        np.save('./Data/AlreadyDone.npy',AlreadyDone)
                        
                        print('**csv saved ')
                    except :
                        print('**fail ',done)
                        fail = np.append(fail,done)
                        np.save('./Data/fail.npy',fail)
                        pass
    
            else:
                print('** Already done ',done)
        else:
            done = week + 'covid'+ ob
            print('****',done)
            if done not in AlreadyDone:
                csv = pd.read_csv('./Data/Unify/covid/{}.csv'.format(week))
                csv.index = csv.loc[:,'code']
                csv = csv.drop(['code'], axis=1)
                ''' To complet here''' 
                ####En cours: récupérer les deux ages et regrouper ou alors recup tous les ages
                try:
                    weeks_corr = pd.read_excel(io='./week_correspond.xlsx', sheet_name='Feuil1') #we can choose the year here.
                    weeks_corr.index = weeks_corr.loc[:,'semaine']
                    days = ['j1','j2','j3','j4','j5','j6','j7']
                    for j in days:
                        print(j)
                        day =  weeks_corr.loc[str(week),j]
                        sursaud_type = 'covid_hospit_incid.incid_rea'
                        siteweb=base[:-80]+  base[-77:-74] + sursaud_type  +base[-40:-37]+str(day)+base[-29:]
                        data=extractDataFromSiteGeodes(siteweb,CHOOSE_CHROMEDRIVER) # output = dataframe 
                        if j=='j1':
                            datasomme = data
                        else:
                            for i in datasomme.index :
                                if datasomme.loc[i,'data'] != 'N/A-résultatnondisponible' and data.loc[i,'data'] != 'N/A-résultatnondisponible':
                                    datasomme.loc[i,'data']= int(datasomme.loc[i,'data']) + int(data.loc[i,'data'])
                                else:
                                    datasomme.loc[i,'data']= 'N/A-résultatnondisponible'
                    name = 'covid' + ob 
                    csv.loc[:,name]=castingColumn(data.loc[:,'data'])
                    #dataWeek[name] = data 
                    csv.to_csv('./Data/Unify/covid/{}.csv'.format(week))
                    AlreadyDone= np.append(AlreadyDone,done)
                    np.save('./Data/AlreadyDone.npy',AlreadyDone)
                    
                    print('**csv saved ')
                except :
                    print('**fail ',done)
                    fail = np.append(fail,done)
                    np.save('./Data/fail.npy',fail)
                    pass
                    
            else:
                print('** Already done ',done)
    return fail, AlreadyDone            
    #return dataWeek

def SaveXlsx(file,weeks,filecsv): #save data in a xlsx with one sheet per week
    filename = './Data/Unify/{}.xlsx'.format(file)
    # Create new workbook
    wb = Workbook()
    wb.save(filename)
    # Remove existing sheet
    ref = wb['Sheet']
    wb.remove(ref)
    # Load existing workbook
    wb = load_workbook(filename)
    i=0
    for week in weeks:
        sheet1 = wb.create_sheet(week,i)
        i= i+1
        active = wb[week]
        csv = pd.read_csv('./Data/Unify/{}/{}.csv'.format(filecsv,week))
        csv.index = csv.loc[:,'code']
        csv = csv.drop(['code'], axis=1)
        # Write dataframe to active worksheet
        for x in dataframe_to_rows(csv):
            active.append(x)
    # Save workbook to write
    wb.save(filename)

if __name__ == "__main__":
    CHOOSE_CHROMEDRIVER='83'
    # TO DO: code to find the last weeks availables
    CHANGE = False #put CHANGE to True if there were changes in the columns or indexes of the csv

    if CHANGE== True:
        deleteAll() #save all weeks csv, AlreadyDone.npy, and fail.npy in a DataBackup.zip and delete them.
        
    if os.path.exists('./Data/AlreadyDone.npy'):
        AlreadyDone = np.load('./Data/AlreadyDone.npy')
    else:
        AlreadyDone = []
    if os.path.exists('./Data/fail.npy'):
        fail = np.load('./Data/fail.npy')
    else:
        fail = []
    base="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
    print('***First January 2020************')
    FirstJan2020, demo = FirstJan('2020')
    FirstJan2020.to_csv('./Data/Unify/FirstJan2020.csv')
    FirstJan2019, demo = FirstJan('2019')
    FirstJan2019.to_csv('./Data/Unify/FirstJan2019.csv')
    #1. choose the weeks to handle
    print('*** pathology extraction ************')

    # weeksPatho=[str(2019)+'-S0'+str(i) for i in range(1,2)]
    
    weeksPatho=[str(2019)+'-S'+str(i) for i in range(1,52)]+[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,22)]
    weeksPatho=[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,20)]


    #2. choose the columns

    colUnifPatho = ['label',
    'asthme_sos_moins15','asthme_sos_15_65','asthme_sos_plus65','asthme_sos_all',
    'asthme_urg_moins15', 'asthme_urg_15_65', 'asthme_urg_plus65', 'asthme_urg_all',
    'asthme_hosp_moins15','asthme_hosp_15_65','asthme_hosp_plus65','asthme_hosp_all',

    'bronchite_sos_moins15','bronchite_sos_15_65','bronchite_sos_plus65','bronchite_sos_all',
    'bronchite_urg_moins15', 'bronchite_urg_15_65', 'bronchite_urg_plus65', 'bronchite_urg_all',
    'bronchite_hosp_moins15','bronchite_hosp_15_65','bronchite_hosp_plus65','bronchite_hosp_all',

    'grippe_sos_moins15','grippe_sos_15_65','grippe_sos_plus65','grippe_sos_all',
    'grippe_urg_moins15', 'grippe_urg_15_65', 'grippe_urg_plus65', 'grippe_urg_all',
    'grippe_hosp_moins15','grippe_hosp_15_65','grippe_hosp_plus65','grippe_hosp_all',

    'pneumo_sos_moins15','pneumo_sos_15_65','pneumo_sos_plus65','pneumo_sos_all',
    'pneumo_urg_moins15', 'pneumo_urg_15_65', 'pneumo_urg_plus65', 'pneumo_urg_all',
    'pneumo_hosp_moins15','pneumo_hosp_15_65','pneumo_hosp_plus65','pneumo_hosp_all']
    createCSV(weeksPatho, demo, colUnifPatho, 'weeks',CHANGE)
    
    for week in weeksPatho:
        fail, AlreadyDone =obtainDataWeek(week,AlreadyDone,fail,base,CHOOSE_CHROMEDRIVER)

    SaveXlsx('PathologyData',weeksPatho,'weeks') #save in a excel file

    print('*** covid extraction ************')
    colUnifCovid = ['label', 'covid_nouvRea',
    'covid_sos_moins15','covid_sos_15_44','covid_sos_45_64','covid_sos_65_74','covid_sos_plus75','covid_sos_all',
    'covid_urg_moins15','covid_urg_15_44','covid_urg_45_64','covid_urg_65_74','covid_urg_plus75','covid_urg_all',
    'covid_hosp_moins15','covid_hosp_15_44','covid_hosp_45_64','covid_hosp_65_74','covid_hosp_plus75','covid_hosp_all',
    'covid_villeNbTest_moins15','covid_villeNbTest_15_44','covid_villeNbTest_45_64','covid_villeNbTest_65_74','covid_villeNbTest_plus75','covid_villeNbTest_all',
    'covid_villeTauxPos_moins15','covid_villeTauxPos_15_44','covid_villeTauxPos_45_64','covid_villeTauxPos_65_74','covid_villeTauxPos_plus75','covid_villeTauxPos_all',
    'covid_villeNbPos_moins15','covid_villeNbPos_15_44','covid_villeNbPos_45_64','covid_villeNbPos_65_74','covid_villeNbPos_plus75','covid_villeNbPos_all']
    weeksCovid=[str(2020)+'-S'+str(i) for i in range(10,23)]
    createCSV(weeksCovid, demo, colUnifCovid, 'covid',CHANGE)

    for week in weeksCovid:
        fail, AlreadyDone = obtainDataWeekCovid(week,AlreadyDone,fail,base,CHOOSE_CHROMEDRIVER)

    SaveXlsx('CovidData',weeksCovid,'covid')

