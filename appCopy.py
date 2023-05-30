from forms import *
from flask import render_template
from data import verbruikers,SLPs,warmtepompen,andere
from flask_weasyprint import HTML
from pypdf import PdfMerger
from io import BytesIO
from matplotlib import pyplot as plt
import numpy as np
import os

'''
================================================================================
#DIMENSIONERING VAN NIEUWE VOORZIENINGEN
================================================================================
'''
def dimensionering(voorziening,totvraag,insulation):  
    """
    Functie om de nieuwe warmtepomp te dimensioneren. 
    gebeurd op basis van totale vraag en vollasturen gebaseerd op isolatiegraad
    input:
        - voorziening: naam van de nieuwe voorziening eg: "warmtepomp_LW"
        - totvraag: vraag voor alle toepassingen met dezelfde voorziening
        - insulation, een integer die de index van isolatiegraad weergeeft. bepaalt het de index in vollasturen en dus het nieuwe vermogen
    return: de dictionary van de correct gedimensioneerde warmtepomp 
    """
    loadh = [1500,1750,2000]  #lijst van vollasturen, een lage isolatiegraad --> lage index --> delen door een lager getal --> groter vermogen

    if voorziening not in andere.keys():  #als de voorziening een warmtepomp is
        h = loadh[insulation]
        vermogen = totvraag/h  #nieuw vermogen bepalen,
        print(vermogen)
        selectlist = warmtepompen.get(voorziening)  #juiste lijst van warmtepompen selecteren
        ranges = sorted([i.get('maxVermogen') for i in selectlist])  #lijst met ranges van vermogen opstellen
        print(selectlist[0].get('naam'),ranges)  
        for range in ranges:  #door de lijst van ranges gaan en diegene pakken die het dichtsbij de vraag ligt (naar boven afgerond)
            if vermogen <= range:
                newvoorziening = selectlist[ranges.index(range)]
                break #stop als range gevonden is 
            elif vermogen > ranges[-1]:
                print("vermogen niet in range")
                newvoorziening = selectlist[(len(ranges)-1)]
                break  #stop als voorziening geselecteerd is 
            else:
                 continue
            
    elif voorziening in andere.keys(): #als de voorziening geen warmtepomp is
         newvoorziening = andere.get(voorziening)

    else: 
        print("voorziening niet gevonden")
    
    return newvoorziening



def selectCOP(index,matrix):
    #index is een tuple afkomstig van runtool, based on isolatiegraad en afgiftesysteem
    #matrix is de lijst met 2 lijsten die als matrix dient om de verschillende cop waardes in te geven
    if type(matrix) == list:
        r = index[0]
        c = index[1]
        cop = matrix[r][c]
    else:
        cop = matrix

    return cop

"""
================================================================================
INPUTS VAN DE GEBRUIKER VERWERKEN
================================================================================
"""
def verbruikProfiel(totverbruik,verbruiksprofiel):
    """
    huidig verbruik verdelen over procentueel verbruikprofiel -> verbruikprofiel genereren
    input:
        - totverbruik: het totale jaarverbruik
        - verbruiksprofiel: de overeenkomstige SLP
    return:
        een list met op elke index het jaarverbruik vermenigvuldigt met de overeenkomstige procentuele waarde in het slp
    """
    profiel = [i*totverbruik for i in verbruiksprofiel]
    return profiel

def nieuweVoorzieningen(scenario,toepassing,huidigprof,index):  
    """#deze functie wordt doorlopen door alle scenarios die meegegeven worden en bepaalt daaruit welke de nieuwe voorzieningen worden die vergelekenn gaan worden met de huidige situatie"""

    a = scenario.get(toepassing)  #de nieuwe voorziening voor toepassing i 
    if list(scenario.values()).count(a) == 1: 
                # maxvraag = (huidigprof.get("dictVoorzieningen").get(toepassing).get('maxvraag'))*4  #maal 4 om kwkwartier om te zetten naar kWh
                vraag = huidigprof.get("dictVoorzieningen").get(toepassing).get('totvraag')
                nieuwVoorziening = dimensionering(a,vraag,insulation = index[1])
                eff = {"efficientie":selectCOP(index = index,matrix = nieuwVoorziening.get('efficientie'))}
                nieuwVoorziening.update(eff)
                                
                                
                                
                print("nieuwe efficientie",eff)

                # d = {toepassing:nieuwVoorziening}
                # nieuwevoorzieningen.update(d)

    elif list(scenario.values()).count(a) > 1:
                zelfdevoorziening = [k for k,v in scenario.items() if v == a]  #lijst met alle namen van toepassingen die dezelfde voorziening gebruiken
                vraag = [(huidigprof.get("dictVoorzieningen").get(i).get('totvraag')) for i in zelfdevoorziening]      #maal 4 om kwkwartier om te zetten naar kWh
                nieuwVoorziening = dimensionering(a,sum(vraag),insulation = index[1])


                eff = {"efficientie":selectCOP(index = index,matrix = nieuwVoorziening.get('efficientie'))}
                nieuwVoorziening.update(eff)
                print("nieuwe efficientie",eff)
                # d = {zelfdevoorziening[i]:nieuwVoorziening for i in range(len(zelfdevoorziening))}
                # nieuwevoorzieningen.update(d)
    return nieuwVoorziening

def verbruikverdeling(verbruik,pers, huidigevoorziening): #verbruik is een dictionary met elke verbruiker en het verbruik, Swwvraag is een input, huidigevoorziening is een dict van de huidige voorzieningen per toepassing
    volumevraagSWW = 40.71*pers*365
    cp = 4186 #j/kg*k
    dt = 50 #°c
    rho = 0.997 #kg/l
    m = volumevraagSWW*rho
    warmtevraagSWW_J = m*cp*dt #dT 10-> 60: 50°c
    warmtevraagSWWf = warmtevraagSWW_J/3600000 #omzetting J naar kWh
     
    voorzieningSWW = huidigevoorziening.get('sanitair warm water')
    verbruikerSWW = huidigevoorziening.get('sanitair warm water').get('verbruiker')
    verbruikerRV = huidigevoorziening.get('ruimteverwarming').get('verbruiker')
    verbruikerElec = huidigevoorziening.get('elektriciteit').get('verbruiker')

    if verbruikerRV == verbruikerSWW:
        verbruikSWW  = warmtevraagSWWf/voorzieningSWW.get('efficientie')
        percSWW = verbruikSWW/verbruik.get(verbruikerSWW)
        verbruikRV = (1-percSWW)*verbruik.get(verbruikerSWW)
        verbruikDict = {"ruimteverwarming":verbruikRV,"sanitair warm water":verbruikSWW,"elektriciteit":verbruik.get("elektriciteit")}

    elif verbruikerSWW == verbruikerElec:  #is dus elektriciteit
        verbruikSWW = warmtevraagSWWf/voorzieningSWW.get('efficientie')
        percSWW = verbruikSWW/verbruik.get(verbruikerSWW)
        verbruikelec = (1-percSWW)*verbruik.get(verbruikerSWW)

        verbruikDict = {"ruimteverwarming":verbruik.get(verbruikerRV),"sanitair warm water":verbruikSWW,"elektriciteit":verbruikelec}

    else:
        print("error in verbruikverdeling")
    print(verbruikDict)

    return verbruikDict
"""
================================================================================
ENERGIEVRAAG BEPALEN
================================================================================
""" 

def energieVraag(efficientie,huidigVraagProfiel):
    """
    energievraag (nuttige energie) van huidige voorzieningen bepalen op basis van huidige efficientie
    """
    if type(huidigVraagProfiel) != list and type (efficientie) != list:
        vraag  = efficientie*huidigVraagProfiel
        
    elif type (efficientie) == list: #if functie is nodig om te bepalen of de efficientie tijdsafhankelijke is of niet, tijdsafhankelijk staat in een list, niet-afhankelijk is gwn een integer
        vraag = [a*b for a,b in zip(huidigVraagProfiel, efficientie )]

    else:
        vraag = [i*efficientie for i in huidigVraagProfiel]

    return vraag

def nieuwVerbruik(voorziening,oudverbruik,huidigVraagProfiel): #huidigVraagProfiel,COP,variableEff,aandeel,oudverbruik):
    """nieuw verbruik voor nieuwe voorziening op basis van het vraagprofiel, de nieuwe voorziening en al dan niet een variabele efficientie"""
    COP=voorziening.get("efficientie")
    variableEff=voorziening.get("varEff")
    aandeel = voorziening.get("aandeel")

    if aandeel != None:
            print('if AANDEEEEL')
            newdict = {}
            if variableEff != None:
                # print("efficientie",efficientie)
                eff = [a*COP for a in variableEff]
                # print(eff)
                verbruik = [(aandeel*a)/b for a,b in zip(huidigVraagProfiel, eff )]
                verbruikC = [(aandeel*i)/COP for i in huidigVraagProfiel]
       
            elif variableEff == None:
                verbruik = [(aandeel*i)/COP for i in huidigVraagProfiel]
                verbruikC = [(aandeel*i)/COP for i in huidigVraagProfiel]
            else:
                print("nieuw verbruik berekenen failed")

            for k,v in oudverbruik.items():
                newdict[k] = v*(1-aandeel)
            newdict[voorziening.get("verbruiker")] = sum(verbruik)
            print('----', newdict)
            return {"variabel":{"profiel":verbruik,"verbruik":newdict },"constant":{"profiel":verbruikC,"totaal":sum(verbruikC)}}

    elif aandeel == None:
            print('if GEEN AANDEEEEL')

            if variableEff != None:
                # print("efficientie",efficientie)
                eff = [a*COP for a in variableEff]
                # print(eff)
                verbruik = [a/b for a,b in zip(huidigVraagProfiel, eff )]
                verbruikC = [i/COP for i in huidigVraagProfiel]
            elif variableEff == None:
                        verbruik = [i/COP for i in huidigVraagProfiel]
                        verbruikC = [i/COP for i in huidigVraagProfiel]
            else:
                        print("nieuw verbruik berekenen failed")
            return {"variabel":{"profiel":verbruik,"verbruik":{voorziening.get("verbruiker"):sum(verbruik)}},"constant":{"profiel":verbruikC,"totaal":sum(verbruikC)}}
    
"""
================================================================================
CO2 & primaire energie 
================================================================================
"""
#https://www.energids.be/nl/vraag-antwoord/wat-houdt-een-ton-co2-precies-in/2141/

def co2(verbruik):
    """co2 uitstoot van een bepaald verbruik met verbruiker bepalen"""
    c = 0
    for key, value in verbruik.items():
        co2 = verbruikers.get(key).get("co2 per kwh")
        if co2 != None:
            c = c + value*co2 
        else:
            print("Nonetype error: verbruiker not in list verbruikers")  
    return c

def primaireE(verbruik):
    c= 0 
    """primaire energie uitstoot van een bepaald verbruik met verbruiker bepalen"""
#https://navigator.emis.vito.be/mijn-navigator?woId=53045 link van vlaamse overheid met andere waarden, gas en elec bijna hetzelfde 
# https://www.vlaanderen.be/epb-pedia/rekenmethode/rekenmethode-e-peil/karakteristiek-jaarlijks-primair-energieverbruik
    for key, value in verbruik.items():
        omzetting = verbruikers.get(key).get("omzetting prim energie")
        if omzetting != None:
            c = c+ value*omzetting 
        else:
            print("Nonetype error: verbruiker not in list verbruikers")
    return c

"""
================================================================================
FINANCIEEL
================================================================================
"""
def verbruikskost(verbruik):
    c = 0 
    for key, value in verbruik.items():
        kost = verbruikers.get(key).get("kost per kwh")
        if kost != None:
            c = c + value*kost 
        else:
            print("Nonetype error: verbruiker not in list verbruikers")
    return c

def totVerbruikskost(dict):
    a = {k:verbruikskost({k:v}) for k,v in dict.items()}
    tot = sum(a.values())
    return tot

def cashandpayback(oudverbruik, nieuwverbruik,investering):
    devOud = 0.05  #oude verbruikskost stijgt met 5% elk jaar
    devNieuw = 0.02 #nieuwe verbruikskost stijgt met 2% elk jaar
    cashflow = []
    kostHuidig = totVerbruikskost(oudverbruik) #initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
    kostNieuw = totVerbruikskost(nieuwverbruik)
    onderhoud = 100
    cashflow.append(-1*investering)
    while sum(cashflow) < 0:
        cashflow.append(kostHuidig - kostNieuw - onderhoud)
        kostHuidig = kostHuidig*(1+devOud)
        kostNieuw = kostNieuw*(1+devNieuw)
    print(cashflow)
    years = len(cashflow)
    return [cashflow, years]

def investering(nieuwlist):
    investList = []
    for v in nieuwlist.values():
        if v not in investList:
            investList.append(v)
        else:
            print("investering van",v.get('naam'),'is reeds meegeteld')

    invest = 0
    for dict in investList:
        a = dict.get('prijs')
        invest += a
    return invest

"""
================================================================================
DICTIONARY VAN HUIDIG PROFIEL GENEREREN
================================================================================
"""
def huidigProfiel(toepassingen,huidigevoorzieningen, huidigverbruik, slps):
    
    print("")
    print("#######################################")
    print("HUIDIG PROFIEL GENEREREN")
    print("#######################################")
    print("")
    
    dictVoorzieningen = {}  #list met een dict per toepassing. de dict bevat info over de voorziening en verbruik voor deze toepassing
    #dictVoorzienigen ziet eruit als volgt {"ruimteverwarming":{}, "elektriciteit":{},"sanitair warm water":{},...}
    
    for i in range(len(toepassingen)):  #voor elke toepassingen in de tool een dict maken met info over welke voorzieningen en het verbruik van deze voorziening
        # print("huidig profiel voor",toepassingen[i])
        newDict = {}
        voorziening = huidigevoorzieningen.get(toepassingen[i])  #selecteer de juiste voorziening die voor de toepassing zorgt 
        verbruiker = voorziening.get('verbruiker')  #welke soort verbruik heeft de toepassing
        verbruik = float(huidigverbruik.get(toepassingen[i]))  #totaal jaarverbruik van de specifieke verbruiker die deze toepassing verbruikt
        slp =  slps.get(toepassingen[i])  #slp die bij de bepaalde toepassing hoort
        print(toepassingen[i],verbruik)
        newDict['voorziening'] = voorziening
        newDict['totverbruik'] = {verbruiker:verbruik} #{verbruiker:sum(newDict.get('verbruikprofiel'))} #totaal verbruik dat de toepassing verbruikt op een jaar
        newDict['totvraag'] = energieVraag(voorziening.get('efficientie'),verbruik)  #per kwartier de vraag berekenen die de toepassing nodig heeft afhankelijk van de huidige efficientie, op basis hiervan kan het verbruik van de nieuwe voorziening met een nieuwe efficientie berekent worden 

        newDict['energievraag'] = verbruikProfiel(newDict.get('totvraag'),slp)  #verbruik dat de toepassing vraagt, per kwartier op een jaar

        update = {toepassingen[i]:newDict}
        dictVoorzieningen.update(update)
        noprint = ["energievraag"]
        resultset = [[key,value] for key, value in newDict.items() if key not in noprint]
        print('\n')
        print(resultset,'\n')

    huidigprofiel = {}
    huidigprofiel['dictVoorzieningen'] = dictVoorzieningen

    verbruikDict = {}
    for toepassing in toepassingen:
        dict = huidigprofiel.get('dictVoorzieningen').get(toepassing)
        verbruik = dict.get('totverbruik')
        for key,value in verbruik.items():
            if  key not in verbruikDict:
                verbruikDict[key] = value
            elif key in verbruikDict:
                oldVal = verbruikDict.get(key)
                newVal = oldVal + value
                update = {key:newVal}
                verbruikDict.update(update)

    huidigprofiel['verbruik'] = verbruikDict  #dictionary van elke verbruiker met een totaal jaarverbruik, zou gelijk moeten zijn aan wat er ingegeven is door de user       
    huidigprofiel['voorzieningen'] = {k:huidigprofiel.get('dictVoorzieningen').get(k).get('voorziening').get('naam') for k in huidigprofiel.get('dictVoorzieningen')}
    huidigprofiel['co2'] = co2(verbruikDict)
    huidigprofiel['primaire energie'] = primaireE(verbruikDict)
    huidigprofiel['totale verbruikskost'] = verbruikskost(verbruikDict) 
    
    print("")
    print("#######################################")
    print("VERBRUIK HUIDIGE SITUATIE - check gelijk aan input","\n", huidigprofiel.get('verbruik'))
    print("--------------------------------------")
    print("VERBRUIKkost HUIDIGE SITUATIE","\n", huidigprofiel.get('verbruikskost'))
    print("#######################################")
    print("")

    return huidigprofiel  # = {"dictvoorzieningen":{},"...":,}

"""
================================================================================
DICTIONARY VAN NIEUW PROFIEL GENEREREN
================================================================================
"""
def nieuwProfiel(toepassingen, scenario, huidigprof, PV,calcPV,index):
    print("")
    print("##################################################################################")
    print("NIEUW PROFIEL GENEREREN",scenario)

    dictVoorzieningen = {}

    nieuwevoorzienigen = {}
    for toepassing in toepassingen:
            nieuwevoorzienigen[toepassing] = nieuweVoorzieningen(scenario=scenario,toepassing=toepassing,huidigprof=huidigprof,index = index)
            print('+++++++++++++++++++++++++++++++++++++',toepassing,nieuwevoorzienigen.get((toepassing)).get('naam'))
    
    print("     NIEUWE VOORZIENINGEN zonder PV") if calcPV == False else print("     NIEUWE VOORZIENINGEN met PV")
    
    for i in range(len(toepassingen)):
        newDict = {}
        print("TOEPASSINNGGGG", toepassingen[i])
        if huidigprof.get("dictVoorzieningen").get(toepassingen[i]).get('voorziening').get('naam') == scenario.get(toepassingen[i]) and calcPV == False:
            update = {toepassingen[i]:huidigprof.get("dictVoorzieningen").get(toepassingen[i])}
            
            print("UPDATE")

            dictVoorzieningen.update(update) 

        else:
            print("TEST WELKE ELSE")   
            voorziening = nieuwevoorzienigen.get(toepassingen[i])
            energievraag = huidigprof.get('dictVoorzieningen').get(toepassingen[i]).get('energievraag') #if calcPV == False else huidigprof.get('dictVoorzieningen').get(toepassingen[i]).get('energievraag') - PV.get('size')
            newDict['voorziening'] = voorziening
            print(toepassingen[i],voorziening.get('naam'))
            nieuwCons = nieuwVerbruik(voorziening = voorziening,oudverbruik=huidigprof.get('dictVoorzieningen').get(toepassingen[i]).get('totverbruik'),huidigVraagProfiel = energievraag ) #energievraag,COP=voorziening.get("efficientie"),variableEff=voorziening.get("varEff"),aandeel = voorziening.get("aandeel"),oudverbruik=huidigprof.get('dictVoorzieningen').get(toepassingen[i]).get('totverbruik'))
            newDict['verbruik'] = nieuwCons.get("variabel")
            newDict['verbruikConstant'] = nieuwCons.get("constant")

            newDict['totverbruikConstant'] = nieuwCons.get('constant').get('totaal')
            newDict['totverbruik'] = newDict.get('verbruik').get('verbruik')

       
                    
            update = {toepassingen[i]:newDict}
            dictVoorzieningen.update(update)
            # print("verbruik per toepassing---------------------------------------:",toepassingen[i],"\n",
            #     "variabele COP", newDict.get("totverbruik"),"\n",
            #     "constante COP",newDict.get("totverbruikConstant")
            #     )

    nieuwprofiel = {}
    nieuwprofiel['nieuwevoorzieningen'] = nieuwevoorzienigen
    nieuwprofiel['dictVoorzieningen'] = dictVoorzieningen

    nieuwprofiel['PV'] = PV if calcPV == True else "Geen PV berekening"
    
    nieuwprofiel['voorzieningen'] = {k:nieuwprofiel.get('dictVoorzieningen').get(k).get('voorziening').get('naam') 
                                    + " " 
                                    + str(nieuwprofiel.get('dictVoorzieningen').get(k).get('voorziening').get('maxVermogen')) 
                                    + nieuwprofiel.get('dictVoorzieningen').get(k).get('voorziening').get('eenheid vermogen')  
                                    
                                    
                                    for k in nieuwprofiel.get('dictVoorzieningen')
                                    }
    verbruikDict = {}
    print(nieuwprofiel.get('voorzieningen'))

    print("     NIEUW VERBRUIK BEREKENEN")
   
    for i in range(len(toepassingen)):
        dict = nieuwprofiel.get('dictVoorzieningen').get(toepassingen[i])
        verbruik = dict.get('totverbruik')
        for key,value in verbruik.items():
            if  key not in verbruikDict:
                verbruikDict[key] = value
            elif key in verbruikDict:
                oldVal = verbruikDict.get(key)
                newVal = oldVal + value
                update = {key:newVal}
                verbruikDict.update(update)
    if calcPV == True and "elektriciteit" in verbruikDict.keys():
        a = {"elektriciteit":verbruikDict['elektriciteit'] - PV['size']}
        verbruikDict.update(a)

    [print("     NIEUW VERBRUIK: ","\n", key,':',value ,"\n") for key, value in verbruikDict.items()]
    

    nieuwprofiel['co2'] = co2(verbruikDict)
    nieuwprofiel['primaire energie'] = primaireE(verbruikDict)  
    nieuwprofiel['verbruik'] = verbruikDict  #dictionary van elke verbruiker met een totaal jaarverbruik, zou gelijk moeten zijn aan wat er ingegeven is door de user       
    nieuwprofiel['totale verbruikskost'] =  verbruikskost(verbruikDict)


    print("     INVESTERING & financieel BEREKENEN")

    nieuwprofiel['investering PV'] = 0 if calcPV == False else PV.get('price') 
    nieuwprofiel['investering'] = investering(nieuwevoorzienigen) + nieuwprofiel.get('investering PV')
    print("")
    print("VERBRUIK NIEUW PROFIEL","\n", nieuwprofiel.get('verbruik'))
    print("--------------------------------------")
    print("VERBRUIKSKOST nieuw profiel","\n", nieuwprofiel.get('totale verbruikskost'))
    print("--------------------------------------")
    print("investering nieuw profiel","\n", nieuwprofiel.get('investering'))
    print("##################################################################################")
    print("")
    
    return nieuwprofiel

"""
================================================================================
VERGELIJKING MAKEN TUSSEN DICT HUIDIG PROFIEL EN DICT NIEUW PROFIEL
================================================================================
"""
def verbruikvergelijking(dictH,dictN):
    comp = {}
    for k,v in dictH.items():
        if k not in dictN.keys():
            a = {k:v}
        elif k in dictN.keys():
            a = {k:v-dictN.get(k)}
        comp.update(a)
    return comp

def profileComparison(huidProf, nieuwProf):
   vergelijking = {} 
   vergelijking['PV'] = nieuwProf.get('PV')
#    print(nieuwProf.get('primaire energie'))
#    print(nieuwProf.get('co2'))

   vergelijking["besparing primaire energie"] = huidProf.get('primaire energie') - nieuwProf.get('primaire energie')
   vergelijking["besparing primaire energie perc"] =(vergelijking.get('besparing primaire energie')/huidProf.get('primaire energie'))*100
   
   vergelijking["CO2 besparing"] = huidProf.get('co2') - nieuwProf.get('co2')
   vergelijking["CO2 besparing perc"] = (vergelijking.get("CO2 besparing")/huidProf.get('co2'))*100
   
   vergelijking["besparing verbruik"] = verbruikvergelijking(huidProf.get('verbruik'),nieuwProf.get('verbruik'))
   print("besparing",vergelijking.get("besparing verbruik"))
   vergelijking["verbruikskostbesparing"] = {k:verbruikskost({k:v}) for k,v in vergelijking.get('besparing verbruik').items()}
   vergelijking["totale kostbesparing"] = sum(vergelijking.get('verbruikskostbesparing').values())
   vergelijking["totale kostbesparing perc"] = (vergelijking.get("totale kostbesparing")/huidProf.get('totale verbruikskost'))*100

   cashflow = cashandpayback(huidProf.get('verbruik'),nieuwProf.get('verbruik'),nieuwProf.get('investering'))

   vergelijking['cashflow'] = cashflow[0]
   vergelijking['tvt'] = cashflow[1]

   return vergelijking

'''
================================================================================
VERGELIJKING MET ALLE SCENARIOS OPROEPEN
================================================================================
'''
def callComparison(listScenarios, profiel,PV,nieuweProfiel): 
    print('----------------------------------------------------------------------------')
    comp = []
    dict1 = {}
    dict2 = {}
    print("=== vergelijking nieuwprofiel met huidig profiel voor:",listScenarios.get('scenario'),listScenarios.get('ruimteverwarming'),listScenarios.get('sanitair warm water'),listScenarios.get('elektriciteit'),'===')
    print("")
    vgl = profileComparison(profiel,nieuweProfiel[0])
    print(vgl)
    vgl['scenario'] = listScenarios.get('scenario')
    dict1['profiel'] = nieuweProfiel[0]
    dict1['vgl'] = vgl
    comp.append(dict1)

    if PV.get('PV') == True:
            print('----------------------------------------------------------------------------')
            print("=== vergelijking nieuwprofiel met huidig profiel voor:",listScenarios.get('scenario'),listScenarios.get('ruimteverwarming'),'met PV ===')
            print("")
            vglPV = profileComparison(profiel,nieuweProfiel[1])
            print(vglPV)
            vglPV['scenario'] = listScenarios.get('scenario')
            dict2['profiel']=nieuweProfiel[1]
            dict2['vgl'] = vglPV
            comp.append(dict2)
    return comp   #structuur 1 comp = [{profiel: {}, vgl: {}},{profielPV: {}, vglPV: {}}]


"""
================================================================================
code oproepen
================================================================================
"""

def main(toepass,huidigeVoorzieningen,huidigverbruik,scenariosList,updateverbruikers,PV,inwoners,COPindex):
    #data in verbruikers update (persoonlijke kostprijs per kwh bijvoorbeeld)
    for k,v in updateverbruikers.items():
        verbruikers.get(k).update(v)
    
    #sanitair warm water in het scenario met LL warmtepomp updaten naar welke installatie er nu aanwezig is (gas of stookolieketel)
    scenariosList[2].update({"sanitair warm water":huidigeVoorzieningen.get('sanitair warm water').get('naam')})

    #het verbruik verdelen over de verschillende toepassingen
    verbruikdiv = verbruikverdeling(verbruik = huidigverbruik, pers = inwoners,huidigevoorziening=huidigeVoorzieningen) #
    print("")
    print("#######################################")
    print("VERBRUIKVERDELING", verbruikdiv)
    print("#######################################")
    print("")

    #huidig profiel maken
    huidigProf = huidigProfiel(toepassingen = toepass, huidigevoorzieningen=huidigeVoorzieningen,slps=SLPs,huidigverbruik=verbruikdiv)
    
    print("")

    print("#######################################")
    print("NIEUWE PROFIELEN GENEREREN")
    print("#######################################")
    print("")

    #lijst  van nieuwe profielen op basis van de nieuwe scenarios 
    nieuweProfielList = []
    for i in range (len(scenariosList)): #elk scenario in de lijst  van scenarios doorlopen, een nieuw profiel maken en dit nieuw profiel vergelijken met het huidige profiel en de vergelijking opslaan in een list 
        list = []    
        nieuwProf = nieuwProfiel(toepassingen = toepass,scenario = scenariosList[i],huidigprof= huidigProf,calcPV = False,PV=PV,index=COPindex)
        list.append(nieuwProf)
        if PV.get('PV') == True:
            nieuwProfPV = nieuwProfiel(toepassingen = toepass,scenario = scenariosList[i],huidigprof= huidigProf,calcPV = True,PV=PV,index=COPindex)
            list.append(nieuwProfPV)
            nieuweProfielList.append(list)
    print("")
    print("#######################################")
    print("NIEUWE PROFIELEN MET HUIDIGE VERGELIJKEN")
    print("#######################################")
    print("")
    #lijst  van vergelijkingen tussen huidig profiel en nieuwe profielen
    listVGL = []
    for i in range (len(nieuweProfielList)): #elk scenario in de lijst  van scenarios doorlopen, een nieuw profiel maken en dit nieuw profiel vergelijken met het huidige profiel en de vergelijking opslaan in een list 
        comparison = callComparison(listScenarios = scenariosList[i],profiel= huidigProf,PV=PV,nieuweProfiel=nieuweProfielList[i])
        listVGL.append(comparison) #[comp1, comp2, comp3...]

    #lijst sorteren op meeste CO2 besparing in scenario zonder PV
    sortedList = sorted(listVGL, key=lambda i: (i[0].get('vgl').get('CO2 besparing perc'),i[0].get('vgl').get('besparing primaire energie perc'),-i[0].get('vgl').get('totale kostbesparing perc')),reverse=True)
    #als de co2 besparing <0 dan voegen we het scenario niet toe aan de lijst
    sortedList = [scen for scen in sortedList if scen[0].get('vgl').get('CO2 besparing perc') > 0 ]
    
    #data voor de grafieken apart verzamelen
    graph_data = []
    for i in range(len(sortedList)):
        vgl = sortedList[i][0].get('vgl')
        data = {}
        data['profiel'] = sortedList[i][0].get('profiel').get('voorzieningen')
        data.get('profiel')["nr"] = i+1
        data['co2abs'] = round(vgl.get('CO2 besparing'))
        data["co2"] = round(vgl.get('CO2 besparing perc'))
        data["primaire"] = round(vgl.get("besparing primaire energie"))
        data["primaireP"] = round(vgl.get("besparing primaire energie perc"))
        data["kostP"] = round(vgl.get("totale kostbesparing perc"))
        data["kost"] = round(vgl.get("totale kostbesparing"))
        data['investering'] = sortedList[i][0].get('profiel').get('investering')

        graph_data.append(data)
        print("xxxxx", graph_data)
    
    for i in range(len(sortedList)):
        vgl = sortedList[i][0].get('vgl')
        data = {}
        data['profiel'] = sortedList[i][0].get('profiel').get('voorzieningen')
        data.get('profiel')["nr"] = i+1
        data['co2abs kg CO2'] = round(vgl.get('CO2 besparing'))
        data["co2 %"] = round(vgl.get('CO2 besparing perc'))
        data["primaire kWh"] = round(vgl.get("besparing primaire energie"))
        data["primaireP %"] = round(vgl.get("besparing primaire energie perc"))
        data["kostP %"] = round(vgl.get("totale kostbesparing perc"))
        data["kost €"] = round(vgl.get("totale kostbesparing"))
        data["tvt [jaar]"] = (vgl.get("tvt"))
        
        print("")
        print("*")
        print("*")
        print("RESULTATEN TESTSCENARIO")
        print("resultaten - scenario",i+1)
        for key, value in data.items():
            print(key, value)

    return  [sortedList,huidigProf,graph_data]

"""
=== TESTFUNCTIE ===
"""
"""Deze functie dient om deze code te runnen zonder heel de webpagina te openen"""
# huidig = {"ruimteverwarming":andere.get("Gasketel"),"sanitair warm water":andere.get("Gasketel"),"elektriciteit":andere.get("elektriciteitsnet")}
# cons = {"aardgas":20000,"stookolie":50000,"elektriciteit":4000}
# kos = {"aardgas":{"kost per kwh":0.14},"elektriciteit":{"kost per kwh":0.5},"stookolie":{"kost per kwh":0.08}}
# testfunct = main(toepass=toepassingen,huidigeVoorzieningen=huidig,huidigverbruik=cons,scenariosList=scenarios,updateverbruikers=kos,PV={'PV':True,'size':3500,'price':5000},inwoners=4,COPindex=(1,0))


"""========================================"""

#een pdf maken uit html template van elk scenario en opslaan in een lijst
#alle pdf's daarna samenvoegen 
def generatePDF(list,huid):
    print("=== generating PDF ===") 
    merger = PdfMerger()
    huidig = huid #session.get('huidig profiel')
    dict1 = huidig.get('voorzieningen')
    dict2 = {k:round(huidig.get('verbruik').get(k)) for k in huidig.get('verbruik')}


    firstPageVar = {
        "dict1":dict1,"dict2":dict2,
        "var1":round(huidig.get('totale verbruikskost')),
        "var2":round(huidig.get('primaire energie')),
        "var3":round(huidig.get('co2')),
        # "chart_values":chart_data
                    }
    huidig_pdf = render_template("pdfHuidigeSituatie.html", **firstPageVar)
    generated_pdfhuidig = HTML(string=huidig_pdf).write_pdf()
    pdf_file_like = BytesIO(generated_pdfhuidig)
    merger.append(pdf_file_like)


    for comp in list:
        print("newcomp")
        co2 = [round(huidig.get('co2'))]
        kost = [round(huidig.get('totale verbruikskost'))]
        primE = [round(huidig.get('primaire energie'))]
        for dict in comp:
            new = dict.get('profiel')
            vgl = dict.get('vgl')
            
           
            dict1 = new.get('voorzieningen')
            dict2 = {k:round(new.get('verbruik').get(k)) for k in new.get('verbruik')}
            dict3 = {k:-1*round(vgl.get('besparing verbruik').get(k)) for k in vgl.get('besparing verbruik')}
            number = list.index(comp) + 1 
            print(dict1)
                       
            var = {
                "name": new.get('voorzieningen').get('ruimteverwarming'),
                "number":number, 
                "dict1":dict1,
                "dict2":dict2,
                "dict3":dict3,
                "var1":round(new.get('totale verbruikskost')),
                "var2":round(new.get('primaire energie')),
                "var3":round(new.get('co2')),
                "var4":round(vgl.get("totale kostbesparing")),
                "var5":round(vgl.get("besparing primaire energie perc")),
                "var6":round(vgl.get("CO2 besparing perc")),
                "var7":round(new.get("investering")),
                "var8":str(str(str(vgl.get('tvt')) + " jaar"))
            }
            co2.append(round(new.get('co2')))
            kost.append(round(new.get('totale verbruikskost')))
            primE.append(round(new.get('primaire energie')))

            template = 'pdfNieuwScenario.html' if type(vgl.get('PV')) == str else 'pdfNieuwScenarioMetPV.html'

            nieuw_pdf = render_template(template, **var)
            generated_pdfnieuw = HTML(string=nieuw_pdf).write_pdf()
            pdf_file_like1 = BytesIO(generated_pdfnieuw)
            merger.append(pdf_file_like1)

        fig = chartimg(co2,kost,primE)
        merger.append(BytesIO(fig))

    pdfpath = os.path.join("static","pdf_files")
    frontpage = open(os.path.join(pdfpath,"Voorzijde.pdf"),"rb")
    voorwoord = open(os.path.join(pdfpath,"Voorwoord.pdf"),"rb")
    aannames = open(os.path.join(pdfpath,"Aannames.pdf"),"rb")
    lastpage = open(os.path.join(pdfpath,"Achterzijde.pdf"),"rb")
    merger.merge(page_number= 0, fileobj = frontpage)
    merger.merge(page_number= 1, fileobj = voorwoord)
    merger.append(aannames)
    merger.append(lastpage)
    
    # create the output file
    with open("merged.pdf", "wb") as f:
        merger.write(f)
    merger.close()
    
    file = "merged.pdf"
    done = True
    return [file, done]

from matplotlib import pyplot as plt
import numpy as np

def chartimg(co2,kost,prim):
    a = len(co2)  #check of pv wordt meegerekend of niet
   
    x1 = np.array(["Huidig", "Nieuw", "Nieuw met PV"]) if a == 3 else np.array(["Huidig", "Nieuw"])
    y1 = np.array(co2)
    y2 = np.array(kost)
    y3 = np.array(prim)

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(8.27, 11.69))

    # Plot the data on each subplot
    colors = [(0.107, 0.180, 0.186, 0.776),(0.107, 0.180, 0.186, 0.776),(0.107, 0.180, 0.186, 0.776)] if a == 3 else [(0.107, 0.180, 0.186, 0.776),(0.107, 0.180, 0.186, 0.776)]

    ax1.barh(x1, y1,color = colors)
    ax1.set_title('CO2 uitstoot')
    ax1.set_xlabel('Kg co2 per jaar')

    ax2.barh(x1, y2,color = colors)
    ax2.set_title('Verbruikskost')
    ax2.set_xlabel('€ per jaar')

    ax3.barh(x1, y3,color = colors)
    ax3.set_title('Primaire energie')
    ax3.set_xlabel('kWh per jaar')
    fig.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='pdf')
    pdf = buffer.getvalue()
    buffer.close()

    return pdf






