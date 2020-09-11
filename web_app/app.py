from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

# #---     use pickle to load in the pre-trained model; loaded at the top of the app, loaded into memory ONCE on the server rather than loaded every time
# with open(f'','rb') as f:
#     model = pickle.load(f)

app = Flask(__name__, template_folder = 'templates/')

x = pd.read_csv('data/sample_df.csv')

@app.route('/', methods=['GET'])
def home():
    return ''' <p> nothing here, friend, but a link to 
                   <a href="/hello">hello</a> and an 
                   <a href="/form_example">example form</a> </p> '''

@app.route('/hello', methods=['GET'])
def hello_world():
    return ''' <h1> Hello, World!</h1> '''

@app.route('/form_example', methods=['GET'])
def form_display():
    return ''' <form action="/string_reverse" method="POST">
                <input type="text" name="some_string" />
                <input type="submit" />
               </form>
             '''

@app.route('/string_reverse', methods=['POST'])
def reverse_string():
    text = str(request.form['some_string'])
    reversed_string = text[-1::-1]
    return ''' output: {}  '''.format(reversed_string)

#---    getting a pandas df to display on a web app
@app.route('/analysis') 
def analysis():
    return render_template("analysis.html", tables=[x.to_html(classes='data')], titles=x.columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


"""
M notes:
#----   after cursor add following code to take in new data and put into PD
#----   take input from SQL and place into Pandas DF
sql_query = pd.read_sql_query('SELECT * FROM **NAME**, conn)

#----   will need to run sql_query through cleaning function
from predict import all_together

cleaned_x = all_together(sql_query)

#----   will need to run code above through pickle model
loaded_model = pickle.load(open('../data/pickle_model.pkl', 'rb'))
proba = loaded_model.predict_proba(cleaned_x) #array of proba
proba = list(proba[:,1])
cleaned_x['prediction'] = proba

#----   get pred.proba and categorize into HIGH, MED, LOW by adding column *WHERE does this info go?
def flag_label(row):
    if row['predict'] == 1 and row['predict'] > 0.97:
        return 'HIGH'
    elif row['predict'] > 0.95:
        return 'MEDIUM'
    elif row['predict'] > 0.91:
        return 'LOW'
    else:
        return 'Not Fraud'

cleaned_x['flag'] = cleaned_x.apply(lambda row: flag_label(row), axis = 1)
display = cleaned_x.iloc[:,[16, 32]].copy() #DOUBLE CHECK

#----   render above dataframe as html and select 
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()
#----   show top features and fraud label and specific identification label 
fraud_html = display.to_html()

#----   write html to flask app
text_file = open("fraud_check.html", "w")
text_file.write(html)
text_file.close()
"""