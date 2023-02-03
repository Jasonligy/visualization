import pandas as pd
import numpy as np

airbnb = pd.read_csv('airbnb_open_data.csv')
#replace the space by the _ for all column
airbnb.columns=[col.lower().replace(" ","_") for col in airbnb.columns]
# remove the dallar sign
def remove_dollar_sign(value):
    if pd.isna(value):
        return np.NaN
    else:
        return float(value.replace("$","").replace(",","").replace(" ",""))

airbnb["price"]=airbnb["price"].apply(lambda x: remove_dollar_sign(x))
airbnb["service_fee"]=airbnb["service_fee"].apply(lambda x: remove_dollar_sign(x))

#compute the mean price of each neighbourhood
airbnb['nei_price'] = airbnb['price'].groupby(airbnb['neighbourhood']).transform('mean')
#compute the age of properties
airbnb['age'] = 2023 - airbnb['construction_year']
airbnb.to_csv('preprocessed.csv')
