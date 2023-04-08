from flask import Flask, render_template, redirect, url_for, request, session, send_file
from forms import*
from appCopy import main, generatePDF, scenarioSelection
from data import toepassingen, RVinput,SWWinput,combiInput,Elecinput,scenarios,verbruikers
import json
import threading



app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = 'geheime tekst'


@app.route('/', methods=('GET', 'POST'))
def start():

    return render_template('start.html')

# def userInputs():
#     form = FormOne()

#     if form.validate_on_submit():
        
#         if form.combi.data == "yes":
            
#             return redirect(url_for('formTwoA'))

#         elif form.combi.data == "no": 

#             return redirect(url_for('formTwoB'))

#     return render_template('formOne.html', form=form,calculations_finished = False)

@app.route("/gegevens", methods=('GET', 'POST'))
def gegevens():
    form = Gegevens()

    if form.validate_on_submit():
        variables = {"isolatie":form.isolatie.data,"afgifte":form.afgifte.data,"inwoners":form.size.data}
        session["variables"] = variables
        
        if form.combi.data == "Ja":
            
            return redirect(url_for('formTwoA'))

        elif form.combi.data == "Nee": 

            return redirect(url_for('formTwoB'))


    return render_template('gegevens.html',form=form)

@app.route("/formTwoA", methods=('GET', 'POST'))
def formTwoA(): 
    form = FormTwoA()
    if form.validate_on_submit():
        selected1 = form.rvsww.data
        RVdict = next((d for d in combiInput if d["naam"]==selected1),None)
        SWWdict = RVdict
        selected2 = form.elec.data
        elec = Elecinput[0] #hier kan de optie komen om pv mee te rekenen of niet
        elec.update({"PV":selected2})
        huidigevoorzieningen = {"ruimteverwarming":RVdict,"sanitair warm water":SWWdict,"elektriciteit":elec}
  
        session["huidige voorzieningen"] = huidigevoorzieningen
        energy_sources = []
        for v in huidigevoorzieningen.values():
            if v.get('verbruiker') in energy_sources or v == 'csrf_token':
                continue
            else:
                energy_sources.append(verbruikers.get(v.get('verbruiker')))
        session['verbruikers'] = energy_sources

            
        if energy_sources:
            # redirect to the consumption form
            return redirect(url_for('consumption'))

    return render_template('formTwoA.html',form=form)


@app.route("/formTwoB", methods=('GET', 'POST'))
def formTwoB(): 
    form = FormTwoB()
    if form.validate_on_submit():
        selected1 = form.voorzieningRV.data
        RVdict = next((d for d in RVinput if d["naam"]==selected1),None)
        selected2 = form.voorzieningSWW.data
        SWWdict = next((d for d in SWWinput if d["naam"]==selected2),None)
        selected3 = form.elec.data
        elec = next((d for d in Elecinput if d["naam"]==selected3),None) #hier kan de optie komen om pv mee te rekenen of niet
        huidigevoorzieningen = {"ruimteverwarming":RVdict,"sanitair warm water":SWWdict,"elektriciteit":elec}
        session["huidige voorzieningen"] = huidigevoorzieningen
                
        energy_sources = []
        for v in huidigevoorzieningen.values():
            if v.get('verbruiker') in energy_sources:
                continue
            else:
                energy_sources.append(v.get('verbruiker'))

        session['verbruikers'] = energy_sources

        if energy_sources:
            # redirect to the consumption form
            return redirect(url_for('consumption'))

    return render_template('formTwoB.html',form=form)

@app.route('/consumption', methods=['GET', 'POST'])
def consumption():
  
    energy_sources = session.get('verbruikers')
    
    for source in energy_sources:
        name = source.get('naam')
        eenheid = source.get('eenheid')
        setattr(ConsumptionForm, f'{name}_consumption', FloatField(f'Geef uw jaarverbruik aan {name} in [{eenheid}]',validators=[InputRequired()],description= f'{name}'))
        setattr(ConsumptionForm, f'{name}_prijs', FloatField(f'Geef uw prijs (in €) per {eenheid} in voor {name}',validators=[InputRequired()]))
    if session.get("huidige voorzieningen").get('elektriciteit').get('PV') == False:
        setattr(ConsumptionForm, 'sizePV', FloatField('kWh van pv installatie',validators=[InputRequired()],default = 3500,description= "Zonnepanelen: zie uitleg"))
        setattr(ConsumptionForm, 'pricePV', FloatField('kost pv installatie',validators=[InputRequired()],default = 4500))

    form = ConsumptionForm(request.form)
    
    if request.method == 'POST' and form.validate():
        # create a dictionary from the form data
        verbruik = {}
        kost = {}
        # verbruik = {source: getattr(form, source + '_consumption').data for source in energy_sources}
        # kost = {source: {"kost per kwh":getattr(form, source + '_prijs').data} for source in energy_sources}
        for source in energy_sources:
            s = source.get('naam')
            verbruik[s] = getattr(form, s + '_consumption').data
            kost[s] = {"kost per kwh":getattr(form, s + '_prijs').data}
        session['verbruik'] = verbruik
        session['kost'] = kost
        
        if session.get("huidige voorzieningen").get('elektriciteit').get('PV') == True:
            session['PV'] = {'PV':False,'size':0,'price':0}
            return redirect(url_for('calculate'))
        
        elif session.get("huidige voorzieningen").get('elektriciteit').get('PV') == False:
            session['PV'] = {'PV':True,'size':form.sizePV.data,'price':form.pricePV.data}
            return redirect(url_for('calculate'))

    return render_template('consumption_form.html', form=form, PV=session.get("huidige voorzieningen").get('elektriciteit').get('PV'))
    

# @app.route("/formFourA", methods=['GET', 'POST'])
# def formFourA():
#     form = FormFourA()
#     if form.validate_on_submit():
#         solarboiler = {'size':form.sizeB.data,'price':form.priceB.data}
#         session['PV'] = {'PV':False,'size':0,'price':0}
    
        
#         return redirect(url_for('calculate'))

#     return render_template('formFour.html',form = form, PV = True)

# @app.route("/formFourB", methods=['GET', 'POST'])
# def formFourB():    
#     form = FormFourB()
#     if form.validate_on_submit():
#         solarboiler = {'size':form.sizeB.data,'price':form.priceB.data}
#         session['PV'] = {'PV':True,'size':form.sizePV.data,'price':form.pricePV.data}
    
#         return redirect(url_for('calculate'))

#     return render_template('formFour.html',form = form, PV = False)

@app.route("/generate_pdf")
def generate_pdf():
        # Start the calculation in a new thread
    t = threading.Thread(target=calculate)
    t.start()

    # Redirect to the waiting page
    return redirect(url_for("results"))

@app.route("/waiting")
def waiting():
    return render_template('waiting.html')


@app.route("/calculate")
def calculate():
    variables = session.get('variables')
    i = variables.get('isolatie')
    a = variables.get('afgifte')
    if i == "Goed geisoleerd" and a == "Vloerverwarming":
        crit = "Q1"
    elif i == "Goed geisoleerd" and a == "Radiatoren":
        crit = "Q2"
    elif i == "Matig geisoleerd" and a == "Vloerverwarming":
        crit = "Q3"
    elif i == "Matig geisoleerd" and a == "Radiatoren":
        crit = "Q2"
    else:
        crit = "Q4"
    print("criteria",crit)
    scenariosf = scenarios
    # scenariosf = scenarioSelection(scenariolist=scenarios,crit = crit)

    

    calc = main(toepass=toepassingen,huidigeVoorzieningen=session.get('huidige voorzieningen'),huidigverbruik=session.get('verbruik'),scenariosList=scenariosf,updateverbruikers=session.get("kost"),PV=session.get('PV'),inwoners=session.get("variables").get("inwoners"))
    print("sessie!", session.get('PV'))
    pdf = generatePDF(calc[0],calc[1])
    session['file'] = pdf[0]
    session['graph'] = calc[2]
    if pdf[1] == True:
        return redirect(url_for("results"))


@app.route('/results')
def results():
    labels = ['CO2', 'Primaire energie', 'Verbruiksost']
    # num_datasets = []
    data = []
    table = []
    dict = session.get('graph')
    for i in range(len(dict)):
        tabled = {"scenario":f'Scenario {i+1}',"voorziening":dict[i].get('profiel').get('ruimteverwarming'),"CO2abs":dict[i].get('co2abs'),"CO2perc":dict[i].get('co2'),"prim":dict[i].get('primaire'),"primP":dict[i].get('primaireP'),'kost':dict[i].get('kost'),'kostP':dict[i].get('kostP')}
        dataset = {
            'label': f'Scenario {i+1}',
            'data': [dict[i].get('co2'),dict[i].get('primaireP'),dict[i].get('kostP')],
            'backgroundColor': f'rgba({i*50}, {i*100}, {i*150}, 0.2)',
            'borderColor': f'rgba({i*50}, {i*100}, {i*150}, 1)',
            'borderWidth': 1,
            'stack': i-1 
        }
        data.append(dataset)
        table.append(tabled)

 
    
    # table = [dict.get('profiel') for dict in session.get('graph')]
            
    # for i in range(len(num_datasets)):
    #     dataset = {
    #         'label': f'Scenario {i+1}',
    #         'data': [num_datasets[i][0],num_datasets[i][1],num_datasets[i][2]],
    #         'backgroundColor': f'rgba({i*50}, {i*100}, {i*150}, 0.2)',
    #         'borderColor': f'rgba({i*50}, {i*100}, {i*150}, 1)',
    #         'borderWidth': 1,
    #         'stack': i-1 
    #     }
    #     data.append(dataset)

    
  

    return render_template('results.html', labels = labels, datasets=data,table=table)


@app.route('/download')
def sendFile():
    pdf = session.get('file')
    with open(pdf,'r'):     
        try:
            return send_file(pdf ) #, as_attachment=True)
        except Exception as e:
            return str(e)


if __name__=='__main__':
    app.run(debug=True, host = "0.0.0.0")

