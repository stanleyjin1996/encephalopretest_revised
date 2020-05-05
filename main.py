# Encephalo Investments Coding Pre-Test - Revised April 2020

import pandas as pd
import numpy as np
import math


def cleanse_data(df):
    # Your task here is to remove data from any ticker that isn't XXY, sort chronologically and return a dataframe
    # whose only column is 'Adj Close'
    
    dfclean = df[df["Ticker"] == "XXY"].copy()
    dfclean["Date"] = pd.to_datetime(dfclean["Date"]) # Convert the string date to "datatime" object
    dfclean = dfclean.sort_values(by = ["Date"])["Adj Close"] # Sort chronologically
    return pd.DataFrame(dfclean)


def mc_sim(sims, days, df):
    # The code for a crude monte carlo simulation is given below. Your job is to extract the mean expected price
    # on the last day, as well as the 95% confidence interval.
    # Note that the z-score for a 95% confidence interval is 1.960
    returns = df.pct_change()
    last_price = df.iloc[-1]

    simulation_df = pd.DataFrame()

    for x in range(sims):
        count = 0
        daily_vol = returns.std()

        price_series = []

        price = last_price * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)

        for y in range(days):
            price = price_series[count] * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    # FILL OUT THE REST OF THE CODE. The above code has given you 'sims' of simulations run 'days' days into the future.
    # Your task is to return the expected price on the last day +/- the 95% confidence interval.
    
    expected_price = simulation_df.iloc[-1].mean() # Calculate the mean of last day price
    sigma = simulation_df.iloc[-1].std() # Calculate the standard deviation of last price
    upper = expected_price + 1.96*sigma/np.sqrt(sims) # The upper bound of 95% confidence interval
    lower = expected_price - 1.96*sigma/np.sqrt(sims) # The lower bound of 95% confidence interval
    
    return expected_price, upper, lower


def main():
    filename = '20192020histdata.csv'
    rawdata = pd.read_csv(filename)
    cleansed = cleanse_data(rawdata)
    simnum = 1000  # change this number to one that you deem appropriate
    days = 25
    expected_price, upper, lower = mc_sim(simnum, days, cleansed)
    return


if __name__ == '__main__':
    main()
