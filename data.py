
import pandas as pd
import os
import csv

'''
================================================================================
SLP's definieren
================================================================================
'''

profielen = pd.read_csv(os.path.join('slp_files', 'profielenToepassingen.csv'))
cop = pd.read_csv(os.path.join('slp_files', 'cop1.csv'))


SLPrv = profielen.iloc[:,0].tolist()
SLPsww = profielen.iloc[:,1].tolist()
SLPelec = profielen.iloc[:,2].tolist()
COPvar1 = cop.iloc[:,0].tolist()
COPgeo = cop.iloc[:,2].tolist()
COPair = cop.iloc[:,4].tolist()
COPwat = cop.iloc[:,6].tolist()
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
    "elektriciteit":{"naam": "elektriciteit", "co2 per kwh":0.23,"omzetting prim energie":2.5,"kost per kwh":0.4,"eenheid":"kWh","avg":3500},
    "aardgas":{"naam": "aardgas","co2 per kwh":0.198,"omzetting prim energie":1,"kost per kwh":0.1,"eenheid":"kWh","avg":20000},
    "stookolie":{"naam":"stookolie","co2 per kwh":0.264,"omzetting prim energie":1,"kost per kwh":0.08,"eenheid":"liter","tokWh":10,"avg":2300},
    }   

#INPUTVOORZIENINGEN: de voorzieningen die de user te zien krijgt bij initiatie van de tool

# heatPump_LW_3 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair}

cvKetel_gas = {"naam":"Gasketel","maxVermogen":"/","Toepassing":"Ruimteverwarming","eenheid vermogen":'kW',"verbruiker": "aardgas","efficientie":0.9,"prijs":0,"varEff":None}
cvKetel_stookolie = {"naam":"Stookolieketel","eenheid vermogen":'kW',"maxVermogen":"/","Toepassing":"Ruimteverwarming","verbruiker": "stookolie","efficientie":0.9,"prijs":0}
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


RVinput = [cvKetel_gas, cvKetel_stookolie]

SWWinput= [doorstroomGas,doorstroomElec] #,zonneboiler]

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
#[[1.2,2.19,3.28],[4.38,4.7,5.14]]
copLW = [[1.1,2.3,3.4],[4.4,5,5.3]]   
copGW= [[1.4,2.4,3.8],[4.8,5.3,5.6]]
copLL= [[1.03,2.05,3.08],[4.1,4.41,4.82]]
copHY= [[1.1,2.3,3.4],[4.4,5,5.3]]  

 

cops = {"lucht-water Warmtepomp":copLW,"bodem-water Warmtepomp":copGW,"lucht-lucht Warmtepomp":copLL,"hybride Warmtepomp":copHY}
#warmtepompen
heatPump_LW_3 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair}
heatPump_LW_5 = {"naam":"Lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":7000,"varEff":COPair}
heatPump_LW_8 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":10000,"varEff":COPair}
heatPump_LW_10 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":11000,"varEff":COPair}
heatPump_LW_12 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":12,"eenheid vermogen":'kW',"prijs":12000,"varEff":COPair}
heatPump_LW_15 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copLW,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":15000,"varEff":COPair}

heatPump_GW_3 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":6800,"varEff":COPgeo}
heatPump_GW_5 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":13900,"varEff":COPgeo}
heatPump_GW_8 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":16300,"varEff":COPgeo}
heatPump_GW_10 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":19000,"varEff":COPgeo}
heatPump_GW_12 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":12,"eenheid vermogen":'kW',"prijs":20000,"varEff":COPgeo}
heatPump_GW_15 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":copGW,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":25000,"varEff":COPgeo}

heatPump_LL_3 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":5000,"varEff":COPair}
heatPump_LL_5 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":5300,"varEff":COPair}
heatPump_LL_8 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":5500,"varEff":COPair}
heatPump_LL_10 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPair}
heatPump_LL_15 = {"naam":"lucht-lucht Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":7000,"varEff":COPair}


heatPump_HY_3 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":3000,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_5 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":4000,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_8 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":5000,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_10 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":6000,"varEff":COPgeo,"aandeel":0.7}
heatPump_HY_15 = {"naam":"hybride Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "elektriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":8000,"varEff":COPgeo,"aandeel":0.7}

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
warmtepomp_LW = [heatPump_LW_3,heatPump_LW_5,heatPump_LW_8,heatPump_LW_10,heatPump_LW_12,heatPump_LW_15]
warmtepomp_GW = [heatPump_GW_3,heatPump_GW_5,heatPump_GW_8,heatPump_GW_10,heatPump_GW_12,heatPump_GW_15]
warmtepomp_LL = [heatPump_LL_3,heatPump_LL_5,heatPump_LL_8,heatPump_LL_10,heatPump_LL_15]
warmtepomp_HY = [heatPump_HY_3,heatPump_HY_5,heatPump_HY_8,heatPump_HY_10,heatPump_HY_15]


#de lijsten hieronder gaan naar de berekeningfiles, dus de voorzieningen die hier niet in staat  worden niet doorgegeven en berekent
condensatieketels = [condensketel_13, condensketel_20,condensketel_30,condensketel_50,condensketel_80,condensketel_100]
doorstroomboilersE = [elektrischeDoorstroomboiler_5,elektrischeDoorstroomboiler_10]
zonneboilers = [zonneboiler_150,zonneboiler_250,zonneboiler_350]
warmtepompboiler = [warmtepompboiler_LW_150,warmtepompboiler_LW_200,warmtepompboiler_LW_270]

list_voorzieningenRV = [cvKetel_gas, warmtepomp_LW,condensatieketels]
list_voorzieningenSWW = [cvKetel_gas, warmtepomp_LW,warmtepomp_GW,doorstroomboilersE]

'''
================================================================================
SCENARIOS
hier komt een lijst van dictionaries die een scenario voorstellen, voor elke voorziening een toepassing. op deze manier heeft de code controle over met welke voorzieningen de huidige situatie vergelijken
================================================================================
'''
"""
lists die naar de berekeningen gestuurd wordt
"""
warmtepompen = {'warmtepomp_LW':warmtepomp_LW,'warmtepomp_LL':warmtepomp_LL,'warmtepomp_GW':warmtepomp_GW,'warmtepomp_HY':warmtepomp_HY,"Gasketel":cvKetel_gas}
andere = {"Gasketel":cvKetel_gas,"elektriciteitsnet":elektriciteit_net,"Stookolieketel":cvKetel_stookolie}

#scenarios

#de lijsten hieronder gaan naar de berekeningfiles, dus de scenarios die hier niet in staat  worden niet doorgegeven en berekent
scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp_LW","sanitair warm water":"warmtepomp_LW","elektriciteit":"elektriciteitsnet", "PV" :False}
scenario2 = {"scenario":"scenario 2", "ruimteverwarming":"warmtepomp_GW","sanitair warm water":"warmtepomp_GW","elektriciteit":"elektriciteitsnet", "PV" :False}
scenario3 = {"scenario":"scenario 3","ruimteverwarming":"warmtepomp_LL","sanitair warm water":"Gasketel","elektriciteit":"elektriciteitsnet", "PV" : False}
scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp_HY","sanitair warm water":"warmtepomp_HY","elektriciteit":"elektriciteitsnet", "PV" : False}
# scenario1 = {"scenario":"scenario 1", "toepassingen":{"combi":"warmtepomp_LW","elektriciteit":"elektriciteitsnet"}, "PV" :False}


scenarios = [scenario1,scenario2,scenario3,scenario4]
