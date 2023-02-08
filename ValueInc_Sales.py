#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 13:55:11 2023

"""

import pandas as pd


# Importing data
data = pd.read_csv('transaction.csv', sep=';')


# Getting summary of the data
data.info()


# Cost Per Transaction Column Calculation
# CPT = CPI * NIP
# variable = dataframe['column_name'}]
CostPerItem = data['CostPerItem']
NumberofItemsPurchased = data['NumberOfItemsPurchased']
CostPerTransaction = CostPerItem * NumberofItemsPurchased


# Adding new column to dataframe
data['CostPerTransaction'] = CostPerTransaction
data['CostPerTransaction'] = data['CostPerItem'] * data['NumberOfItemsPurchased']


# Adding sales per transaction column
data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']


# Adding profit per transation column
data['ProfitPerTransaction'] = data['SalesPerTransaction'] - data['CostPerTransaction']


# Adding markup = (sales-cost)/cost
data['Markup'] = ( data['SalesPerTransaction'] - data['CostPerTransaction'] ) / data['CostPerTransaction']
data['Markup'] = data['ProfitPerTransaction'] / data['CostPerTransaction']


# Rounding markup for format consistency
data['Markup'] = round(data['Markup'], 2)


# Checking column data types
print(data['Day'].dtype)


# Changing column types
data['Day'] = data['Day'].astype(str)
print(data['Day'].dtype)

data['Year'] = data['Year'].astype(str)
print(data['Year'].dtype)


# Adding Date column
data['Date'] = data['Day']+'-'+data['Month']+'-'+data['Year']


# Using split to separate client keywords column
# df[['NewColumn1', 'NewColumn2', ...]] = df['OriginalColumn'].str.split('sep' , expand = True)
data[['ClientAge', 'ClientType', 'LengthofContract']] = data['ClientKeywords'].str.split(',', expand = True)


# Using replace to clean up client columns
data['ClientAge'] = data['ClientAge'].str.replace('[' , '')
data['LengthofContract'] = data['LengthofContract'].str.replace(']' , '')


# Using the lower function to change item description to lowercase
data['ItemDescription'] = data['ItemDescription'].str.lower()


# Merging files <-- bringing in a seasonal dataset
seasons = pd.read_csv('value_inc_seasons.csv')
seasons = pd.read_csv('value_inc_seasons.csv', sep=';')


# Merging files: merge_df = pd.merge(df_old, df_new, on = 'common_column')
data = pd.merge(data, seasons, on = 'Month')

# Dropping Day, Month, Year, Client Keywords columns due to redundancy
# df = df.drop('columnname', axis = 1) <-- '1' is a column; '0' is a row
data = data.drop(['ClientKeywords', 'Day', 'Month', 'Year'], axis =1)


# Exporting data frame into csv
data.to_csv('ValueInc_Cleaned.csv', index = False)
# since there's a transaction ID to identify each unique row, we dno't need the index; otherwise we would set the index as True
