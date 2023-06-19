
import pandas as pd
import os
import csv

'''
================================================================================
SLP's definieren
================================================================================
'''

profielen = pd.read_csv(os.path.join('slp_files', 'profielenToepassingen.csv'))
# cop = pd.read_csv(os.path.join('slp_files', 'cop1.csv'))


SLPrv = profielen.iloc[:,0].tolist()
SLPsww = profielen.iloc[:,1].tolist()
SLPelec = profielen.iloc[:,2].tolist()
# COPvar1 = cop.iloc[:,0].tolist()
# COPgeo = cop.iloc[:,2].tolist()
# COPair = cop.iloc[:,4].tolist()
# COPwat = cop.iloc[:,6].tolist()
SLPs = {"ruimteverwarming":SLPrv,"sanitair warm water":SLPsww,"elektriciteit":SLPelec} #,"COP":COPvar1}
toepassingen = ["ruimteverwarming", "sanitair warm water","elektriciteit"]


'''
================================================================================
HIERONDER EEN LIJST VAN INPUTVOORZIENGEN EN DE INGEGEVEN DATA
================================================================================
'''

# https://www.energids.be/nl/vraag-antwoord/hoeveel-co2-stoot-mijn-woning-uit/68/#:~:text=aardgas%3A%200%2C198%20kg%20CO2,kg%20CO2%20per%20kWh
# https://www.vlaanderen.be/epb-pedia/rekenmethode/rekenmethode-e-peil/karakteristiek-jaarlijks-primair-energieverbruik
verbruikers = {
    "elektriciteit":{"naam": "elektriciteit", "co2 per kwh":0.23,"omzetting prim energie":2.5,"kost per kwh":0.4,"eenheid":"kWh","avg":3500},
    "aardgas":{"naam": "aardgas","co2 per kwh":0.198,"omzetting prim energie":1,"kost per kwh":0.1,"eenheid":"kWh","avg":20000},
    "stookolie":{"naam":"stookolie","co2 per kwh":0.264,"omzetting prim energie":1,"kost per kwh":0.08,"eenheid":"liter","tokWh":10,"avg":2300},
    "zonne-energie":{"naam":"zonne-energie","co2 per kwh":0,"omzetting prim energie":0,"kost per kwh":0,"eenheid":"liter","tokWh":0,"avg":2300}
    }   

#INPUTVOORZIENINGEN: de voorzieningen die de user te zien krijgt bij initiatie van de tool

# heatPump_LW_3 = {"naam":"lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair}

cvKetel_gas = {"naam":"Gasketel","maxVermogen":"/","Toepassing":"Ruimteverwarming","eenheid vermogen":'kW',"verbruiker": "aardgas","efficientie":0.9,"prijs":0,"varEff":None}
cvKetel_stookolie = {"naam":"Stookolieketel","eenheid vermogen":'kW',"maxVermogen":"/","Toepassing":"Ruimteverwarming","verbruiker": "stookolie","efficientie":0.9,"prijs":0}
doorstroomGas = {"naam":"Doorstroomboiler op gas","Toepassing":"Ruimteverwarming","verbruiker":"aardgas","efficientie":0.95,"maxVermogen":"","eenheid vermogen":"","prijs":0} 
elecVerwarming = {"naam":"Elektrische verwarming","Toepassing":"Ruimteverwarming","verbruiker":"elektriciteit","efficientie":1} 
zonneboiler = {"naam":"Zonneboiler","Toepassing":"Sanitair warm water","verbruiker":"zonne-energie","efficientie":1,'prijs':0} 
doorstroomElec = {"naam":"Elektrische doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","continue verbruik (kWh)":0.225,"inhoud":5,"efficientie":1,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":0}
elektriciteit_net = {"naam":"elektriciteitsnet","Toepassing":"elektriciteit","verbruiker": "elektriciteit","efficientie":1,'prijs':0,"maxVermogen":"","eenheid vermogen":"","PV":False}

"""elektriciteit"""
# elektriciteitPV = {"naam":"elektriciteitsnet en PV","Toepassing":"elektriciteit","verbruiker": "elektriciteit","efficientie":1,'prijs':0,"maxVermogen":"","eenheid vermogen":"","PV":True}  #prijs en opbrengst hangen af van de input van de user
# PV = {"naam":"enkel pv","Toepassing":"elektriciteit","verbruiker": "zonne-energie","efficientie":1,'prijs':0}

# elektrischeDoorstroomboiler_10 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","continue verbruik (kWh)":0.273,"inhoud":10,"efficientie":1,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":280}

"""inputscenarios"""

RVinput = [cvKetel_gas, cvKetel_stookolie]

SWWinput= [doorstroomGas,doorstroomElec, zonneboiler]

combiInput = [cvKetel_gas, cvKetel_stookolie]

Elecinput = [elektriciteit_net]

"""
================================================================================
VOORZIENINGEN
================================================================================
"""
"""COP matrix"""
"""
                    slecht isolatie - matig isolatie - goed isolatie
Radiator        |         x      |           x        |         x
Vloerverwarming |           x     |       x           |     x
"""
copLW = [[1.20,2.2,3.30],[4.39,4.72,5.16]]   
copGW= [[1.21,2.42,3.63],[4.84,5.20,5.69]]
copLL= [[1.35,2.05,3.08],[4.1,4.41,4.82]]


cops = {"lucht-water warmtepomp":copLW,"bodem-water warmtepomp":copGW,"lucht-lucht warmtepomp":copLL,"hybride warmtepomp":copLW}
#warmtepompen
heatPump_LW_3 = {"naam":"lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000} #,"varEff":COPair}
heatPump_LW_5 = {"naam":"Lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":7000}#,"varEff":COPair}
heatPump_LW_8 = {"naam":"lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":10000}#,"varEff":COPair}
heatPump_LW_10 = {"naam":"lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":11000}#,"varEff":COPair}
heatPump_LW_12 = {"naam":"lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":12,"eenheid vermogen":'kW',"prijs":12000}#,"varEff":COPair}
heatPump_LW_15 = {"naam":"lucht-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":15000}#,"varEff":COPair}

heatPump_GW_3 = {"naam":"bodem-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6800} #,"varEff":COPgeo}
heatPump_GW_5 = {"naam":"bodem-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":13900} #,"varEff":COPgeo}
heatPump_GW_8 = {"naam":"bodem-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":16300} #,"varEff":COPgeo}
heatPump_GW_10 = {"naam":"bodem-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":19000} #,"varEff":COPgeo}
heatPump_GW_12 = {"naam":"bodem-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":12,"eenheid vermogen":'kW',"prijs":20000} #,"varEff":COPgeo}
heatPump_GW_15 = {"naam":"bodem-water warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":25000} #,"varEff":COPgeo}

heatPump_LL_3 = {"naam":"lucht-lucht warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":5000 }#,"varEff":COPair}
heatPump_LL_5 = {"naam":"lucht-lucht warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":5300}#,"varEff":COPair}
heatPump_LL_8 = {"naam":"lucht-lucht warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":5500}#,"varEff":COPair}
heatPump_LL_10 = {"naam":"lucht-lucht warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":5700}#,"varEff":COPair}
heatPump_LL_12 = {"naam":"lucht-lucht warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":12,"eenheid vermogen":'kW',"prijs":6000}#,"varEff":COPair}

heatPump_LL_15 = {"naam":"lucht-lucht warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":7000} #,"varEff":COPair}


heatPump_HY_3 = {"naam":"hybride warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000,"aandeel":0.7}
heatPump_HY_5 = {"naam":"hybride warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":7000,"aandeel":0.7}
heatPump_HY_8 = {"naam":"hybride warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":10000,"aandeel":0.7}
heatPump_HY_10 = {"naam":"hybride warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":11000,"aandeel":0.7}
heatPump_HY_12 = {"naam":"hybride warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":12,"eenheid vermogen":'kW',"prijs":12000,"aandeel":0.7}
heatPump_HY_15 = {"naam":"hybride warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":15000,"aandeel":0.7}

#doorstroomboilers

#voorzieningen in een lijst per soort plaatsen, deze worden doorlopen tijdens de berekening en een wordt gekozen op basis van de dimensionering
#lijsten van voorziening



#de lijsten hieronder gaan naar de berekeningfiles, dus de voorzieningen die hier niet in staat  worden niet doorgegeven en berekent


'''
================================================================================
SCENARIOS
hier komt een lijst van dictionaries die een scenario voorstellen, voor elke voorziening een toepassing. op deze manier heeft de code controle over met welke voorzieningen de huidige situatie vergelijken
================================================================================
'''
"""
lists die naar de berekeningen gestuurd wordt
"""

warmtepomp_LW = [heatPump_LW_3,heatPump_LW_5,heatPump_LW_8,heatPump_LW_10,heatPump_LW_12,heatPump_LW_15]
warmtepomp_GW = [heatPump_GW_3,heatPump_GW_5,heatPump_GW_8,heatPump_GW_10,heatPump_GW_12,heatPump_GW_15]
warmtepomp_LL = [heatPump_LL_3,heatPump_LL_5,heatPump_LL_8,heatPump_LL_10,heatPump_LL_12,heatPump_LL_15]
warmtepomp_HY = [heatPump_HY_3,heatPump_HY_5,heatPump_HY_8,heatPump_HY_10,heatPump_HY_12,heatPump_HY_15]

warmtepompen = {'warmtepomp_LW':warmtepomp_LW,'warmtepomp_LL':warmtepomp_LL,'warmtepomp_GW':warmtepomp_GW,'warmtepomp_HY':warmtepomp_HY,"Gasketel":cvKetel_gas}
andere = {"Gasketel":cvKetel_gas,"elektriciteitsnet":elektriciteit_net,"Stookolieketel":cvKetel_stookolie,"Elektrische doorstroomboiler":doorstroomElec,"Doorstroomboiler op gas":doorstroomGas,"Zonneboiler":zonneboiler}

#scenarios

#de lijsten hieronder gaan naar de berekeningfiles, dus de scenarios die hier niet in staat  worden niet doorgegeven en berekent
scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp_LW","sanitair warm water":"warmtepomp_LW","elektriciteit":"elektriciteitsnet", "PV" :False}
scenario2 = {"scenario":"scenario 2", "ruimteverwarming":"warmtepomp_GW","sanitair warm water":"warmtepomp_GW","elektriciteit":"elektriciteitsnet", "PV" :False}
scenario3 = {"scenario":"scenario 3","ruimteverwarming":"warmtepomp_LL","sanitair warm water":"Gasketel","elektriciteit":"elektriciteitsnet", "PV" : False}
scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp_HY","sanitair warm water":"warmtepomp_HY","elektriciteit":"elektriciteitsnet", "PV" : False}
# scenario1 = {"scenario":"scenario 1", "toepassingen":{"combi":"warmtepomp_LW","elektriciteit":"elektriciteitsnet"}, "PV" :False}


scenarios = [scenario1,scenario2,scenario3,scenario4]
