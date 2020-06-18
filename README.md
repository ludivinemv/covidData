# covid

## organisation
- Documents
- Data
  - Insee *(données démographiques récupérées sur DataGouv et utilisées par le code)*
  - Unify *(contient les données récupérées)*
    - covid *(contient les CSVs (1 par semaine) pour le covid)*
    - weeks *(contient les CSVs (1 par semaine) pour les autres pathologies)*
    - CovidData.xlsx *(xls regroupant les csv covid (1 feuille par semaine))*
    - PathologyData.xlsx *(xls regroupant les csv des autres pathologies (1 feuille par semaine))*
    - FirstJan2019.csv *(Contient les données démographiques au premier janvier 2019)*
    - FirstJan2020.csv *(Contient les données démographiques au premier janvier 2020)*
  - AlreadyDone.npy *(est utilisé par le code pour savoir ce qui est déjà rempli)*
  -fail.npy *(array donnant des informations sur ce qui a échoué lorsque l'on lance le code)*
- chromedriver_win32_81 
- chromedriver_win32_83

- README.md
- requirements.txt 
- Possibilités_covid.docx *(contient ce qui peut être récupéré sur le site Géodes, en rouge ce qui a été récupéré)*

- cleanPipeline.py *(fichier principal à lancer)*
- week_correspond.xlsx *(table utilisée par le code python pour correspondre les jours à une semaine. Il peut être étendu à d'autres semaines si besoin)*

## Construction des colonnes des CSVs:
- Index: code of the departement *(00 correspond to France)*
- Columns:
  - label: label of the departements
  - sex: rate of women *(seulement pour FirstJan2019 et FirstJan2020)*
  - age: moins de 15 ans, entre 15 et 65 et plus de 65 ans.  *(seulement pour FirstJan2019 et FirstJan2020)*
  - pathologies are build in 3 parts (pathology_object_age)
    - pathology 
      - covid
      - asthme
      - bronchite
      - grippe
      - pneumopathie
    - object 
      - sos: Taux d'actes médicaux SOS médecins (sur 10 000 actes)
      - urg: Taux de passage aux urgences (sur 10 000 passages)
      - hosp: Taux d'hospitalisation par passage au urgences (sur 10 000 passages)
      - (for covid) villeTest: number of tests
      - (for covid) villePos: positive tests
      - (for covid) nouvRea: nombre de nouvelles hospitalisations en réanimations par semaine *(all_age seulement)*
    - age
      - moins15: less than 15 year old
      - 15_65: between 15 and 65 year old *(devided in two classes for covid (15-44 and 45-64))*
      - plus65: more than 65 year old *(devided in two classes for covid (65-74 and plus 75))*

## Installation
- pip install -r requirements.txt
- utiliser python 3

## Explication du code
### Les options à choisir
- <ins>CHOOSE_CHROMEDRIVER</ins> : choisir entre la version '81' et '83'. Si besoin vous pouvez installer une autre version en ajoutant le chromedriver dans la racine dans le dossier chromedriver_win32_Number
- <ins>CHANGE</ins>: A mettre sur True si vous voulez tout supprimer et relancer. Pour simplement compléter les fichiers existant mettre à False
- <ins> weeksPatho et weeksCovid</ins>: modifier weeksPatho en fonction des semaines désirées. C'est ici qu'il faut modifier pour ajouter les nouvelles semaines au fur et à mesure ( ** /!\ ** pour l'instant il ne reconnait pas lorsque la semaine n'est pas présente, donc si une semaine n'existe pas, au lieu de passer au except, il remplit avec des données d'une semaine avec un url proche.)
- <ins>colUnifPatho et colUnifCovid </ins> : si besoin rajouter les colonnes ici 
