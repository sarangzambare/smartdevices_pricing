import pandas as pd
import re
import numpy as np
from math import isnan


# importing scraped data
products_df = pd.read_csv("csv/smartdevices_data_full.csv")

# removing unwanted index column
products_df = products_df.drop("Unnamed: 0",axis=1)

#products_df.columns = Index([u'name', u'LTE', u'year', u'weight', u'display_type', u'screen_size',
#       u'ppi', u'cpu_ghz', u'ram', u'internal', u'camera', u'front_cam',
#       u'blth_v', u'battery', u'price'],
#      dtype='object')

# getting rid of all rows with at least one Nan
products_df = products_df.dropna(axis=0)

# exporting to csv
products_df.to_csv('csv/data_nomissing.csv')


# cleaning column year
for i in range(products_df.shape[0]):
    products_df.iloc[i,2] = products_df.iloc[i,2][:4]


products_df = products_df[products_df.year != 'Exp.']
products_df = products_df[products_df.year != 'Not ']



# cleaning column weight
products_df = products_df[products_df.weight != '-']

for i in range(products_df.shape[0]):

    products_df.iloc[i,3] = products_df.iloc[i,3][:3]
    products_df.iloc[i,3] = products_df.iloc[i,3].replace(".","")


# classifying all display into 3 broad types
for i in range(products_df.shape[0]):
    if('LCD' in products_df.iloc[i,4]):
        products_df.iloc[i,4] = 'LCD'
    elif('OLED' in products_df.iloc[i,4]):
        products_df.iloc[i,4] = 'OLED'
    else:
        products_df.iloc[i,4] = 'OTHER'

# cleaning column screen_size, units=inches
for i in range(products_df.shape[0]):
    products_df.iloc[i,5] = re.findall(r'.*\sinches',products_df.iloc[i,5])[0][:-7]


# cleaning column ppi, units=ppi
for i in range(products_df.shape[0]):
    products_df.iloc[i,6] = re.findall(r'\d{0,4}\.{0,1}\d{0,2}\sppi',products_df.iloc[i,6])[0][:-4]

# cleaning column cpu, units=GHz
for i in range(products_df.shape[0]):
    if(len(re.findall(r'\d{0,3}\.{0,1}\d{0,2}\sGHz',products_df.iloc[i,7])) != 0):
        products_df.iloc[i,7] = re.findall(r'\d{0,3}\.{0,1}\d{0,2}\sGHz',products_df.iloc[i,7])[0][:-4]
    elif(len(re.findall(r'\d{0,3}\.{0,1}\d{0,2}\sMHz',products_df.iloc[i,7])) != 0):
        products_df.iloc[i,7] = "0." + re.findall(r'\d{0,3}\.{0,1}\d{0,2}\sMHz',products_df.iloc[i,7])[0][:-4].replace(".","")
    else:
        products_df.iloc[i,7] = None

                   
