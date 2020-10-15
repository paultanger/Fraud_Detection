
# Detection of fraudulent event submissions

## Overview

This project implements a random forest classification model to predict whether events submitted to an event website are real or fraudulent events.  The events are pulled from an API and stored in a Postgres database and displayed using a Flask app.

## Table of Contents

* [Data sources and EDA](#data-EDA-cleaning)
* [API and database implementation](#API-and-database-implementation)
* [Modeling](#Modeling)
* [Results](#Results)
* [Web app](#web-app)
* [Code overview](code-overview)

## Data, EDA, cleaning

A set of data was obtained with tags for the type of event category (list types here)
We chose to use all numerical features. We filled nans with with the mean of the column except for the longitude and latitude column which we filled with 0.

We also took the ```ticket_types``` column and made new columns associated with average ticket cost, total quantity of tickets, tot tickets sold and ratio of sold to quantity.

This left us with 31 features. 

discuss differences between training data and API data
TODO: finish this section

### Correlation Plots
our features mostly are correlated
![fn](images/corr_plot.png)

### Comparing Fraud and Not Fraud Examples
We found that many of the numerical variable means were different between the two groups:

| Fraud   |   approx_payout_date |   body_length |   channels |   delivery_method |   event_created |   event_end |   event_published |   event_start |   fb_published |     gts |   has_analytics |   has_header |   has_logo |   name_length |   num_order |   num_payouts |   object_id |   org_facebook |   org_twitter |   sale_duration |   sale_duration2 |   show_map |   user_age |   user_created |   user_type |   venue_latitude |   venue_longitude |
|:--------|---------------------:|--------------:|-----------:|------------------:|----------------:|------------:|------------------:|--------------:|---------------:|--------:|----------------:|-------------:|-----------:|--------------:|------------:|--------------:|------------:|---------------:|--------------:|----------------:|-----------------:|-----------:|-----------:|---------------:|------------:|-----------------:|------------------:|
| False   |          1.35125e+09 |       3886.99 |       6.38 |              0.48 |     1.34587e+09 | 1.35082e+09 |       1.34291e+09 |   1.35054e+09 |           0.14 | 2481.68 |            0.08 |         0.21 |       0.86 |         42.78 |       30.34 |         37.04 | 4.51462e+06 |           8.63 |          4.69 |           49.83 |            53.95 |       0.85 |     402.68 |    1.31108e+09 |        2.82 |            35.17 |            -60.69 |
| True    |          1.34769e+09 |       1508.89 |       4.15 |              0.07 |     1.34533e+09 | 1.34726e+09 |       1.31854e+09 |   1.34678e+09 |           0.02 | 1911.21 |            0    |         0.07 |       0.65 |         29.98 |        4.53 |          0.58 | 4.70004e+06 |           1.04 |          0.29 |           14.13 |            16.54 |       0.76 |      87.15 |    1.3378e+09  |        1.62 |            35.97 |            -43.41 |

## API and database implementation

details of API and db stuff here
* API class stores in postgres db running EC2
We setup an AWS EC2 instance
We created a postgres database

## Modeling

### Accuracy metrics selected
F1 score: harmonic mean of recall and precision. We chose this because the classes were imbalanced. We wanted to make sure we did not have too many false negatives.

### Validation and Testing Methodology
We split our dataset into train and test set stratifying to make sure we have the same ratio of fraud to to not fraud in both sets. We also oversampled the training dataset so there was a higher ratio of fraud in the training so that the model would not just guess all in the majority class. We tried using SMOTE technique instead of oversampling but oversampling performed better.

We found a random forest classifier model to be the best performing model. It got an f1 score TODO: update this on test data.

![fn](images/cm.png)

### discuss oversampling
TODO: 

### Flagging Fraud
Since our model did so well with identifying fraud we looked at the ```.predict_proba``` from our hold out data. We realized that the threshold our model created was very high to be marked as fraud so we decided to have the follow threshold for HIGH, MEDIUM, LOW risk:

If 0.95 < predict_proba < 1 = HIGH
If 0.95 <= predict_prob = MEDIUM
If 0.91 <= predict_prob = LOW

### Model validation
discuss here

### ROC
TODO: revise with new ROC
ROC plot:
![fn](images/ROC1.png)

##  Web app
FLask app discussion here

## Code overview
* in `src/load_json_to_db.py` loads the original data into these tables:
    - `original_data`
    - `org_ticket_types`
    - `org_previous_payouts`

* The second and third tables were nested json and were broken out.  Each table has `object_id` (and in the original data table it is the primary key).  The second and third tables have multiple rows for `object_id` and will be aggregated later.

* Then `api_client.py` can be run and will keep adding rows to these tables:
    - `api_data`
    - `ticket_types`
    - `previous_payouts`

* `api_data` actually has some columns that aren't in the API data and could be updated later: `acct_type` and `approx_payout_date`.  In addition, the api doesn't send data for these cols: `gts`, `num_order`, `num_payout`. Also of note, the api data has a `sequence_number` that the original data doesn't have.

* The `cleaner_funcs.py` is intended to be implemented with the `predict_class.py` and called from the app to make new predictions.

