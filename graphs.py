from flask import Flask, render_template, redirect, url_for, request, session, send_file



app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = 'geheime tekst'


@app.route('/', methods=('GET', 'POST'))
def start():
       # Define Plot Data
    labels = ['CO2 besparing', 'kostbesparing']
 
    num_datasets =[ [0, 10],
   [10, 15] ]

    data = []
            
    for i in range(len(num_datasets)):
        dataset = {
            'label': f'Dataset {i+1}',
            'data': [num_datasets[i][0],num_datasets[i][1]],
            'backgroundColor': f'rgba({i*50}, {i*100}, {i*150}, 0.2)',
            'borderColor': f'rgba({i*50}, {i*100}, {i*150}, 1)',
            'borderWidth': 1,
            'stack': i-1 
        }
        data.append(dataset)


    return render_template(
        'graphs.html', labels = labels, datasets = data
        
    )




if __name__=='__main__':
    app.run(debug=True, host = "0.0.0.0")