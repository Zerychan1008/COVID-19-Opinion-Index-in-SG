# -*- coding: utf-8 -*-
"""Analyze.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P9Di4ufgDpJ5yEQXbW7Gm_ssoSuXjy4-
"""

# from google.colab import drive
# drive.mount('/content/drive')

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
# df_result = pd.read_csv("/content/drive/My Drive/covid19sg_project/sentiment_attention.csv", index_col=None)
df_result = pd.read_csv("sentiment_attention.csv", index_col=None)
df_result.datetime = pd.to_datetime(df_result.datetime)
df_result.head()

dates = df_result.datetime.tolist()
num_days = 182

"""##  Read Daily Cases

https://data.world/hxchua/covid-19-singapore
"""

df_case = pd.read_csv("Covid-19-SG.csv")
df_case.Date = df_case.Date.apply(lambda x: x + ", 2020")
df_case.Date =  pd.to_datetime(df_case.Date)
df_used = df_case[["Date", "Daily Confirmed ", "Daily Discharged"]]
df_used.rename(columns={"Date": "datetime", 
                        "Daily Confirmed ":"daily_case",
                        "Daily Discharged":"daily_disarged"}, inplace=True)
df_final = pd.merge(df_result, df_used, on='datetime', how='outer')
df_final.fillna(value=0, inplace=True)
df_final.set_index("datetime", inplace=True)



idx = np.arange(0, num_days, int(num_days/20))
xticks = [dates[ele].date() for ele in idx]

import matplotlib.pyplot as plt

fig, ax=plt.subplots(figsize=(15,7))
ax.plot(np.arange(0, num_days), df_final.Senti.tolist())
ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax.set_title("Sentiment Index")

fig, ax=plt.subplots(figsize=(15,7))
ax.plot(np.arange(0, num_days), df_final.attention.tolist())
ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax.set_title("Attention Index")

fig, ax=plt.subplots(figsize=(15,7))
ax.plot(np.arange(0, num_days), df_final.daily_case.tolist())
ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax.set_title("Daily Confirmed Case")

fig, ax=plt.subplots(figsize=(15,7))
ax.plot(np.arange(0, num_days), df_final.daily_disarged.tolist())
ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax.set_title("Daily Discharged Case")


# leisure_index
fig, ax=plt.subplots(figsize=(15,7))

ax.plot(np.arange(0, num_days), df_final.daily_case, color="red", marker="o")
ax.set_ylabel("Daily Confirmed Case",color="red",fontsize=14)

ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(np.arange(0, num_days), df_final.attention,color="blue",marker="o")
ax2.set_ylabel("Attention Index",color="blue",fontsize=14)

fig.savefig('attenion_dailycase.png',
            format='png',
            dpi=100,
            bbox_inches='tight')


fig, ax=plt.subplots(figsize=(15,7))

ax.plot(np.arange(0, 15), df_final.daily_case[:15], color="red", marker="o")
ax.set_ylabel("Daily Confirmed Case",color="red",fontsize=14)

ax.set_xticks(idx)
ax.set_xticklabels(xticks[:15], rotation=45)
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(np.arange(0, 15), df_final.attention[:15],color="blue",marker="o")
ax2.set_ylabel("Attention Index",color="blue",fontsize=14)

fig.savefig('short_attention_dailycase.png',
            format='png',
            dpi=100,
            bbox_inches='tight')



fig, ax=plt.subplots(figsize=(15,7))

ax.plot(np.arange(0, num_days), df_final.daily_case, color="red", marker="o")
ax.set_ylabel("Daily Confirmed Case",color="red",fontsize=14)

ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(np.arange(0, num_days), df_final.Senti,color="blue",marker="o")
ax2.set_ylabel("Sentiment Index",color="blue",fontsize=14)

fig.savefig('senti_dailycase.png',
            format='png',
            dpi=100,
            bbox_inches='tight')

fig, ax=plt.subplots(figsize=(15,7))

ax.plot(np.arange(0, num_days), df_final.attention, color="red", marker="o")
ax.set_ylabel("Attention",color="red",fontsize=14)

ax.set_xticks(idx)
ax.set_xticklabels(xticks, rotation=45)
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(np.arange(0, num_days), df_final.Senti,color="blue",marker="o")
ax2.set_ylabel("Sentiment Index",color="blue",fontsize=14)

fig.savefig('senti_attention.png',
            format='png',
            dpi=100,
            bbox_inches='tight')

#%%
"""## Correlation Analysis"""

df_sector = pd.read_csv("sgx.csv")
df_sector.rename(columns={"daily return": "datetime"}, inplace=True)
df_sector.datetime = pd.to_datetime(df_sector.datetime, format="%m/%d/%Y")
df_sector.set_index("datetime", inplace=True)

df_sector = df_sector['2020-01-21':]

df_sector.head()

industrs = ['reits', 'leisure', 'consumer', 'property', 'finance',
       'electronic manufacture', 'traditional manufacture', 'transportation',
       'retail', 'health product manufacture', 'medical & hospital']
"choose all necessary items to compare with attention"
BASE = 100
output_cols = []
for ind in industrs:
    rtns = df_sector[ind].tolist()
    index = [100]
    for rt in rtns:
        number = float(rt.split('%')[0])
        index.append(index[-1]*(1+number/100.0)) #deal with percentile numbers
    in_col = "{}_index".format(ind)
    df_sector[in_col] = index[1:]
    output_cols.append("{}_index".format(ind))

df_sectorindex = df_sector[output_cols]

df_sectorindex.head()

df_all = pd.merge(df_sectorindex, df_final, on='datetime')

df_all.head()

df_all.reset_index(inplace=True)

# rename of df_all columns
map_dict = {'reits_index':'REITS_index',
            'leisure_index':'Leisure & Entertainment_index',
            'consumer_index':'Consumer_index',
            'property_index':'Property_index',
            'finance_index':'Finance_index',
            'electronic manufacture_index':'Electronics Manufacturing_index',
            'traditional manufacture_index':'Traditional Manufacturing & Supply_index',
            'transportation_index':'Transportation_index',
            'retail_index':'Retail Trade & Services_index',
            'health product manufacture_index':'Health Products & Manufacturing_index',
            'medical & hospital_index':'Medical & Hospital Services_index'}
industry_newname = list(map_dict.values())

df_all.rename(columns=map_dict, inplace = True)

"""## Correlation Visualization"""
'''
# leisure_index
fig, ax=plt.subplots(figsize=(15,7))
df_all.leisure_index.plot(ax=ax, style='b-', legend=True)
# same ax as above since it's automatically added on the right
df_all.attention.plot(ax=ax, style='r-', secondary_y=True, legend=True)

# finance_index
fig, ax=plt.subplots(figsize=(15,7))
df_all.finance_index.plot(ax=ax, style='b-', legend=True)
# same ax as above since it's automatically added on the right
df_all.attention.plot(ax=ax, style='r-', secondary_y=True, legend=True)
'''
peak_index = df_all.attention.argmax()
result = []
for ele in industry_newname:
    fig, ax=plt.subplots(figsize=(15,7))
    df_all[ele].plot(ax=ax, style='b-', legend=True)
    # same ax as above since it's automatically added on the rightt
    df_all.attention.plot(ax=ax, style='r-', secondary_y=True, legend=True)
    plt.axvline(x=peak_index, ymin=0.0, ymax=0.99, color="grey", linewidth=4, linestyle='-.')
    #df_all.attention.diff().plot(ax=ax, style='g-', secondary_y=True, legend=True)
    corr_ele_drop = pearsonr(df_all.attention.iloc[:peak_index], df_all[ele].iloc[:peak_index])
    corr_ele_rebound = pearsonr(df_all.attention.iloc[peak_index:], df_all[ele].iloc[peak_index:])
    drop_ele = df_all[ele].iloc[peak_index] - df_all[ele].iloc[0]
    rebound_ele = df_all[ele].iloc[-1] - df_all[ele].iloc[peak_index]
    num_days = df_all.shape[0]
    idx = np.arange(0, num_days, int(num_days/20))
    dates = df_all.datetime.tolist()
    xticks = [dates[ele].date() for ele in idx]
    ax.set_xticks(idx)
    ax.set_xticklabels(xticks, rotation=45)
    ratio = -rebound_ele/drop_ele
    lag_peak = df_all[ele].argmin()-peak_index
    plt.title('corr_drop: {}, corr_reboud: {}, drop: {}%, rebound: {}%, ratio: {}'.format(round(corr_ele_drop[0],2), round(corr_ele_rebound[0],2),round(drop_ele,2), round(rebound_ele,2), round(ratio,2)))
    plt.savefig('attention_'+ele+'.png')
    print(ele)
#    if "traditional" in ele:
#        ele = ele + " & Supply"
    result.append([ele.capitalize(), round(corr_ele_drop[0], 2), round(corr_ele_rebound[0], 2),round(drop_ele, 2), round(rebound_ele,2), round(ratio,2), round(lag_peak,2)])
    
result = pd.DataFrame(result)
result.columns=['Sector','Drop Correlation','Rebound Correlation','Drop Percentage(%)','Rebound Percentage(%)','Return Ratio','Time Lag(Days)' ]
result.to_csv('sector_result.csv', index = None )
"""## Correlation Computation"""

corr_table = df_all.iloc[:,list(range(1,12))+[13]].corr()
corr_table = round(corr_table,2)
corr_table.to_csv('correlation_update.csv')
