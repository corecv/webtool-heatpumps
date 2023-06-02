from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, IntegerField, BooleanField,RadioField, SelectField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange
from data import RVinput, SWWinput, Elecinput, combiInput



"""=== generate inputs voor meerdere forms"""
"""Hieronder staat de declaratie van inputs die in meerdere forms gebruikt worden, elk field wordt gemaakt via een functie die het field genereert"""
def elecVoorziening():
    elec = RadioField('Heeft u reeds zonnepanelen?',choices=["Ja","Nee"],validators=[InputRequired()])
    return elec

def jaarverbruikElec():
    electriciteit = FloatField('Jaarverbruik electriciteit',validators=[InputRequired()],default = 3500)
    return electriciteit
def costElec():
    costElec = FloatField('Kost per kWh electriciteit',validators=[InputRequired()],default = 0.3)
    return costElec
def jaarverbruikAardgas():
    aardgas = FloatField('Jaarverbruik aardgas',validators=[InputRequired()],default = 20000)
    return aardgas

def costAardgas():
    costAardgas = FloatField('Kost per kWh aardgas',validators=[InputRequired()],default = 0.5)
    return costAardgas

def jaarverbruikStookolie(): 
    stookolie = FloatField('Jaarverbruik stookolie',validators=[InputRequired()],default = 0)
    return stookolie

def costStookolie():
    costStookolie = FloatField('Kost per kWh stookolie',validators=[InputRequired()],default = 0.5)
    return costStookolie

def pvData():
    sizePV = FloatField('kWh van PV-installatie',validators=[InputRequired()],default = 3500)
    return sizePV

def solarBoilerdata():
    sizeB = FloatField('kWh van zonne-boiler installatie',validators=[InputRequired()],default = 2500)
    return sizeB


def pricePV():
    pricePV = FloatField('Kost PV-installatie',validators=[InputRequired()],default = 4500)
    return pricePV


def priceBoiler():  
    prijsBoiler = FloatField('kost zonneboiler installatie',validators=[InputRequired()],default = 5000)
    return prijsBoiler




"""===eerste stap"""

class FormOne(FlaskForm):
    combi = RadioField('Heeft u een combisysteem voor verwarming en sanitair warm water?',choices=["yes","no"],validators=[InputRequired()])


"""Gegevens"""
class Gegevens(FlaskForm):
    size = IntegerField("Huidige gezinsgrootte:",validators=[InputRequired(),NumberRange(min=0,message="Value must be higher than 0")])
    isolatie = RadioField("Type isolatie:",choices =["Goed geisoleerd","Matig geisoleerd","Slecht geisoleerd"] ,validators=[InputRequired()])
    afgifte = RadioField("Type verwarming:",choices =["Vloerverwarming","Radiatoren"] ,validators=[InputRequired()])
    combi = RadioField('Heeft u een combisysteem voor verwarming en sanitair warm water?',choices=["Ja","Nee"],validators=[InputRequired()])

"""===tweede stap"""
class FormTwoA(FlaskForm):
    rvsww = RadioField(label = 'Welke voorziening heeft u voor ruimteverwarming en sanitair warm water?', choices=[(d["naam"],d["naam"]) for d in RVinput], validators=[InputRequired()])
    # sww = RadioField(label ='Welke voorziening heeft u voor sanitair warm water?', choices=[(a["naam"],a["naam"]) for a in SWWinput], validators=[InputRequired()])
    elec = elecVoorziening()

class FormTwoB(FlaskForm):
    rvsww = RadioField(label ='Welke voorziening heeft u voor ruimteverwarming?', choices=[(a["naam"],a["naam"]) for a in RVinput], validators=[InputRequired()])
    sww = RadioField(label ='Welke voorziening heeft u voor sanitair warm water?', choices=[(a["naam"],a["naam"]) for a in SWWinput], validators=[InputRequired()])
    elec = elecVoorziening()



"""===derde stap==="""
# class FormThreeA(FlaskForm):
#     aardgas = jaarverbruikAardgas()
#     costAardgas = costAardgas()
#     electriciteit = jaarverbruikElec()
#     costElec = costElec()
    
# class FormThreeB(FlaskForm):
#     stookolie = jaarverbruikStookolie()
#     costStookolie = costStookolie()
#     electriciteit = jaarverbruikElec()
#     costElec = costElec()


class ConsumptionForm(FlaskForm):
    

    pass


# "===vierde stap==="

# class FormFourA(FlaskForm):
#     sizeB = solarBoilerdata()
#     priceB = priceBoiler()
    
    
# class FormFourB(FlaskForm):
#     sizeB = solarBoilerdata()
#     priceB = priceBoiler()
#     sizePV = pvData()
#     pricePV = pricePV()

   
