from flask import Flask, render_template, redirect, url_for, session, send_file
from forms import*
from appCopy import main, generatePDF
from data import toepassingen, RVinput,SWWinput,combiInput,Elecinput,scenarios,verbruikers
import threading




app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
# cache = Cache(app)
app.config['SECRET_KEY'] = 'geheime tekst'
# app.config['CACHE_TYPE'] = 'simple'


@app.route('/', methods=('GET', 'POST'))
def start():

    return render_template('start.html')


@app.route("/gegevens", methods=('GET', 'POST'))
def gegevens():
    form = Gegevens()

    if form.validate_on_submit():
        variables = {"isolatie":form.isolatie.data,"afgifte":form.afgifte.data,"inwoners":form.size.data,"combisysteem":form.combi.data}
        session["variables"] = variables
        # session["combi"] = form.combi.data
        
        # if form.combi.data == "Ja":
            
        #     return redirect(url_for('formTwoA'))

        # elif form.combi.data == "Nee": 

        return redirect(url_for('formTwoA'))


    return render_template('gegevens.html',form=form)

@app.route("/formTwoA", methods=('GET', 'POST'))
def formTwoA(): 
    combi = session['variables']['combisysteem']
    form = FormTwoA() if combi =='Ja' else FormTwoB()
    cont = False

    if form.validate_on_submit():
        selected1 = form.rvsww.data
        RVdict = next((d for d in combiInput if d["naam"]==selected1),None)
        
        selected2 = form.elec.data
        elec = Elecinput[0] #hier kan de optie komen om pv mee te rekenen of niet
        elec.update({"PV":selected2})
        
        if combi == "Nee":
            selected3  = form.sww.data
            SWWdict = next((d for d in SWWinput if d["naam"]==selected3),None)
        
        else:
            SWWdict = RVdict

        huidigevoorzieningen = {}
        huidigevoorzieningen["ruimteverwarming"] = RVdict
        huidigevoorzieningen["sanitair warm water"] = SWWdict
        huidigevoorzieningen["elektriciteit"] = elec
        session["huidige voorzieningen"] = huidigevoorzieningen
        energy_sources = []
        for v in huidigevoorzieningen.values():
            if v.get('verbruiker') in energy_sources or v == 'csrf_token' or v.get('verbruiker')=="zonne-energie":
                continue
            else:
                energy_sources.append(verbruikers.get(v.get('verbruiker')))
        session['verbruikers'] = energy_sources
        print("++++++++++++++++++++++++++++++++++++++++++=", energy_sources)
        cont=True
        if energy_sources:
            # redirect to the consumption form
            return redirect(url_for('consumption'))

    return render_template('formTwoA.html',form=form,c=combi)


@app.route("/formTwoB", methods=('GET', 'POST'))
def formTwoB(): 
    form = FormTwoB()
    
    if form.validate_on_submit():
        selected1 = form.rv.data
        RVdict = next((d for d in RVinput if d["naam"]==selected1),None)
        selected2 = form.sww.data
        SWWdict = next((d for d in SWWinput if d["naam"]==selected2),None)
        selected3 = form.elec.data
        elec = Elecinput[0] 
        elec.update({"PV":selected3})
        huidigevoorzieningen = {"ruimteverwarming":RVdict,"sanitair warm water":SWWdict,"elektriciteit":elec}
        session["huidige voorzieningen"] = huidigevoorzieningen
        huidigevoorzieningen = {}        
        energy_sources = []
        for v in session['huidige voorzieningen'].values():
            if v.get('verbruiker') in energy_sources or v == 'csrf_token' or v.get('verbruiker')=="zonne-energie":
                continue
            else:
                energy_sources.append(verbruikers.get(v.get('verbruiker')))

        session['verbruikers'] = energy_sources

        if energy_sources:
            # redirect to the consumption form
            return redirect(url_for('consumption'))

    return render_template('formTwoB.html',form=form)


@app.route('/consumption', methods=['GET', 'POST'])
# @cache.cached(timeout=0,key_prefix='consumption')
def consumption():
    energy_sources = session.get('verbruikers')
    form = ConsumptionFormA()
    # print("formprint",form)

    # if request.referrer and 'consumption' not in request.referrer:
    #     # Reset the form to remove dynamically added fields
    #     form = ConsumptionForm()
    sources = [source['naam'] for source in energy_sources]
    print(sources)
    sourcedata = {source['naam']:source.get('tokWh') for source in energy_sources}
    print(sourcedata)
    pv = session.get("huidige voorzieningen").get('elektriciteit').get('PV')
    var = None
    if "aardgas" in sources and 'stookolie' not in sources:
        var = 10

    elif "stookolie" in sources and 'aardgas' not in sources:
        var = 20

    elif "stookolie" in sources and "aardgas" in sources:
        var = 30
 
    else:
        var = -1  # Set a default value when none of the conditions match
    

    

    # for source in energy_sources:
    #     name = source.get('naam')
    #     print("TEST",name)
    #     eenheid = source.get('eenheid')
    #     price = source.get('kost per kwh') if source.get('tokwh') == None else source.get('kost per kwh')/source.get('tokwh')
    #     avg = source.get('avg') 
    #     setattr(ConsumptionForm, f'{name}_consumption', FloatField(f'Geef uw jaarverbruik aan {name} in [{eenheid}]',default = avg, validators=[InputRequired()],description= f'{name}'))
    #     setattr(ConsumptionForm, f'{name}_prijs', FloatField(f'Geef uw prijs (in €) per {eenheid} in voor {name}',default = price,validators=[InputRequired()]))
    
    # if session.get("huidige voorzieningen").get('elektriciteit').get('PV') == "Nee":
    #     setattr(ConsumptionForm, 'sizePV', FloatField('kWh van pv installatie',validators=[InputRequired()],default = 3500,description= "Zonnepanelen: zie uitleg rechts"))
    #     setattr(ConsumptionForm, 'pricePV', FloatField('kost pv installatie',validators=[InputRequired()],default = 4500))
    

    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():

    
        # create a dictionary from the form data
        verbruik = {}
        kost = {}
        # verbruik = {source: getattr(form, source + '_consumption').data for source in energy_sources}
        # kost = {source: {"kost per kwh":getattr(form, source + '_prijs').data} for source in energy_sources}
        #aardgas inladen
        if var == 10 :
            a = sourcedata['aardgas']
            verbruik['aardgas'] = form.aardgas.data * a if a != None else form.aardgas.data
            kost['aardgas'] = {"kost per kwh":form.aardgasC.data/a} if a != None else {"kost per kwh":form.aardgasC.data}
        #stookolie inladen
        if var == 20:
            a = sourcedata['stookolie']
            verbruik['stookolie'] = form.stookolie.data * a if a != None else form.stookolie.data
            kost['stookolie'] = {"kost per kwh":form.stookolieC.data/a} if a != None else {"kost per kwh":form.stookolieC.data}
        
        if var == 30:
            a = sourcedata['stookolie']
            b = sourcedata['aardgas']
            verbruik['stookolie'] = form.stookolie.data * a if a != None else form.stookolie.data
            kost['stookolie'] = {"kost per kwh":form.stookolieC.data/a} if a != None else {"kost per kwh":form.stookolieC.data}
            verbruik['aardgas'] = form.aardgas.data * b if b != None else form.aardgas.data
            kost['aardgas'] = {"kost per kwh":form.aardgasC.data/b} if b != None else {"kost per kwh":form.aardgasC.data}

       
        session['PV'] = {'PV':False,'size':0,'price':0} if pv == 'Ja' else {'PV':True,'size':form.sizePV.data,'price':form.pricePV.data}
        


        verbruik['elektriciteit'] = form.elec.data  # * a if a != None else form.elec.data
        kost['elektriciteit'] = {"kost per kwh":form.elecC.data/a} if a != None else {"kost per kwh":form.elecC.data}

        print("verbruik na inlezen",verbruik)
        session['verbruik'] = verbruik
        session['kost'] = kost
        
        # for source in energy_sources:
        #     a = source.get('tokWh')
        #     s = source.get('naam')
        #     verbruik[s] = getattr(form, s + '_consumption').data*a if a != None else getattr(form, s + '_consumption').data
        #     kost[s] = {"kost per kwh":getattr(form, s + '_prijs').data/a} if a != None else {"kost per kwh":getattr(form, s + '_prijs').data}
        # session['verbruik'] = verbruik
        # session['kost'] = kost
       
        return redirect(url_for('calculate'))
        # if pv == "Ja":
        #     session['PV'] = {'PV':False,'size':0,'price':0}
        #     return redirect(url_for('calculate'))
        
        # elif pv == "Nee":
        #     session['PV'] = {'PV':True,'size':form.sizePV.data,'price':form.pricePV.data}
        #     return redirect(url_for('calculate'))
   

    return render_template('consumption_form.html', form=form,scen = var, PV=pv)
# @app.before_request
# def before_request():
#     if request.referrer and '/consumption' in request.referrer:
#         cache.delete('consumption')


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
    if a == "Radiatoren":
        r = 0
    else:
        r = 1
        
    if i == "Goed geisoleerd":
        c = 2
    elif i == "Matig geisoleerd":
        c = 1
    else:
        c = 0
    index = (r,c)
    scenariosf = scenarios
 
    calc = main(toepass=toepassingen,huidigeVoorzieningen=session.get('huidige voorzieningen'),huidigverbruik=session.get('verbruik'),scenariosList=scenariosf,updateverbruikers=session.get("kost"),PV=session.get('PV'),inwoners=session.get("variables").get("inwoners"),COPindex=index)
    print("sessie!", session.get('PV'))
    pdf = generatePDF(calc[0],calc[1])
    session['file'] = pdf[0]
    session['graph'] = calc[2]
    if pdf[1] == True:
        return redirect(url_for("results"))


@app.route('/results')
def results():
    labels = ['Besparing CO2', 'Besparing primaire energie', 'Besparing verbruikskost']
    data = []
    table = []
    dict = session.get('graph')
    for i in range(len(dict)):
        tabled = {"scenario":f'Scenario {i+1}',"voorziening":dict[i].get('profiel').get('ruimteverwarming'),"CO2abs":dict[i].get('co2abs'),"CO2perc":dict[i].get('co2'),"prim":dict[i].get('primaire'),"primP":dict[i].get('primaireP'),'kost':dict[i].get('kost'),'kostP':dict[i].get('kostP'),'investering':dict[i].get('investering')}
        n = dict[i].get('profiel').get('ruimteverwarming')
        txt = ""
        if "lucht-water" in n:
            txt = 'LW'
        elif "lucht-lucht" in n:
            txt = 'LL'
        elif "bodem-water" in n:
            txt = 'BW'
        elif "hybride" in n:
            txt = 'HY'
        tabled['txt'] = txt
         
        dataset = {
            'label': f'{n}',
            'data': [dict[i].get('co2'),dict[i].get('primaireP'),dict[i].get('kostP')],
            'backgroundColor': f'rgba({(i)*100}, {(i)*150}, {(i)*90}, 0.2)',
            'borderColor': f'rgba({i*0}, {i*0}, {i*0}, 1)',
            'borderWidth': 1,
            'stack': i-1 
        }
        data.append(dataset)
        table.append(tabled)
    userdata = []
    for v in session.get('variables').values():
        userdata.append(v)


 

    return render_template('results.html',userd = userdata, labels = labels, datasets=data,table=table)


@app.route('/download')
def sendFile():
    pdf = session.get('file')
    with open(pdf,'r'):     
        try:
            return send_file(pdf) #, as_attachment=True)
        except Exception as e:
            return str(e)


if __name__=='__main__':
    app.run(debug=True, host = "0.0.0.0")

