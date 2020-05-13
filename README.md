# covid

## Results table organisation:
- Index: code of the departement (0 correspond to France)
- Columns:
  - label: label of the departements
  - sex: rate of women
  - mean_age: average age
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
    - age
      - moins15: less than 15 year old
      - 15_65: between 15 and 65 year old
      - plus65: more than 65 year old
