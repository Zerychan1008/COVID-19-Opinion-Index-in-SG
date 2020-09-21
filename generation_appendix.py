# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 17:44:48 2020

@author: Zhao Rui
"""

import pandas as pd
import numpy as np
import yfinance as yf
#%%
xls = pd.ExcelFile('sgx.xlsx')
sheet_list = ['reits',
              'leisure',
              'consumer',
              'property',
              'finance',
              'elec',
              'trad',
              'trans',
              'retail',
              'health',
              'medical']

appendix_name=['REITS_index',
               'Leisure & Entertainment_index',
               'Consumer_index',
               'Property_index',
               'Finance_index',
               'Electronics Manufacturing_index',
               'Traditional Manufacturing & Supply_index',
               'Transportation_index',
               'Retail Trade & Services_index',
               'Health Products & Manufacturing_index',
               'Medical & Hospital Services_index']

for sheet in sheet_list:
    df = pd.read_excel(xls, sheet)