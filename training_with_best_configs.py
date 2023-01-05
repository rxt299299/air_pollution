# load the grouped list for colnames
from utils import air_pollutions
from utils import continuous_variables, category_variables
from utils import FIXED_PARAMS

import lightgbm as lgb
import json
import numpy as np
import math
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    explained_variance_score,
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    r2_score,
)

# functions
# metrics function
def model_metrics(y_true, predictions):

    pd.set_option("display.max_columns", None)

    # get base metrics
    base_metrics = {
        "Explained Variance (higher is better)": explained_variance_score(
            y_true=y_true, y_pred=predictions
        ),
        "Mean Absolute Error (lower is better)": mean_absolute_error(
            y_true=y_true, y_pred=predictions
        ),
        "Mean Squared Error (lower is better)": mean_squared_error(
            y_true=y_true, y_pred=predictions
        ),
        "R-squared Score (higher is better)": r2_score(
            y_true=y_true, y_pred=predictions
        ),
    }

    # convert to DataFrames
    results = pd.DataFrame(base_metrics, index=["Base Metrics"]).transpose()

    return results


# training function
def train_lgb(params, X):
    X_train, X_valid, y_train, y_valid = train_test_split(
        X[features_names],
        target_y,
        test_size=0.2,
        stratify=X.ap_code,
        random_state=1234,
    )
    # create the Dataset
    train_data = lgb.Dataset(
        data=X_train,
        label=y_train,
        feature_name=features_names,
        categorical_feature=category_variables,
    )

    valid_data = lgb.Dataset(
        data=X_valid,
        label=y_valid,
        feature_name=features_names,
        categorical_feature=category_variables,
    )

    # cross-validated model
    model = lgb.train(
        params=params,
        train_set=train_data,
        valid_sets=[valid_data],
        num_boost_round=FIXED_PARAMS["num_boost_round"],
        feature_name=features_names,
        categorical_feature=category_variables,
        early_stopping_rounds=FIXED_PARAMS["early_stopping_rounds"],
    )

    return model, X_train, y_train, X_valid, y_valid


# Inputs
best_exp_path = "/home/mibao/work/air_pollution/best_experiments/"

data_folder = (
    "/home/mibao/work/air_pollution/data-overall-update/"
    "data_process/after_engineer/union_per_pollution/"
)

model_metrics_output_path = "/home/mibao/work/air_pollution/models_metrics/"

boosting_type = "gbdt"
features_names = continuous_variables + category_variables

for air_pollution in air_pollutions:

    # load best experiments configs
    with open(
        best_exp_path + boosting_type + "/" + air_pollution + "_best_paras.json"
    ) as json_file:
        best_configs = json.load(json_file)

    best_MSE = best_configs["mse"]
    del best_configs["mse"]

    # combine fixed parameters and best parameters for each type of boosting

    if boosting_type == "gbdt":

        FIXED_PARAMS = {**FIXED_PARAMS, **{"boosting": "gbdt"}}

    elif boosting_type == "dart":

        FIXED_PARAMS = {
            **FIXED_PARAMS,
            **{
                "boosting": "dart",
                "drop_seed": 4,
                "uniform_drop": True,
                "xgboost_dart_mode": True,
            },
        }

    elif boosting_type == "goss":
        FIXED_PARAMS = {
            **FIXED_PARAMS,
            **{"boosting": "gbdt", "data_sample_strategy": "goss",},
        }

    params = {**FIXED_PARAMS, **best_configs}

    # load the dataset
    df = pd.read_csv(data_folder + air_pollution + "_unionSites.csv")
    df = shuffle(df)
    # df = df.head(50000)
    X = df.copy()

    # target y
    target_name = X.columns[1]

    X = X.reset_index()
    X = X.drop(["level_0", "index"], axis=1)
    cv = X.pop("cv_fold")
    target_y = X.pop(target_name)

    for c in category_variables:
        X[c] = X[c].astype("category")

    # start training
    model, X_train, y_train, X_valid, y_valid = train_lgb(params, X)

    # get the performance
    predict_y = model.predict(X_valid)
    df_metrics = model_metrics(y_valid, predict_y)

    ###################################
    # save performance metrics and model
    model.save_model(model_metrics_output_path + air_pollution + "_best_model.txt")
    df_metrics.to_csv(
        model_metrics_output_path
        + air_pollution
        + "_best_model_overall_performance.csv"
    )

    ################################################################################
    # 对比每个站点在overall model的performance和其在individual trained model的performance
    ################################################################################
    RMSE_dict = {}
    df_train = pd.concat([X_train, y_train], axis=1)
    df_valid = pd.concat([X_valid, y_valid], axis=1)

    for ap_code in df["ap_code"].unique():

        df_train_M = df_train[df_train["ap_code"] == ap_code]
        df_valid_M = df_valid[df_valid["ap_code"] == ap_code]

        # create the Dataset
        train_data_M = lgb.Dataset(
            data=df_train_M[features_names],
            label=df_train_M[air_pollution],
            feature_name=features_names,
            categorical_feature=category_variables,
        )

        valid_data_M = lgb.Dataset(
            data=df_valid_M[features_names],
            label=df_valid_M[air_pollution],
            feature_name=features_names,
            categorical_feature=category_variables,
        )

        # cross-validated model
        model_M = lgb.train(
            params=params,
            train_set=train_data_M,
            valid_sets=[valid_data_M],
            num_boost_round=FIXED_PARAMS["num_boost_round"],
            feature_name=features_names,
            categorical_feature=category_variables,
            early_stopping_rounds=FIXED_PARAMS["early_stopping_rounds"],
        )

        # performance on individual model:
        predict_y_M = model_M.predict(df_valid_M[features_names])
        individual_rmse = math.sqrt(
            mean_squared_error(y_true=df_valid_M[air_pollution], y_pred=predict_y_M)
        )

        # performance on overall model:
        predict_y_M_overall = model.predict(df_valid_M[features_names])
        overall_rmse = math.sqrt(
            mean_squared_error(
                y_true=df_valid_M[air_pollution], y_pred=predict_y_M_overall
            )
        )

        RMSE_dict[ap_code] = {
            "individual model": individual_rmse,
            "overall model": overall_rmse,
        }

    with open(
        model_metrics_output_path
        + air_pollution
        + "_sites_indiv_overall_model_compare.json",
        "w",
    ) as outfile:
        json.dump(RMSE_dict, outfile)
