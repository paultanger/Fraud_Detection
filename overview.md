## Premise
You are a contract data scientist/consultant hired by a new e-commerce site to try to weed out fraudsters.  The company unfortunately does not have much data science expertise... so you must properly scope and present your solution to the manager before you embark on your analysis.  Also, you will need to build a the core of a software project that can be deployed by the company engineers using your best model to make predictions.  Since others will potentially use/extend your code you **NEED** to properly encapsulate your code and leave plenty of comments.

## The Data
#### NOTE: This data is VERY sensitive!

It is located in `data/data.zip`.

***Do not share this data with anyone! Do not include the data file in your pull request!***

You will be required to work on the project on campus.


### Deliverables 
* Scoping document (in Markdown)
* Code on private fork of repo on Github
    * Proper functions/encapsulation
    * Well commented
    * Model description document (see below)
* Prediction and results saving script with usage instructions
    * Needs to query "live" data from our data generator.
    * Needs to query the database to produce a prediction record history.
    * Optional: Produce three categories for your predictions: Low, Medium, and High Risk. How you categorize these is up to you.


### The "product" of fraud
Something that you will need to think about throughout this case study is how the product of your client fits into the given technical process.  A few points to note about the case of fraud:

* Failures are not created equal
    * False positives decrease customer/user trust
    * False negatives cost money
        * Not all false negative cost the same amount of money
* Accessibility
    * Other (non-technical) people may need to interact with the model/machinery
    * Manual review

Your model will be used only as the first step in the fraud identification process. You do not use the model to declare a ground truth about fraud or not fraud, but simply to flag which transactions need further manual review.  You will be building a triage model of what are the most pressing (and costly) transactions you have seen. It may also be useful to display what factors contribute to a given case being flagged as fraudulent by your model.  

# Suggested Timeline

## Morning

### Step 1: EDA
Before you start building the model, start with some EDA.

#### [Deliverable]: Look at the data
Start by looking at the data.

1. Load the data with pandas. Add a 'Fraud' column that contains True or False values depending on if the event is fraud. If `acct_type` field contains the word `fraud`, label that point Fraud.

2. Check how many fraud and not fraud events you have.

3. Look at the features. Make note of ones you think will be particularly useful to you.

4. Do any data visualization that helps you understand the data.


#### [Deliverable]: Scoping the problem
Before you get cranking on your model, think of how to approach the problem.

1. What preprocessing might you want to do? How will you build your feature matrix? What different ideas do you have?

2. What models do you want to try?

3. **What metric will you use to determine success?**


### Step 2: Building the Model

#### [Deliverable]: Comparing models
Start building your potential models.

**Notes for writing code:**
* As you write your code, **always be committing** (ABC) to Github!
* Write **clean and modular code**.
* Include **comments** on every method.

*Make sure to get a working model first before you try all of your fancy ideas!*

1. If you have complicated ideas, implement the simplest one first! Get a baseline built so that you can compare more complicated models to that one.

2. Experiment with using different features in your feature matrix. Use different featurization techniques like stemming, lemmatization, tf-idf, part of speech tagging, etc.

3. Experiment with different models like SVM, Logistic Regression, Decision Trees, kNN, etc. You might end up with a final model that is a combination of multiple classification models.

4. Compare their results. Pick a good metric; don't just use accuracy!

## Afternoon

#### [Deliverable]: Model description and code
After all this experimentation, you should end up with a model you are happy with.

1. Create a file called `model.py` which builds the model based on the training data.

    * Feel free to use any library to get the job done.
    * Again, make sure your code is **clean**, **modular** and **well-commented**! The general rule of thumb: if you looked at your code in a couple months, would you be able to understand it?

2. In a file called `report.md`, describe your project findings including:
    * An overview of a chosen "optimal" modeling technique, with:
        * process flow
        * preprocessing
        * accuracy metrics selected
        * validation and testing methodology
        * parameter tuning involved in generating the model
        * further steps you might have taken if you were to continue the project.


#### [Deliverable]: Pickled model

1. Use `pickle` to serialize your trained model and store it in a file. This is going to allow you to use the model without retraining it for every prediction, which would be ridiculous.

### Step 3: Prediction script

Take a few raw examples and store them in json or csv format in a file called `test_script_examples`.


#### [Deliverable]: Prediction script

1. Write a script `predict.py` that reads in a single example from `test_script_examples`, vectorizes it, unpickles the model, predicts the label, and outputs the label probability (print to standard out is fine).

    This script will serve as a sort of conceptual and code bridge to the web app you're about to build.

    Each time you run the script, it will predict on one example, just like a web app request. You may be thinking that unpickling the model every time is quite inefficient and you'd be right; we'll remove that inefficiency in the web app.


### Step 4: Database

#### [Deliverable]: Prediction script backed by a database

You'll want to store each prediction the model makes on new examples, which means you'll need a database.

1. Set up a Postgres or MongoDB database that will store each example that the script runs on. You should create a database schema that reflects the form of the raw example data and add a column for the predicted probability of fraud.

2. Write a function in your script that takes the example data and the prediction as arguments and inserts the data into the database.

    Now, each time you run your script, one row should be added to the `predictions` table with a predicted probability of fraud.

## Step 5: Presentation

#### [Deliverable]: Presentation of your prediction system and how to use it

1. Describe your own understanding of the data and some key features or trends that provide insight or contain the most signal.

2. Explain what your model does to learn from the data and how it performs. Describe the metrics you've chosen to evaluate your possible models and how your final model performs on unseen test data.

3. Describe how you use the data access point as provided by the "engineers" and how you process and use the data. A demonstration of the collected data and database updates is preferred. 

    Also describe how your engineering team could use the code you've built and the model you've pickled to make predictions and access your database.