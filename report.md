## An overview of a chosen "optimal" modeling technique, with:
we ran all numerical columns with along the an expaned version of the "ticket type" column and modeled if with a ranom forest classification model. We took the text from the description column and creates its own data fram where we tockenized and clustered with kmeans algorithm. 
## process flow

## preprocessing
> We took all columns with numerical values and filled nans with the mean of the column. we expanded the "ticket type" column into rows of tickets sold, ticket quantity , average ticket sale price, and ratio of sold to tickets available.  


## accuracy metrics selected
f1 score: harmonic mean of recal and percision

## validation and testing methodology
We split the data frame into train and test sets with with stratification to make sure we have the same ratio of fraud cases in train and test. We  fit our model with the train set, then use the test set to get a score for the model

## parameter tuning involved in generating the model
further steps you might have taken if you were to continue the project.

