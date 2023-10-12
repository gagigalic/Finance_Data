import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import cufflinks as cf

start_data = datetime.datetime(2015, 1,1)
end_data = datetime.datetime(2022,1,1)

#HSBC Holdings plc
HSBC = yf.download("HSBC", start=start_data, end =end_data)

#Deutsche Bank Aktiengesellschaft
DB = yf.download("DB", start=start_data, end =end_data)

#BNP Paribas SA
BNP = yf.download("BNP.PA", start=start_data, end =end_data)

#Banco Santander, S.A.
SAN = yf.download("SAN", start=start_data, end =end_data)

#ING Groep N.V. (ING)
ING = yf.download("ING", start=start_data, end =end_data)

#Concat all
tickers = ["HSBC", "DB", "BNP", "SAN", "ING"]
bank_stocks = pd.concat([HSBC, DB, BNP, SAN, ING],axis = 1, keys=tickers)
bank_stocks.columns.names=["Bank Ticker", "Stock Info"]
print(bank_stocks.head())

#max close prise for each bank throughout time period
max_price =bank_stocks.xs(key = "Close", axis = 1, level = "Stock Info").max()
print(max_price)

#new DataFrame
returns = pd.DataFrame()

for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
print(returns.head())

#pairplot for returns
sns.pairplot(returns[1:])
plt.savefig("pairplot_returns.png")
plt.close()

# single min returns
min_returns = returns.min()
print(min_returns)

#Date (index) of the min values for the returns
date_of_min_returns = returns.idxmin()
print(date_of_min_returns)

#DB, BNP, SAN have min return on 24.06.2016,
#June 23, 2016: One of the most significant events of June 2016 was the United Kingdom's referendum on its membership in the European Union (EU), commonly referred to as "Brexit."

#Date (index) of the max values for the returns
date_of_max_returns =returns.idxmax()
print(date_of_max_returns)

#HSBC, BNP, SAN have max returns od 09.11.2020
#On November 9, 2020, Pfizer and BioNTech jointly announced promising results from their Phase 3 COVID-19 vaccine trials. They reported that their vaccine candidate was more than 90% effective in preventing COVID-19. This announcement had a significant impact on global financial markets, including the banking sector.

#standard deviations for 2020
std_2020 = returns.loc["2020-01-01":"2020-12-31"].std()
print(std_2020)


#Distplot using seaborn of the 2020 returns for ING Groep N.V.
sns.displot(returns.loc["2020-01-01":"2020-12-31"]["ING Return"], color = "green", bins = 50)
plt.savefig("ing_returns_2020.png")
plt.close()

#Line plot showing Close price for each bank for the entire index of time
bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()
plt.savefig("close_price.png")
plt.close()


#iplot, Close price
fig = bank_stocks.xs(key='Close',axis=1,level='Stock Info').iplot(asFigure=True)
fig.show()

#Plot the rolling 30 day average against the Close Price for  Deutsche Bank Aktiengesellschaft stock for the year 2020
plt.figure(figsize=(12,6))
DB['Close'].loc['2020-01-01':'2021-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
DB['Close'].loc['2020-01-01':'2021-01-01'].plot(label='DB CLOSE')
plt.legend()
plt.savefig("average.png")
plt.close()


#Heatmap of the correlation between the stocks Close Price
sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)
plt.savefig("heatmap.png")
plt.close()

#Clustermap
sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)
plt.savefig("cluster.png")
plt.close()

