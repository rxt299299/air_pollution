air_pollutions = ["nox", "no2", "no", "o3", "pm2.5", "pm10"]
weathers = ["ws", "wd", "temp", "RH"]
weathers_2 = ["ssr", "tp", "blh", "tcc", "sp", "tc"]
times = ["date_unix", "week", "weekday", "hour", "month", "day_julian"]


continuous_variables = [
    "ws",
    "wd",
    "temp",
    "RH",
    "ssr",
    "tp",
    "blh",
    "tcc",
    "sp",
    "ap_lat",
    "ap_long",
    "met_lat",
    "met_long",
    "date_unix",
    "year",
]

category_variables = [
    "ap_code",
    "MetCode",
    "site",
    "week",
    "weekday",
    "hour",
    "month",
    "day_julian",
]

percentile_variables = ["ws", "wd", "temp", "RH", "ssr", "tp", "blh", "tcc", "sp"]


FIXED_PARAMS = {
    "objective": "regression",
    "metric": "rmse",
    "bagging_freq": 5,
    "num_boost_round": 500,
    "early_stopping_rounds": 50,
    "min_data_in_leaf": 20,
    "min_sum_hessian_in_leaf": 1e-3,
    "lambda_l2": 2e-1,
}
