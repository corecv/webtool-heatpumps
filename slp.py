import pandas as pd
import os
import matplotlib.pyplot as plt 
import csv 

def insertCSV(filename):
    
    csv = str(filename)
    path = os.getcwd()
    pathcsv = os.path.join(path, csv)
    data = pd.read_csv(os.path.join(path, csv))
    return data

filename="overzichtSLPs.csv"
data = insertCSV(filename)

timeValues = data.iloc[:,0]
SLPel = data.iloc[:,6] #profiel van de VREG
SLPg = data.iloc[:,10] #profiel van de VREG
# COP = data.iloc[:,8].tolist() #nu is er de mogelijkheid om de COP variabel te maken, op dit moment nog steeds een constante waarde in de csv, uiteindelijk zou dit ook een profiel per kwartier moeten worden van percentages. hiermee kan dan de COP van een elke warmtepomp vermenigvuldigt worden om een variable factor mee te rekenen 
elecEff = data.iloc[:,9]
datapoints = len(SLPg)
# print(datapoints)

def generateSLP(SLPgas):
#de SLPs voor ruimteverwarming, sanitair genereren op basis van het SLPg van de VREG
#het onderscheid maken tussen de profielen voor ruimteverwarming, sanitair ww en electriciteit
    min_gas = min(SLPgas) #minimum van het gasprofiel = waarde voor sanitair ww 
    SLPsww =[min_gas]*len(SLPgas) #SLP voor sanitair ww genereren, de constante waarde (min van gasprofiel) voor elk kwartier. To do: variatie in het profiel brengen, is meer realistisch dan altijd eenzelfde waarde
    SLPrv = [SLPgas[i]-SLPsww[i] for i in range(len(SLPgas))] #SLP voor ruimteverwarming genereren door de waarde voor SWW af te trekken van het totaal profiel voor gas

    return [SLPsww, SLPrv]



def listToCsv(file,list):
    with open(file,'w', newline="") as f:
        csv_writer = csv.writer(f)
        for row in list:
            csv_writer.writerow([row])
    return

def genCOP(length):
    COP = [None]*length  #lijst met cop 1 maken (voor elk kwartier dezelfde waarde)
    print(len(COP))
    basevalue = 1
    for index in range(len(COP)):
        if index <= 7800:  #1 jan tot 20 maart
            COP[index] = basevalue*0.8
        elif index > 7800 and index <= 16560:  #21 maart tot 20 juni
            COP[index] = basevalue*1
        elif index > 16560 and index <=25320: #21 juni tot 20 sept
            COP[index] = basevalue*1.2
        elif index > 25320 and index <= 34080: #21 sept tot 20 dec
            COP[index] = basevalue*1
        elif index > 34080:  #21 dec tot 1 jan
            COP[index] = basevalue*0.8
    return COP




def plotslp(slp,x,y):
    plt.plot(slp)
    plt.ylabel(x)
    plt.xlabel(y)
    plt.show()
    return


"+++ maak slp voor een variable COP +++"
COP = genCOP(datapoints)
print(len(COP))
print(COP)
listToCsv("slp_files\cop1.csv",COP)
plotslp(COP,"timevalue","percent")
"+++ maak slp voor een variable COP +++"
"+++ maak slp voor RV en SWW +++"
RvSWW = generateSLP(SLPg)
SLPrv = RvSWW[1]
SLPsww = RvSWW[0]
#print(COP)
listToCsv("slp_files\slprv.csv",SLPrv)
listToCsv("slp_files\slpsww.csv",SLPsww)

"+++ maak slp voor een variable COP +++"
# file = open('slp_files\cop1.txt','w')
# for value in COP:
#     file.write(str(value)+"\n")

# file.close()




