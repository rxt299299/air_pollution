# load the grouped list for colnames
from utils import (
    air_pollutions,
    continuous_variables,
    category_variables,
    FIXED_PARAMS
)


import lightgbm as lgb
import neptune
import pandas as pd
from sklearn.utils import shuffle
import skopt

import neptune.new as neptune
from neptune.new.integrations.lightgbm import NeptuneCallback
from sklearn.model_selection import train_test_split
import json
import numpy as np
from sklearn.metrics import mean_squared_error



class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


run = neptune.init(
    project="rxt299299/airpollution",
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIwMjE3NTFmOC03NGIxLTQ4ZGQtOGUzNC1hNGQ2MTFkMTZmMjgifQ==",
    name="nox",
    tags=["lgbm-integration", "cv"],
)  # your credentials

data_folder = (
    "/home/mibao/work/air_pollution/data-overall-update/"
    "data_process/after_engineer/union_per_pollution/"
)

features_names = continuous_variables + category_variables
boosting_type = "gbdt"  # gbdt, dart, goss


SEARCH_PARAMS = {
    "learning_rate": 0.2,
    "max_depth": 15,
    "num_leaves": 32,
    "feature_fraction": 0.8,
    "subsample": 0.2,
    #'reg_sqrt':False
}

SPACE = [
    skopt.space.Real(0.01, 0.2, name="learning_rate", prior="log-uniform"),
    skopt.space.Integer(1, 30, name="max_depth"),
    skopt.space.Integer(10, 200, name="num_leaves"),
    skopt.space.Real(0.1, 1.0, name="feature_fraction", prior="uniform"),
    skopt.space.Real(0.1, 1.0, name="subsample", prior="uniform"),
    # skopt.space.Boolean(True, False, name='reg_sqrt')
]

n_calls_ = 100

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

    SEARCH_PARAMS = {
        **SEARCH_PARAMS,
        **{"skip_drop": 0.5, "max_drop": 50, "drop_rate": 0.1},
    }
    SPACE += [
        skopt.space.Real(0.2, 0.8, name="skip_drop", prior="uniform"),
        skopt.space.Integer(20, 80, name="max_drop", prior="uniform"),
        skopt.space.Real(0.05, 0.2, name="drop_rate", prior="uniform"),
    ]
    n_calls_ = 30

elif boosting_type == "goss":
    FIXED_PARAMS = {
        **FIXED_PARAMS,
        **{"boosting": "gbdt", "data_sample_strategy": "goss",},
    }

    SEARCH_PARAMS = {**SEARCH_PARAMS, **{"top_rate": 0.2, "other_rate": 0.1,}}

    SPACE += [
        skopt.space.Real(0.1, 0.4, name="top_rate", prior="uniform"),
        skopt.space.Real(0.05, 0.2, name="other_rate", prior="uniform"),
    ]


def train_evaluate(search_params):
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

    # set parameters for training
    params = {**FIXED_PARAMS, **search_params}

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

    predict_y = model.predict(X_valid)

    return mean_squared_error(y_true=y_valid, y_pred=predict_y)


for air_pollution in air_pollutions:
    df = pd.read_csv(data_folder + air_pollution + "_unionSites.csv")
    # df = df.head(1000)
    df = shuffle(df)

    X = df.copy()

    target_name = X.columns[1]

    X = X.reset_index()
    X = X.drop(["level_0", "index"], axis=1)
    cv = X.pop("cv_fold")
    target_y = X.pop(target_name)

    for c in category_variables:
        X[c] = X[c].astype("category")

    @skopt.utils.use_named_args(SPACE)
    def objective(**params):
        return train_evaluate(params)

    results = skopt.forest_minimize(
        objective, SPACE, n_calls=n_calls_, n_random_starts=10
    )

    search_params = [
        "learning_rate",
        "max_depth",
        "num_leaves",
        "feature_fraction",
        "subsample",
    ]
    if boosting_type == "dart":
        search_params += ["skip_drop", "max_drop", "drop_rate"]
    elif boosting_type == "goss":
        search_params += ["top_rate", "other_rate"]

    best_paras = dict(zip(search_params, results.x))

    best_paras = {**{"mse": results.fun,}, **best_paras}

    with open(
        "best_experiments/" + boosting_type + "/" + air_pollution + "_best_paras.json",
        "w",
    ) as outfile:
        json.dump(best_paras, outfile, cls=NpEncoder)
