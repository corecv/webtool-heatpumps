from flask_wtf import FlaskForm
from wtforms import IntegerField,RadioField, FloatField
from wtforms.validators import InputRequired, NumberRange
from data import RVinput, SWWinput

"""=== generate inputs voor meerdere forms"""
"""Hieronder staat de declaratie van inputs die in meerdere forms gebruikt worden, elk field wordt gemaakt via een functie die het field genereert"""
def elecVoorziening():
    elec = RadioField('Heeft u reeds zonnepanelen?',choices=["Ja","Nee"],validators=[InputRequired()])
    return elec


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

class ConsumptionForm(FlaskForm):

    pass

class ConsumptionFormA(FlaskForm):
    aardgas  = FloatField('Geef uw jaarverbruik aan aardgas in kWh',default = 20000)
    aardgasC  = FloatField('Geef uw prijs (in €) per kWh in voor aardgas',default = 0.1)
    elec  = FloatField('Geef uw jaarverbruik aan elektriciteit in kWh',default = 3500)
    elecC  = FloatField('Geef uw prijs (in €) per kWh in voor elektriciteit',default = 0.4) 
    sizePV = FloatField("Geef de grootte van uw zonnepaneel installatie in in kWh",default = 3500)
    pricePV = FloatField('Geef de kost van de zonnepaneel installatie in [€]',default = 4500) 
    stookolie  = FloatField('Geef uw jaarverbruik aan stookolie in L in [Liter]',default = 2000) 
    stookolieC  = FloatField('Geef uw prijs (in €) per L in voor stookolie [€/L]',default = 0.0008) 



   
