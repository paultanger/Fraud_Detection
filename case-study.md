## Premise

You are a contract data scientist/consultant hired by a new e-commerce site to try to weed out fraudsters.  The company unfortunately does not have to many data science expertise... so you must properly scope and present your solution to the manager before you embark on your analysis.  Also, you will need to build a sustainable software project that you can hand off to the companies engineers by deploying your model in the cloud.  Since others will potentially use/extend your code you **NEED** to properly encapsulate your code and leave plenty of comments.

#### NOTE: This data is VERY sensitive! It is called train.json and is on the desktop of the mac mini. Do not share this data with anyone or copy any of it off the Mac mini's.  You will be required to work on the project in the classroom.

### Deliverables (i.e. what you will be graded on)

* Scoping document (in Markdown)
* Code on private fork of repo on Github
    * proper functions/encapsulation
    * well commented
    * Model description document (see below)
* Flask app with well documented API
    * Needs to register your service at POST `/register`
    * Needs to accept input records on POST `/score` endpoint
* Web based front-end to enable quick triage of potential fraud
    * Triage importance of transactions (low risk, medium risk, high risk)
    * Extra: D3 based visualization of data/trend

### The "product" of fraud

Something that you will (need to) think about throughout this sprint is how the product of your client fits into the give technical process.  A few points to note about the case of fraud:

* Failures are not created equal
    * False positives decrease customer/user trust
    * False negatives cost money
        * Not all false negative cost the same amount of $$$
* Accessibility
    * Other (non-technical) people may need to interact with the model/machinery
    * Manual review

The fraud problem is actually semi-supervised in a way.  You do not use the model to declare a ground truth about fraud or not fraud, but simply to flag which transactions need further manual review.  We will essentially be building a triage model of what the most pressing (and costly) transaction we have seen.

### Step 1: Scope the problem

Before we dive into things we will need to scope the problem.  In the scoping stage we will define key metrics that we will use to measure success and outline the general steps you will take (with estimated time to completion).

#### [Deliverable]: Scoping document

1. A high level description of your approach in tackling this data science project:
    1. What steps did you take first (e.g. data exploration, visualization, statistical analyses)?
    2. What insights were generated from this exploration?
    3. Which modeling and preprocessing algorithms did you consider using to solve this problem?
        * What are the respective strengths/weaknesses of these tactics?
    4. Which modeling and preprocessing algorithms did you experiment with prior to producing your optimal model?
        * What were the results of these attempts: strengths/weaknesses, decision process behind acceptance/rejection, further insights into the data set?
        * What validation and testing methodology did you use?
    5. Success metric

### Step 2: The Model

#### [Deliverable]: Model description and code
* You may use any one (or multiple) supervised learning techniques to create this classification model, and any natural language pre-processing that you find generates the best results.
* Try comparing different models we have encountered (SVM, Logistic Regression, Decision Trees, kNN) as well as different featurization techniques (stemming vs lemmatization, tf-idf vs. bag of words, part of speach tagging, etc.)
* Feel free to use any library to get the job done.
* In your pull request, describe your project findings including:
    * An overview of a chosen “optimal” modeling technique, with:
        * process flow
        * preprocessing
        * accuracy metrics selected
        * validation and testing methodology
        * parameter tuning involved in generating the model
        * further steps you might have taken if you were to continue the project.
* Always be committing (ABC) to Github
    * clean and modular code
    * Comments for every method

#### [Deliverable]: Pickled model

Use `cPickle` to serialize your trained model and store it in a file. This is going to allow you to use the model without retraining it for every prediction, which would be ridiculous.

### Step 3: Prediction script

Take a few raw examples and store them in json or csv format in a file called `test_script_examples` or the like.

#### [Deliverable]: Prediction script

Write a script `predict.py` that reads in a single example from `test_script_examples`, vectorizes it, unpickles the model, predicts the label, and outputs the label probability (print to standard out is fine).

This script will serve as a sort of conceptual and code bridge to the web app you're about to build.

Each time you run the script, it will predict on one example, just like a web app request. You may be thinking that unpickling the model everytime is quite inefficient and you'd be right; we'll remove that inefficiency in the web app.

### Step 4: Database

#### [Deliverable]: Prediction script backed by a database

We want to store each prediction the model makes on new examples, which means we'll need a database.

Set up a postgres database that will store each example that the script runs on. You should create a database schema that reflects the form of the raw example data and add a column for the predicted probability of fraud.

Write a function in your script that takes the example data and the prediction as arguments and inserts the data into the database.

Now, each time you run your script, one row should be added to the `predictions` table with a predicted probability of fraud.

### Step 5: Web App

#### [Deliverable]: Hello World app

A request in your browser to `/hello` should display "Hello, World!". Set up a Flask app with a route `GET /hello` to do so.

Use this [tutorial](http://blog.luisrei.com/articles/flaskrest.html) to help.

#### [Deliverable]: Fraud scoring service

Set up a route `POST /score` and have it execute the logic in your prediction script. You should import the script as a module and call functions defined therein.

There are two things we'll do to make this all more efficient: 1. We only want to unpickle the model once, and 2. We only want to connect to the database once. Do both in a `if __name__ == '__main__':` block before you call `app.run()` and you can refer to these top-level global variables from within the function. This may require some re-architecting of your prediction module.

The individual example will no longer be coming from a local file, but instead will come in the body of the POST request as JSON. You can use `request.data` or `request.json` to access that data. You'll still need to vectorize it, predict, and store the example and prediction in the database.

You can test out this route by, in a separate script, sending a POST request to /score with a single example in JSON form using the `requests` Python package.

### Step 6: Get "live" data

We've set up a service for you that will ping your server with "live" data so that you can see that it's really working.

To use this service:
    * Send a POST request to `/register` with your IP and port (as `ip` and `port` parameters in JSON). We'll announce what the ip address of the service machine is in class. Write this code in the `if name` block at the bottom of your Flask script (i.e. it should register each time you run the Flask script)

Make sure your app is adding the examples to the database with predicted fraud probabilities.

### Step 7: Dashboard

#### [Deliverable]: Web front end to present results

We want to present potentially fraudulent transactions with their probability scores from our model. The transactions should be segmented into 3 groups: low risk, medium risk, or high risk (based on the probabilities).

* Add route in Flask app for dashboard
* Read data from postgres
* Return HTML with the data
    * To generate the HTML from the json data from the database, either just use simple string concatenation or Jinja2 templates.

### Step 8: Deploy!

Use the [aws sprint](https://github.com/zipfian/aws-and-the-cloud) as your guide if you need one.

Should be accessible on AWS.

* Set up AWS instance
    * Restrict IP address access to Data Warehouse (remember, data is sensitive!). You can do this on the aws website when configuring your instance.
* Set up environment on your EC2 instance
* Push your code to github
* SSH into the instance and clone your repo
* Run Flask app on instance (make sure you update the register code with your updated ip and port)
* Make it work (debug, debug, debug)
* Profits!

### Step 9: Present

Create a 3 minute presentation on your model, the application/interface, its performance, and any information you think is pertinent to the client.

You will be presenting Friday afternoon.

### Extra

* Make your dashboard interactive. Allow a dashboad user to clear or flag fraud events. Come up with other features that might be useful.

* Create a D3 visualization for your web based frontend.  You might want to visualize any number of metrics/data.  Use your creativity to create something that makes sense for a end user in terms of what data you present.

