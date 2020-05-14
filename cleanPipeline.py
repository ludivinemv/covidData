from selenium import webdriver
import pandas as pd
import requests
import os
import numpy  as np
import time
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows


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
        string = column[i]
        try:
            string_int = float(string)
            castData.append(string_int)
        except ValueError:
            # Handle the exception
            castData.append(-100)
    return castData

def extractDataFromSiteGeodes(siteweb):
    driver = webdriver.Chrome("./chromedriver_win32/chromedriver")
    driver.get(siteweb)
    time.sleep(30)
    python_button = driver.find_element_by_xpath("//a[@id= 'tm_table']")
    python_button.click()
    time.sleep(10)
    python_button = driver.find_element_by_xpath("//th[@class= 'dt-head-left sorting_asc']")
    python_button.click()
    table = driver.find_element_by_xpath("//tbody")
    rows = table.find_elements_by_xpath("//tr[@role= 'row']")
    text = [x.text for x in rows]
    col=["".join(text[i].split()[0]) for i in range(2,103)]#50= N/A-divisionpar0 #2-102
    #castData=castingData(col))
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
    driver.close()
    return data

def FirstJan():
    #1. Take csv from  https://www.insee.fr/fr/statistiques/1893198 :Estimation de population par département, sexe et âge quinquennal - Années 1975 à 2020 (csv a telecharger)
    PATHData = './Data/Insee/demography.xls'
    # if os.path.exists(PATHData)==False:
    #     driver.get('https://www.insee.fr/fr/statistiques/1893198')
    #     ref = driver.find_element_by_xpath('//a[@href="/fr/statistiques/fichier/1893198/estim-pop-dep-sexe-aq-1975-2020.xls"]')
    #     r = requests.get(ref, stream=True,allow_redirects=True)
    #     open(PATHData, 'wb').write(r.content) 
    #2. open xls
    demo = pd.read_excel(io=PATHData, sheet_name='2020') #we can choose the year here.
    #3. convert in dataframe
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
    FirstJan2020.loc[:,'sex'] = 100*wom/tot
    #7.age TO MODIFY: change to have age moyen
    more = demo.loc[:,'E65_69'] +  demo.loc[:,'E70_74'] 
    + demo.loc[:,'E75_79'] +  demo.loc[:,'E80_84']
    + demo.loc[:,'E85_89'] +  demo.loc[:,'E90_94'] +  demo.loc[:,'E95_plus']
    tot = demo.loc[:,'Etotal']
    rate = 100*more/tot
    FirstJan2020.loc[:,'age'] = rate
    return FirstJan2020, demo

def createCSV(weeks, demo, colUnif,file):
    for week in weeks:
        #3. create a dataframe with departements as index 
        dataUnif = pd.DataFrame(index=demo.index,  columns=colUnif)
        dataUnif.loc[:,'label']=demo.loc[:,'label']
        #5. save as a csv with the name = [YEAR]_S[week].csv
        if os.path.exists('./Data/Unify/{}/{}.csv'.format(file,week))==False or CHANGE==True:
            dataUnif.to_csv('./Data/Unify/{}/{}.csv'.format(file,week))

''' Recupére les colonnes avec extractDataFromSiteGeodes pour chaque patho, age et object et semaine'''
def obtainDataWeek(week,AlreadyDone,fail):
    # for week in weeks:
    # recuperer le dataframe pour chaque colonne avec extractDataFromSiteGeodes
    ages = ['_all','_moins15','_plus65','_15_65']
    objects = ['_sos','_urg','_hosp']#,'_']
    pathology = ['asthme','grippe','bronchite', 'pneumo']
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
                    print('****',week, patho,ob,age)
                    if age == '_all':
                        ageCODE = '0'
                    elif age == '_moins15':
                        ageCODE = 'A'
                    elif age == '_15_65':
                        ageCODE = 'B'
                    elif age == '_plus65':
                        ageCODE = 'C'
                    
                    siteweb=base[:-78]+ ageCODE + base[-77:-67] + sursaud_type + sickAndtype +base[-40:-37]+str(week)+base[-29:]
                    #print(siteweb)
                    try:
                        data=extractDataFromSiteGeodes(siteweb) # output = dataframe 
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
    #return dataWeek

def obtainDataWeekCovid(week,AlreadyDone,fail):
    # for week in weeks:
    # recuperer le dataframe pour chaque colonne avec extractDataFromSiteGeodes
    ages = ['_all','_moins15','_plus75','_15_44','_45_64','_65_74']
    objects = ['_sos','_urg','_hosp','_villeNbTest','_villeTauxPos','_villeNbPos']
    ages = ['_plus75']
    objects = ['_urg']

    #write on csv
    for ob in objects:
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
                    data=extractDataFromSiteGeodes(siteweb) # output = dataframe 
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
    return fail, AlreadyDone            
    #return dataWeek

def SaveXlsx(file,weeks,filecsv):
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
    if os.path.exists('./Data/AlreadyDone.npy'):
        AlreadyDone = np.load('./Data/AlreadyDone.npy')
    else:
        AlreadyDone = []
    if os.path.exists('./Data/fail.npy'):
        fail = np.load('./Data/fail.npy')
    else:
        fail = []
    base="https://geodes.santepubliquefrance.fr/#bbox=-367462,6426007,436234,269535&c=indicator&f=0&i=sursaud_sau.prop_asthme_hospit_sau&s=2019-S01&selcodgeo=50&t=a01&view=map2"
    CHANGE = False #put CHANGE to True if there were changes in the columns or indexes of the csv
    print('***First January 2020************')
    FirstJan2020, demo = FirstJan()

    #1. choose the weeks to handle
    print('*** pathology extraction ************')

    weeksPatho=[str(2019)+'-S0'+str(i) for i in range(1,10)]+[str(2019)+'-S'+str(i) for i in range(10,55)]+[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,19)]
    # weeksPatho=[str(2020)+'-S0'+str(i) for i in range(1,10)]+[str(2020)+'-S'+str(i) for i in range(10,19)]

    #2. choose the columns

    colUnifPatho = ['label','sex', 'mean_age',
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
    createCSV(weeksPatho, demo, colUnifPatho, 'weeks')
   
    for week in weeksPatho:
        
        fail, AlreadyDone =obtainDataWeek(week,AlreadyDone,fail)
    SaveXlsx('PathologyData',weeksPatho,'weeks') #save in a excel file

    print('*** covid extraction ************')
    colUnifCovid = ['label',
    'covid_sos_moins15','covid_sos_15_44','covid_sos_45_64','covid_sos_65_74','covid_sos_plus75','covid_sos_all',
    'covid_urg_moins15','covid_urg_15_44','covid_urg_45_64','covid_urg_65_74','covid_urg_plus75','covid_urg_all',
    'covid_hosp_moins15','covid_hosp_15_44','covid_hosp_45_64','covid_hosp_65_74','covid_hosp_plus75','covid_hosp_all',
    'covid_villeNbTest_moins15','covid_villeNbTest_15_44','covid_villeNbTest_45_64','covid_villeNbTest_65_74','covid_villeNbTest_plus75','covid_villeNbTest_all',
    'covid_villeTauxPos_moins15','covid_villeTauxPos_15_44','covid_villeTauxPos_45_64','covid_villeTauxPos_65_74','covid_villeTauxPos_plus75','covid_villeTauxPos_all',
    'covid_villeNbPos_moins15','covid_villeNbPos_15_44','covid_villeNbPos_45_64','covid_villeNbPos_65_74','covid_villeNbPos_plus75','covid_villeNbPos_all']
    weeksCovid=[str(2020)+'-S'+str(i) for i in range(10,19)]
    createCSV(weeksCovid, demo, colUnifCovid, 'covid')
 
    for week in weeksCovid:
        fail, AlreadyDone = obtainDataWeekCovid(week,AlreadyDone,fail)

    SaveXlsx('CovidData',weeksCovid,'covid')


    AlreadyDone = np.load('./Data/AlreadyDone.npy')