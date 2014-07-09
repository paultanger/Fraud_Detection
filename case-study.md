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
    * Needs to register your service at `/register`
    * Needs to accept input records on `/score` endpoint
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

### Step 3: Web App

Complete the [zipfian/data-products](https://github.com/zipfian/data-products) exercise.  This will teach you enough to build you fraud service.

#### [Deliverable]: Flask Scoring Service
* Perform discover on `/register` to let the application know your model/service is online.
    * Send a POST request to `/register` with your IP and port (as `ip` and `port` parameters).
* Listen on `/score` for new data points
* Save all transactions to Postgres
* Web front end to present results
    * Fraudulent transactions with triage score (low risk, medium risk, or high risk)
    * Allow a user to approve/freeze a transaction and mark appropriately in your database

### Step 4: Deploy!

Use the [aws sprint](https://github.com/zipfian/aws-and-the-cloud) as your guide if you need one.

Should be accessible on AWS.

### Step 5: Present

Create a 3 minute presentation on your model, the application/interface, its performance, and any information you think is pertinent to the client.

You will be presenting Friday afternoon.

### Extra

Create a D3 visualization for your web based frontend.  You might want to visualize any number of metrics/data.  Use your creativity to create something that makes sense for a end user in terms of what data you present.

