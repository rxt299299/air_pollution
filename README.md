# air_pollution
**Scripts for Air Pollution project**

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
  
