## Premise
You are a contract data scientist/consultant hired by a new e-commerce site to try to weed out fraudsters.  The company unfortunately does not have much data science expertise... so you must properly scope and present your solution to the manager before you embark on your analysis.  Also, you will need to build a sustainable software project that you can hand off to the companies engineers by deploying your model in the cloud.  Since others will potentially use/extend your code you **NEED** to properly encapsulate your code and leave plenty of comments.

## The Data
#### NOTE: This data is VERY sensitive!

It is located in `data/data.zip`.

***Do not share this data with anyone or copy any of it off the mac minis! Do not include the data file in your pull request!***

You will be required to work on the project in the classroom.


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
Something that you will (need to) think about throughout this sprint is how the product of your client fits into the given technical process.  A few points to note about the case of fraud:

* Failures are not created equal
    * False positives decrease customer/user trust
    * False negatives cost money
        * Not all false negative cost the same amount of $$$
* Accessibility
    * Other (non-technical) people may need to interact with the model/machinery
    * Manual review

The fraud problem is actually semi-supervised in a way.  You do not use the model to declare a ground truth about fraud or not fraud, but simply to flag which transactions need further manual review.  We will essentially be building a triage model of what the most pressing (and costly) transaction we have seen.

## Day 1: Morning

### Step 1: EDA
Before we start building the model, let's start with some EDA.

#### [Deliverable]: Look at the data
Let's start by looking at the data.

1. Load the data in with pandas. Add a 'Fraud' column that contains True or False values depending on if the event is fraud. This is determined based on the `acct_type` field.

2. Check how many fraud and not fraud events you have.

3. Look at the features. Make note of ones you think will be particularly useful to you.

4. Do any data visualization that helps you understand the data.


#### [Deliverable]: Scoping the problem
Before you get cranking on your model, let's think of how to approach the problem.

1. Think of what preprocessing you might want to do. How will you build your feature matrix? What different ideas do you have?

2. What models do you want to try?

3. What metric will you use to determine success?


### Step 2: Building the Model

#### [Deliverable]: Comparing models
Now start building your potential models.

**Notes for writing code:**
* As you write your code, **always be committing** (ABC) to Github!
* Write **clean and modular code**.
* Include **comments** on every method.

*Make sure to get a working model first before you try all of your fancy ideas!*

1. If you have complicated ideas, implement the simplest one first! Get a baseline built so that you can compare more complicated models to that one.

2. Experiment with using different features in your feature matrix. Use different featurization techniques like stemming, lemmatization, tf-idf, part of speech tagging, etc.

3. Experiment with different models like SVM, Logistic Regression, Decision Trees, kNN, etc. You might end up with a final model that is a combination of multiple classification models.

4. Compare their results. Make sure to do good comparison and don't just use accuracy!

## Day 1: Afternoon

#### [Deliverable]: Model description and code
After all this experimentation, you should end up with a model you are happy with.

1. Create a file called `model.py` which builds the model based on the training data.

    * Feel free to use any library to get the job done.
    * Again, make sure your code is **clean**, **modular** and **well-commented**! The general rule of thumb: if you looked at your code in a couple months, would you be able to understand it?

2. In your pull request, describe your project findings including:
    * An overview of a chosen “optimal” modeling technique, with:
        * process flow
        * preprocessing
        * accuracy metrics selected
        * validation and testing methodology
        * parameter tuning involved in generating the model
        * further steps you might have taken if you were to continue the project.


#### [Deliverable]: Pickled model

1. Use `cPickle` to serialize your trained model and store it in a file. This is going to allow you to use the model without retraining it for every prediction, which would be ridiculous.

### Step 3: Prediction script

Take a few raw examples and store them in json or csv format in a file called `test_script_examples` or the like.


#### [Deliverable]: Prediction script

1. Write a script `predict.py` that reads in a single example from `test_script_examples`, vectorizes it, unpickles the model, predicts the label, and outputs the label probability (print to standard out is fine).

    This script will serve as a sort of conceptual and code bridge to the web app you're about to build.

    Each time you run the script, it will predict on one example, just like a web app request. You may be thinking that unpickling the model every time is quite inefficient and you'd be right; we'll remove that inefficiency in the web app.


### Step 4: Database

#### [Deliverable]: Prediction script backed by a database

We want to store each prediction the model makes on new examples, which means we'll need a database.

1. Set up a Postgres or MongoDB database that will store each example that the script runs on. You should create a database schema that reflects the form of the raw example data and add a column for the predicted probability of fraud.

2. Write a function in your script that takes the example data and the prediction as arguments and inserts the data into the database.

    Now, each time you run your script, one row should be added to the `predictions` table with a predicted probability of fraud.

## Day 2: Morning

### Step 5: Web App

#### [Deliverable]: Hello World app

1. A request in your browser to `/hello` should display "Hello, World!". Set up a Flask app with a route `GET /hello` to do so.

    Use this [tutorial](http://blog.luisrei.com/articles/flaskrest.html) to help.

#### [Deliverable]: Fraud scoring service

1. Set up a route `POST /score` and have it execute the logic in your prediction script. You should import the script as a module and call functions defined therein.

    There are two things we'll do to make this all more efficient:

    1. We only want to unpickle the model once
    2. We only want to connect to the database once.

    Do both in a `if __name__ == '__main__':` block before you call `app.run()` and you can refer to these top-level global variables from within the function. This may require some re-architecting of your prediction module.

    The individual example will no longer be coming from a local file, but instead you will get it by making an HTTP GET request to a server that will give you a data point as a string, which you can parse into JSON.  (You can use json.loads() to parse a string to json, which is the reverse process of json.dumps().)  You will still need to vectorize this example data point, predict, and store it along with your prediction in the database.

    You can test out this route by, in a separate script, sending a GET request to the /data_point route on the data server (hosted by us, see section below) using the `requests` Python package.


### Step 6: Get "live" data

We've set up a service for you that will periodically release new, "live" data so that you can experience working with a dataset that is not static.

To use this service, you will need to make a GET request to `http://galvanize-case-study-on-fraud.herokuapp.com/data_point`.

There are a few interesting aspects to the data flow that we want you to experience during this case study.  One aspect is that the dataset is *dynamic*, not static.  That means that while you do have a certain amount of training data, *more (unlabeled) data is generated all the time* that needs to be labeled (predicted).  Therefore you can't simply run a script locally, predict all your unknown data points, and save the result as, say, a .csv or into a database, as you might do with a static dataset.  Instead, to handle a dynamic dataset, you need a 'live' function that uses your model to predict a new data point on the fly.  So where does that new data point to predict come from?  When you're writing a data product, in this case a prediction service, you often set up a route on your server like /score, which scores/predicts an individual data point.  Indeed, you'll want to do that here.  Usually, you'll deploy your app to a place like AWS or Heroku or inside your company's network, where other machines can access it (ie, they can make a POST request to your /score endpoint, sending inside the POST request the new data point to be scored).  It can be a little hard to develop such an app, though, since while you're developing locally you'll likely be running the app on your laptop, usually within a network like Galvanize's or at, say, a cafe with WiFi, and requests can't come from elsewhere on the internet into your machine.  So we are going to use a slightly different flow here to get new data points.  Namely, you are going to make GET requests to a server (that we've set up for you) that offers up new data points every so often.  Once you make that GET request, you'll want to send the results of the request over to your own /score route to score them.  This simulates the experience of using a model on a new data point live, while allowing for easy local development.  (As an extension if you're feeling ambitious, you could create a route named something like /get_and_score, which would both GET a fresh new data point as well as score it.)  So, to summarize: make a GET request to `http://galvanize-case-study-on-fraud.herokuapp.com/data_point`, take the result and parse it into JSON, take that result and score it using your model, and save the resulting prediction along with the data point to your database of predicted fraud probabilities.

**Make sure your app is adding the examples to the database with predicted fraud probabilities.**

What's happening over at `http://galvanize-case-study-on-fraud.herokuapp.com/data_point`?  Well, there are 3 concurrent processes load-balanced behind that endpoint, so any request to that URL might end up being routed to one of three processes.  Each of those processes chooses a random data point (with replacement) and continues to serve it up for X seconds, where X is somewhere in the range of 10s-60s (secret ;).  You don't have control (by design) of which process your request gets sent to.  So, you might make three requests to that URL and hit one process once, one process twice, and one process not at all.  Assuming you flooded the server with many requests for a few seconds, you would get many responses, but only 3 of them would be unique.  If you continued to make requests and de-duplicate the results over a longer period of time, you would get a maximum of 3 unique data points every X seconds.

## Day 2: Afternoon

### Step 7: Dashboard

#### [Deliverable]: Web front end to present results

We want to present potentially fraudulent transactions with their probability scores from our model. The transactions should be segmented into 3 groups: low risk, medium risk, or high risk (based on the probabilities).

* Add route in Flask app for dashboard
* Read data from postgres
* Return HTML with the data
    * To generate the HTML from the json data from the database, either just use simple string concatenation or Jinja2 templates.


### Step 8: Deploy!

Use [these instructions](https://github.com/zipfian/project-proposals/blob/master/host_app_on_amazon.md) as your guide if you need one.

* Set up AWS instance
* Set up environment on your EC2 instance
* Push your code to github
* SSH into the instance and clone your repo
* Run Flask app on instance (make sure you update the register code with your updated ip and port)
* Make it work (debug, debug, debug)
* Profits!


### Extra

* Make your dashboard interactive. Allow a dashboard user to clear or flag fraud events. Come up with other features that might be useful.

* Create a D3 visualization for your web based frontend.  You might want to visualize any number of metrics/data.  Use your creativity to create something that makes sense for a end user in terms of what data you present.
