
import pandas as pd
import os
import csv




'''
================================================================================
CSV FILE INLEZEN
================================================================================
'''
# ALLE INGELEZEN DATA HIERONDER komt uit de csv: "overzichtSLPs.csv
# def insertCSV(filename):
#     filename="overzichtSLPs.csv"
#     csv = str(filename)
#     path = os.getcwd()
#     pathcsv = os.path.join(path, csv)
#     data = pd.read_csv(os.path.join(path, csv))
#     return data

'''
================================================================================
SLP's definieren
================================================================================
'''
SLPrv = pd.read_csv("slp_files\profielenToepassingen.csv").iloc[:,0].tolist()
SLPsww = pd.read_csv("slp_files\profielenToepassingen.csv").iloc[:,1].tolist()
SLPelec = pd.read_csv("slp_files\profielenToepassingen.csv").iloc[:,2].tolist()
COPvar1 = pd.read_csv("slp_files\cop1.csv").iloc[:,0].tolist()
COPgeo = pd.read_csv("slp_files\cop1.csv").iloc[:,2].tolist()
COPair = pd.read_csv("slp_files\cop1.csv").iloc[:,4].tolist()
COPwat = pd.read_csv("slp_files\cop1.csv").iloc[:,6].tolist()
SLPs = {"ruimteverwarming":SLPrv,"sanitair warm water":SLPsww,"elektriciteit":SLPelec,"COP":COPvar1}
toepassingen = ["ruimteverwarming", "sanitair warm water","elektriciteit"]




'''
================================================================================
HIERONDER EEN LIJST VAN INPUTVOORZIENGEN EN DE INGEGEVEN DATA
================================================================================
'''

# https://www.energids.be/nl/vraag-antwoord/hoeveel-co2-stoot-mijn-woning-uit/68/#:~:text=aardgas%3A%200%2C198%20kg%20CO2,kg%20CO2%20per%20kWh
# https://www.vlaanderen.be/epb-pedia/rekenmethode/rekenmethode-e-peil/karakteristiek-jaarlijks-primair-energieverbruik
verbruikers = {
    "elektriciteit":{"naam": "elektriciteit", "co2 per kwh":0.23,"omzetting prim energie":2.5,"kost per kwh":0.3,"eenheid":"kWh","tokWh":1},
    "aardgas":{"naam": "aardgas","co2 per kwh":0.198,"omzetting prim energie":1,"kost per kwh":0.5,"eenheid":"kWh","tokWh":1},
    "stookolie":{"naam":"stookolie","co2 per kwh":0.264,"omzetting prim energie":1,"kost per kwh":0.5,"eenheid":"liter","tokWh":10},
    "zonne-energie":{"co2 per kwh":0,"omzetting prim energie":0,"kost per kwh":0},
    "hout":{"co2 per kwh":0,"omzetting prim energie":0,"kost per kwh":0}
    }   

#INPUTVOORZIENINGEN: de voorzieningen die de user te zien krijgt bij initiatie van de tool

# heatPump_LW_3 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair}

cvKetel_gas = {"naam":"Gasketel","maxVermogen":"/","Toepassing":"Ruimteverwarming","eenheid vermogen":'kW',"verbruiker": "aardgas","efficientie":0.9,"prijs":0,"varEff":None}
cvKetel_stookolie = {"naam":"Stookolieketel","Toepassing":"Ruimteverwarming","verbruiker": "stookolie","efficientie":0.9}
pelletkachel = {"naam":"pelletkachel","Toepassing":"Ruimteverwarming","verbruiker":"houtpellet","efficientie":0.85} 
elecKetel = {"naam":"Elektrische ketel","Toepassing":"Ruimteverwarming","verbruiker":"elektriciteit","efficientie":1} 
doorstroomGas = {"naam":"Doorstroomboiler op gas","Toepassing":"Ruimteverwarming","verbruiker":"aardgas","efficientie":0.95} 
elecVerwarming = {"naam":"Elektrische verwarming","Toepassing":"Ruimteverwarming","verbruiker":"elektriciteit","efficientie":1} 
zonneboiler = {"naam":"Zonneboiler","Toepassing":"Sanitair warm water","verbruiker":"zonne-energie","efficientie":1} 

"""elektriciteit"""
elektriciteit_net = {"naam":"elektriciteitsnet","Toepassing":"elektriciteit","verbruiker": "elektriciteit","efficientie":1,'prijs':0,"maxVermogen":"","eenheid vermogen":"","PV":False}
elektriciteitPV = {"naam":"elektriciteitsnet en PV","Toepassing":"elektriciteit","verbruiker": "elektriciteit","efficientie":1,'prijs':0,"maxVermogen":"","eenheid vermogen":"","PV":True}  #prijs en opbrengst hangen af van de input van de user
PV = {"naam":"enkel pv","Toepassing":"elektriciteit","verbruiker": "zonne-energie","efficientie":1,'prijs':0}

doorstroomElec = {"naam":"Elektrische doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","continue verbruik (kWh)":0.225,"inhoud":5,"efficientie":1,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":200}
elektrischeDoorstroomboiler_10 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","continue verbruik (kWh)":0.273,"inhoud":10,"efficientie":1,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":280}


"""inputscenarios"""


RVinput = [cvKetel_gas, cvKetel_stookolie,elecVerwarming]

SWWinput= [doorstroomGas,doorstroomElec,zonneboiler]

combiInput = [cvKetel_gas, cvKetel_stookolie,elecKetel]

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

copLW = [[4,4.2,4.5],[4.6,4.8,5]]   
copGW= [[4.5,4.7,4.9],[5,5.2,5.4]]
copLL= [[4,4.2,4.5],[4.6,4.8,5]]
copHY= [[4,4.2,4.5],[4.6,4.8,5]]

cops = {"lucht-water Warmtepomp":copLW,"bodem-water Warmtepomp":copGW,"lucht-lucht Warmtepomp":copLL,"hybride Warmtepomp":copHY}
#warmtepompen
heatPump_LW_3 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair}
heatPump_LW_5 = {"naam":"Lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":7000,"varEff":COPair}
heatPump_LW_8 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":10000,"varEff":COPair}
heatPump_LW_10 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":11000,"varEff":COPair}

heatPump_GW_3 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6800,"varEff":COPgeo}
heatPump_GW_5 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":13900,"varEff":COPgeo}
heatPump_GW_8 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":16300,"varEff":COPgeo}
heatPump_GW_10 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":19000,"varEff":COPgeo}

heatPump_WW_3 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":9000,"varEff":COPwat}
heatPump_WW_5 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":9300,"varEff":COPwat}
heatPump_WW_8 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":9500,"varEff":COPwat}
heatPump_WW_10 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":10000,"varEff":COPwat}
heatPump_WW_15 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":11000,"varEff":COPwat}

heatPump_LL_3 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":5000,"varEff":COPair,"aandeel":0.7}
heatPump_LL_5 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":5300,"varEff":COPair,"aandeel":0.7}
heatPump_LL_8 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":5500,"varEff":COPair,"aandeel":0.7}
heatPump_LL_10 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair,"aandeel":0.7}
heatPump_LL_15 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":7000,"varEff":COPair,"aandeel":0.7}


heatPump_HY_3 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":9000,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_5 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":9300,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_8 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":9500,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_10 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":10000,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_15 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":11000,"varEff":COPgeo,"aandeel":0.7}

#doorstroomboilers
doorstroomboiler_5 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","efficientie":1,"maxVermogen":5,"prijs":500}
elektrischeDoorstroomboiler_5 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","continue verbruik (kWh)":0.225,"inhoud":5,"efficientie":1,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":200}
elektrischeDoorstroomboiler_10 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","continue verbruik (kWh)":0.273,"inhoud":10,"efficientie":1,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":280}
#condensatieketels #vermogen is hier in KW
condensketel_13 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":13,"eenheid vermogen":'kW',"prijs":1835}
condensketel_20 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":20,"eenheid vermogen":'kW',"prijs":2038}
condensketel_30 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":30,"eenheid vermogen":'kW',"prijs":2600}
condensketel_50 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":50,"eenheid vermogen":'kW',"prijs":3800}
condensketel_80 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":80,"eenheid vermogen":'kW',"prijs":4800}
condensketel_100 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":100,"eenheid vermogen":'kW',"prijs":5500}
#zonneboiler
#nummer achter de naam is de boilerinhoud in Liter
zonneboiler_150 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"maxVermogen":150,"eenheid vermogen":'L', "gezinsgrootte":3,"prijs":2543}
zonneboiler_250 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"maxVermogen":250,"eenheid vermogen":'L',"gezinsgrootte":5,"prijs":3000}
zonneboiler_350 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"maxVermogen":350,"eenheid vermogen":'L',"gezinsgrootte":7,"prijs":3500}
#warmtepompboiler  #vermogen is hier in L weergegeven
warmtepompboiler_LW_150 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","efficientie":2.5,"maxVermogen":150,"eenheid vermogen":'L',"prijs":2294}
warmtepompboiler_LW_200 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","efficientie":3.19,"maxVermogen":200,"eenheid vermogen":'L',"prijs":2790}
warmtepompboiler_LW_270 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","efficientie":3.19,"maxVermogen":270,"eenheid vermogen":'L',"prijs":2906}

#voorzieningen in een lijst per soort plaatsen, deze worden doorlopen tijdens de berekening en een wordt gekozen op basis van de dimensionering
#lijsten van voorziening
warmtepomp_LW = [heatPump_LW_3,heatPump_LW_5,heatPump_LW_8,heatPump_LW_10]
warmtepomp_GW = [heatPump_GW_3,heatPump_GW_5,heatPump_GW_8,heatPump_GW_10]
warmtepomp_WW = [heatPump_WW_3,heatPump_WW_5,heatPump_WW_8,heatPump_WW_10,heatPump_WW_15]
warmtepomp_LL = [heatPump_LL_3,heatPump_LL_5,heatPump_LL_8,heatPump_LL_10,heatPump_LL_15]
warmtepomp_HY = [heatPump_HY_3,heatPump_HY_5,heatPump_HY_8,heatPump_HY_10,heatPump_HY_15]


#de lijsten hieronder gaan naar de berekeningfiles, dus de voorzieningen die hier niet in staat  worden niet doorgegeven en berekent
condensatieketels = [condensketel_13, condensketel_20,condensketel_30,condensketel_50,condensketel_80,condensketel_100]
doorstroomboilersE = [elektrischeDoorstroomboiler_5,elektrischeDoorstroomboiler_10]
zonneboilers = [zonneboiler_150,zonneboiler_250,zonneboiler_350]
warmtepompboiler = [warmtepompboiler_LW_150,warmtepompboiler_LW_200,warmtepompboiler_LW_270]

list_voorzieningenRV = [cvKetel_gas, warmtepomp_LW,condensatieketels]
list_voorzieningenSWW = [cvKetel_gas, warmtepomp_LW,warmtepomp_GW,warmtepomp_WW,doorstroomboilersE]

'''
================================================================================
SCENARIOS
hier komt een lijst van dictionaries die een scenario voorstellen, voor elke voorziening een toepassing. op deze manier heeft de code controle over met welke voorzieningen de huidige situatie vergelijken
================================================================================
'''

#scenarios
"""
mogelijkheden
ruimteverwarming: warmtepomp LW, warmtepomp GW, wartepomp WW, warmtepomp LW, gasketel, condensatiektel
sanitair warm water:warmtepomp LW, warmtepomp GW, wartepomp WW, warmtepomp LW, gasketel, condensatiektel
elektriciteit: elektriciteitsnet, elektriciteitsnet en PV 
"""
# scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler elektrisch","elektriciteit":"elektriciteitsnet", "PV" :False}
# scenario2 = {"scenario":"scenario 2", "ruimteverwarming":"warmtepomp GW","sanitair warm water":"doorstroomboiler elektrisch","elektriciteit":"elektriciteitsnet", "PV" :False}
# scenario3 = {"scenario":"scenario 3", "ruimteverwarming":"warmtepomp WW","sanitair warm water":"doorstroomboiler elektrisch","elektriciteit":"elektriciteitsnet", "PV" : False}
# scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler elektrisch","elektriciteit":"elektriciteitsnet", "PV" : False}
# scenario5 = {"scenario":"scenario 5","ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler gas","elektriciteit":"elektriciteitsnet", "PV" : False}
# scenario6 = {"scenario":"scenario 6","ruimteverwarming":"warmtepomp LW","sanitair warm water":"warmtepomp LW","elektriciteit":"elektriciteitsnet", "PV" : False}
scenario7 = {"scenario":"scenario 7","ruimteverwarming":"condensatieketel","sanitair warm water":"condensatieketel","elektriciteit":"elektriciteitsnet", "PV" : False}
#de lijsten hieronder gaan naar de berekeningfiles, dus de scenarios die hier niet in staat  worden niet doorgegeven en berekent
scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp LW","sanitair warm water":"warmtepomp LW","elektriciteit":"elektriciteitsnet", "PV" :False, 'criteria':['Q1']}
scenario2 = {"scenario":"scenario 2", "ruimteverwarming":"warmtepomp GW","sanitair warm water":"warmtepomp GW","elektriciteit":"elektriciteitsnet", "PV" :False, 'criteria':['Q1']}
scenario3 = {"scenario":"scenario 3", "ruimteverwarming":"warmtepomp WW","sanitair warm water":"warmtepomp WW","elektriciteit":"elektriciteitsnet", "PV" : False, 'criteria':['Q0']}
scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp LL","sanitair warm water":"Gasketel","elektriciteit":"elektriciteitsnet", "PV" : False, 'criteria':['Q2'],"verdeling":[0.7,1,1]}
scenario5 = {"scenario":"scenario 5","ruimteverwarming":"warmtepomp HY","sanitair warm water":"warmtepomp HY","elektriciteit":"elektriciteitsnet", "PV" : False, 'criteria':['Q2','Q3','Q4']}


scenarios = [scenario1,scenario2,scenario4,scenario5]
# scenarios = [scenario1]