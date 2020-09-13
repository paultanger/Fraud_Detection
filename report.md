## An overview of a chosen "optimal" modeling technique, with:
we ran all numerical columns with along the an expaned version of the "ticket type" column and modeled if with a ranom forest classification model. We took the text from the description column and creates its own data fram where we tockenized and clustered with kmeans algorithm. 
## process flow

## preprocessing
> We took all columns with numerical values and filled nans with the mean of the column. we expanded the "ticket type" column into rows of tickets sold, ticket quantity , average ticket sale price, and ratio of sold to tickets available.  

# comparing fraud and not fraud examples
We found that many of the numerical variable means were different between the two groups:

| Fraud   |   approx_payout_date |   body_length |   channels |   delivery_method |   event_created |   event_end |   event_published |   event_start |   fb_published |     gts |   has_analytics |   has_header |   has_logo |   name_length |   num_order |   num_payouts |   object_id |   org_facebook |   org_twitter |   sale_duration |   sale_duration2 |   show_map |   user_age |   user_created |   user_type |   venue_latitude |   venue_longitude |
|:--------|---------------------:|--------------:|-----------:|------------------:|----------------:|------------:|------------------:|--------------:|---------------:|--------:|----------------:|-------------:|-----------:|--------------:|------------:|--------------:|------------:|---------------:|--------------:|----------------:|-----------------:|-----------:|-----------:|---------------:|------------:|-----------------:|------------------:|
| False   |          1.35125e+09 |       3886.99 |       6.38 |              0.48 |     1.34587e+09 | 1.35082e+09 |       1.34291e+09 |   1.35054e+09 |           0.14 | 2481.68 |            0.08 |         0.21 |       0.86 |         42.78 |       30.34 |         37.04 | 4.51462e+06 |           8.63 |          4.69 |           49.83 |            53.95 |       0.85 |     402.68 |    1.31108e+09 |        2.82 |            35.17 |            -60.69 |
| True    |          1.34769e+09 |       1508.89 |       4.15 |              0.07 |     1.34533e+09 | 1.34726e+09 |       1.31854e+09 |   1.34678e+09 |           0.02 | 1911.21 |            0    |         0.07 |       0.65 |         29.98 |        4.53 |          0.58 | 4.70004e+06 |           1.04 |          0.29 |           14.13 |            16.54 |       0.76 |      87.15 |    1.3378e+09  |        1.62 |            35.97 |            -43.41 |



## accuracy metrics selected
f1 score: harmonic mean of recal and percision

## validation and testing methodology
We split the data frame into train and test sets with with stratification to make sure we have the same ratio of fraud cases in train and test. We  fit our model with the train set, then use the test set to get a score for the model

## parameter tuning involved in generating the model
further steps you might have taken if you were to continue the project.

## notes on the code:
* in src/ load_json_to_db.py loads the original data into these tables:
- original_data
- org_ticket_types
- org_previous_payouts

* The second and third tables were nested json and were broken out.  Each table has object_id (and in the original data table it is the primary key).  The second and third tables have multiple rows for object_id and will be aggregated later.

* Then api_client.py can be run and will keep adding rows to these tables:
- api_data
- ticket_types
- previous_payouts

* api_data actually has some columns that aren't in the API data and could be updated later: `acct_type` and `approx_payout_date`.  Also of note, the api data has a `sequence_number` that the original data doesn't have.
