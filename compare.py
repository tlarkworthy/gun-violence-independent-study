#%%
import pandas
import numpy as np
import googlemaps
import datetime

# %%
df_kaggle = pandas.read_csv('gun-violence-data_01-2013_03-2018.csv')
df_ppd = pandas.read_csv('ppdshootings2018.csv')
df_kaggle = df_kaggle.replace(np.nan, '', regex=True)
df_ppd = df_ppd.replace(np.nan, '', regex=True)

# %%
gmaps = googlemaps.Client(key='AIzaSyBLpT1VXgEu8-4fTERh4a4XBLFm3blOE1U')

# %%
def get_lat(addr):
    try:
        return gmaps.geocode(addr)[0]['geometry']['location']['lat']
    except:
        return None

# %%
def convert_date(datestring):
    x = datestring[:-5].split('/')

    year = '20' + x[2]
    month = '0' + x[0] if len(x[0]) < 2 else x[0]
    day = '0' + x[1] if len(x[1]) < 2 else x[1]

    return year + '-' + month + '-' + day



# %%
df_joined = pandas.merge(df_ppd, df_kaggle, on='date', how='left')

# %%
df_joined = df_joined[df_joined['city_or_county'] == 'Philadelphia']

# %%
def compare_addr(x):
    addr = x['address']
    if addr == x['Address']:
        return True
    
    try:
        loc = gmaps.geocode(addr)[0]['geometry']['location']
        x_lat = float(x['lat'])
        x_lng = float(x['lng'])
    except:
        return False
    
    return abs(loc['lat'] - x_lat) < 1e-3 and abs(loc['lng'] - x_lng) < 1e-3


# %%
df_joined[df_joined.apply(compare_addr, axis=1)]
