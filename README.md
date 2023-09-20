# air_pollution
**Air pollutant dispersion in street canyons**
## Background
Air pollution caused by the heavy emissions from vehicles can easily become trapped in city streets with limited airflow, posing a significant risk to public health and emerging as a critical concern. To effectively manage air quality in these urban "hotspots," there is a pressing need to gain a clearer understanding of how these pollutants behave and to develop practical tools for evaluating air quality improvement efforts.

## Project Aim
The main objective of this endeavor is to figure out how urban canyons affect air quality and, more importantly, how we can use fancy machine learning and economic modeling to unravel the secrets behind it. 
1. Our initial task involves crafting some cool methods that bring together different fields of study to help us crack the code of how city streets shape air quality. We're zooming in on pollutants like NOx and NO2 – NOx is like a silent observer while NO2 gets into chemistry shenanigans with NOx-O3 and VOC radicals. By comparing NO2 and NOx, we can learn how the atmosphere plays its part in our computer-based air quality simulations.
2. We're turning to a speedy machine learning model to help us decipher how stuff like environmental actions and day-to-day city life affect the air in your average street canyon. We'll dig deep into what really matters, like how much traffic there is and what kinds of vehicles are zooming around, all of which are like puzzle pieces for our model. To put this to the test, we'll use data from COVID-19 lockdowns as a real-life example.
3. Ever wondered how many cars a regular city street can handle without turning the air all smoggy, even during super windy days? We're on a mission to find out. We'll be digging into how people and traffic react in these conditions, spotting shifts in transportation habits, and figuring out just how much leeway there is for traffic without causing air quality havoc in our cities.

## Data Collection
We're rounding up a bunch of info for our research. That includes air pollution numbers from London's Marylebone Road and North Kensington over the past decade, along with weather data like wind speed, temperature, and more. Plus, we're also counting how many cars drive through these areas.

## Model Development
When it comes to making models for predicting air pollution, we used LightGBM, which not only makes our predictions more accurate but also does it faster than other methods. Plus, we've tweaked and fine-tuned it to work like a charm, even with large and complex datasets. In this project, we'll be customizing a LightGBM regression model specifically for air pollution levels, taking into account various weather factors and pollution sources.

## Model Evaluation
To check how well our nifty ML model is doing, we're using some math tricks like root-mean-square error (RMSE) and the index of agreement (IOA). These will help us see if our model is on point. A comprehensive comparison between our model and a process-based multi-box model for street canyon simulations will be provided.

## Preprocess
### Step 1:
- preprocess/data_check_columns: for all sites, check the missing columns in each site

### Step 2:
- preprocess/data_preprocess:
  - data preprocess before feature engineering, join the site info and extract included x and y features for each site
  - for each air pollution, save the union dataframes for related sites

### Step 3:
- preprocess/analysis_before_feature_engineering:
  - check missing values ratio 
  - check if exists rows missing all values for any group(see example weather group)
  
  
## Features engineering & Training
### Step 1:
- feature_engineering: 
  - extract column year
  - fill missing values
  - add cross validation column (not used in this version)

### Step 2:
- lightgbm_training_tuning.py:
  - tuning and find the best combination of hpyer parameters for each air pollution model training
  - save the best config
  - https://app.neptune.ai/rxt299299/airpollution/

### Step 3:
- training_with_best_configs:
  - load the best hyper parameters config
  - training model use the best config and save the model and performance
  - for each site, compare the performance between individual model(site level) and overall model
  
  
## References
- https://towardsdatascience.com/lets-do-feature-engineering-5731efc3d7fe
- https://neptune.ai/blog/lightgbm-parameters-guide
- https://docs.neptune.ai/integrations/lightgbm/
  
