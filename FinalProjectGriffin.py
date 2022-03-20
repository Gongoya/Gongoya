# -*- coding: utf-8 -*-
"""House Prices Prediction Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lfr3DVjWFcNKu4KAgbgJzYXKh9Yana5n

# INTRODUCTION
This is a project that builds an end to end Machine learning pipeline and deploy it as an API.
The Tools used are Pycaret and deployment of the app in Streamlit.
"""

# First install pycaret and other libraries to be used in this project
#Installing pycaret

pip install pycaret[full]

#install FastAPI

# pip install fastapi

"""# DATA"""

#The Project will use dataset from pycaret dataset house
#The goal of the tutorial is to predict the house price based on its features like Lot area, Utilities, Lot frontage, sale condition etc.
#The data can be obtained from PyCaret’s repository. https://github.com/pycaret/pycaret/tree/master/datasets

#Import Pycaret, then we load the dataset of the house into python.

# import pycaret

from pycaret.datasets import get_data
House_Data = get_data('house')

#Drop Columns, If any with missing Values.

House_Data_1= House_Data.dropna(axis=1)
print(House_Data_1)

#Drop Rows, If any with missing Values.

House_Data_2 = House_Data_1.dropna()
print(House_Data_2)

House_Data_2.head()

"""# Exploratory Data Analysis"""

#visualization to assess the relationship of independent features (weight, cut, color, clarity, etc.) with the target variable i.e. Price

# plot scatter LotArea and Price
import plotly.express as px
fig = px.scatter(x=House_Data_2['LotArea'], y=House_Data_2['SalePrice'], 
                 facet_col = House_Data_2['YrSold'], opacity = 0.25, template = 'plotly_dark', trendline='ols',
                 trendline_color_override = 'red', title = 'PRICES OF HOUSES')
fig.show()

"""# Distribution of target Variable, Sale Price"""

#Plotting a Histogram will enable us visualize the data and draw inferences of the distribution.

# plot histogram
fig = px.histogram(House_Data_2, x=["SalePrice"], template = 'plotly_dark', title = 'Histogram of Price')
fig.show()

# The above Histogram shows the distribution of the data to be rightly skewed.
# To normalize the data, we will get log transform the data.
#Import numpy
# First we make a copy of the data.

import numpy as np
# create a copy of data
House_Data_2_copy = House_Data_2.copy()
# create a new feature Log_SalePrice
House_Data_2_copy['Log_SalePrice'] = np.log(House_Data_2['SalePrice'])
# plot histogram
fig = px.histogram(House_Data_2_copy, x=["Log_SalePrice"], title = 'Histgram of Log SalePrice', template = 'plotly_dark')
fig.show()

#The Data is now normal. The target variable SalePrice is approximately normal.

"""# Prepare the Data
We next prepare the data using Pycaret, Initialize the set up, check the variables and assess Multicollinearity if any and missing values...etc.
After this step we will model and train the data.
"""

from pycaret.regression import *
s = setup(House_Data_2, target = 'SalePrice', transform_target = True)

"""# Model Training & Selection"""

#Here we use Pycarets functionality of Compare models, and cross validation.

# compare all models
best = compare_models()

#According to the above results, the best model is the 'CatBoost Regressor' It has the lowest Mean Absolute Error (MAE) amongst all the models.

#We also check model residuals of the model we have trained.

# check the residuals of trained model
plot_model(best, plot = 'residuals_interactive')

pip uninstall matplotlib

pip install matplotlib==3.1.3

# check feature importance
plot_model(best, plot = 'feature')

"""# Finalizing of Model Training and Saving the ML pipeline"""

# finalize the model
final_best = finalize_model(best)
# save model to disk
save_model(final_best, 'House_Data_2-pipeline')

"""# Deployment of the ML Model"""

# To deploy, first we need to import some libraries.
#Pandas, Unicorn,load_model, predict_model and FastAPI

import pandas as pd
from pycaret.regression import load_model, predict_model
from fastapi import FastAPI
import uvicorn

#Next we create the application object using FastAPI

# Create the app object
app = FastAPI()

#. Load trained Pipeline
model = load_model('House_Data_2-pipeline')
# loading the trained model House_Data_2-pipeline

# uvicorn main:app --reload

import nest_asyncio

nest_asyncio.apply()

@app.post('/predict')
def predict(GrLivArea, YearBuilt, TotalBsmtSF, ExterQual_TA, Fireplaces_0,GarageArea):
    data = pd.DataFrame([GrLivArea, YearBuilt, TotalBsmtSF, ExterQual_TA, Fireplaces_0,GarageArea])
    data.columns = ['GrLivArea', 'YearBuilt', 'TotalBsmtSF', 'ExterQual_TA', 'Fireplaces_0','GarageArea']

    predictions = predict_model(model, data=data) 
    return {'prediction': int(predictions['Label'][0])}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

