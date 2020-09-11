from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

# #---     use pickle to load in the pre-trained model; loaded at the top of the app, loaded into memory ONCE on the server rather than loaded every time
# with open(f'','rb') as f:
#     model = pickle.load(f)

app = Flask(__name__, template_folder = 'templates/')

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
@app.route('/analysis', methods=['GET'])
def analysis():
    x = pd.DataFrame(np.random.randn(20,5))
    return render_template("analysis.html", data = x.to_dict())
    # return ''' <h1> Hello, World!</h1> '''


#---    second attempt/way of getting pandas df to display on web app
@app.route('/tables', methods=['GET'])
def show_tables():
    data = pd.read_json('../data/data.json')
    return render_template('analysis.html', data = data.to_html())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


"""
M notes:
#----   after cursor add following code to take in new data and put into PD

#----   take input from SQL and place into Pandas DF
sql_query = pd.read_sql_query('SELECT * FROM **NAME**, conn)
print(sql_query)

#----   will need to run sql_query through cleaning function
**add code here

#----   will need to run code above through pickle model
loaded_model = pickle.load(open('****', 'rb'))
proba = loaded_model.predict_proba(X) #list of proba
print(proba)

#----   get pred.proba and categorize into HIGH, MED, LOW by adding column *WHERE does this info go?
if proba == 1 and proba < 0.97:
    high
elif proba > 0.97 and proba < 0.95:
    med
elif proba > 0.91 and proba < 0.95:
    low
else:
    not fraud


#----   render above dataframe as html and select 
fraud_html = fraud_check.to_html()

#----   write html to flask app
text_file = open("fraud_check.html", "w")
text_file.write(html)
text_file.close()
"""