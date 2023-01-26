air_pollutions = ["nox", "no2", "no", "o3", "pm2.5", "pm10"]
weathers = ["ws", "wd", "temp", "RH"]
weathers_2 = ["ssr", "tp", "blh", "tcc", "sp"]
times = ["date_unix", "week", "weekday", "hour", "month", "day_julian"]
optional_x = ["o3"]


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
    "o3",
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

sites_name_with_o3 = [
    "AstonHill",
    "BirminghamA4540",
    "BristolStPauls",
    "LeedsCentre",
    "MaryleboneRoad",
    "NorthKensington",
]


site_info_columns = ["ap_lat", "ap_long", "MetCode", "met_lat", "met_long", "site"]
#'ap_lat', 'ap_long', 'MetCode', 'met_lat','met_long', 'site'

site_info_dict = {
    "MY1": {
        "ap_lat": 51.52253,
        "ap_long": -0.154611,
        "MetCode": 37720,
        "met_lat": 51.479166667,
        "met_long": -0.450555556,
        "site": "UT",
    },
    "KC1": {
        "ap_lat": 51.52105,
        "ap_long": -0.213492,
        "MetCode": 37720,
        "met_lat": 51.479166667,
        "met_long": -0.450555556,
        "site": "UB",
    },
    "BIRR": {
        "ap_lat": 52.47614,
        "ap_long": -1.874978,
        "MetCode": 35340,
        "met_lat": 52.453889,
        "met_long": -1.748056,
        "site": "UT",
    },
    "BRS8": {
        "ap_lat": 51.462839,
        "ap_long": -2.584482,
        "MetCode": 37243,
        "met_lat": 51.382778,
        "met_long": -2.719167,
        "site": "UB",
    },
    "LED6": {
        "ap_lat": 53.81997,
        "ap_long": -1.576361,
        "MetCode": 33463,
        "met_lat": 53.611666667,
        "met_long": -1.666944444,
        "site": "UT",
    },
    "LEED": {
        "ap_lat": 53.80378,
        "ap_long": -1.546472,
        "MetCode": 33463,
        "met_lat": 53.611666667,
        "met_long": -1.666944444,
        "site": "UB",
    },
    "ABD7": {
        "ap_lat": 57.14455,
        "ap_long": -2.106472,
        "MetCode": 30910,
        "met_lat": 57.205,
        "met_long": -2.205277778,
        "site": "UT",
    },
    "AH": {
        "ap_lat": 52.50385,
        "ap_long": -3.034178,
        "MetCode": 35200,
        "met_lat": 52.243055556,
        "met_long": -2.885833333,
        "site": "RB",
    },
    "SCN2": {
        "ap_lat": 53.58634,
        "ap_long": -0.636811,
        "MetCode": 33735,
        "met_lat": 53.306944444,
        "met_long": -0.548055556,
        "site": "UI",
    },
    "YK11": {
        "ap_lat": 53.95189,
        "ap_long": -1.075861,
        "MetCode": 32660,
        "met_lat": 54.043590989,
        "met_long": -1.250316066,
        "site": "UT",
    },
}
