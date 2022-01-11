import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib import dates as mpl_dates

# import Data from files
bit_2017 = pd.read_csv(r"Bitcoin_2017.csv")
bit_2018 = pd.read_csv(r"Bitcoin_2018.csv")
bit_2019 = pd.read_csv(r"Bitcoin_2019.csv")
bit_2020 = pd.read_csv(r"Bitcoin_2020.csv")
bit_2021 = pd.read_csv(r"Bitcoin_2021.csv")
all_bitcoin = [bit_2017,bit_2018, bit_2019, bit_2020, bit_2021]
bit_df = pd.concat(all_bitcoin, ignore_index=True)

# All datatypes from the file are being recognized as objects. This needs to be changed to integers
# and dates Leaving them as their current data type can be limiting,
# because there are special packages and functions that are unique to certain data types.

# This function removes the comma from the prices and converts it into an integer


def tonum(name):
    name = int(name.replace(',', ''))
    return name

# This  function takes a dataframe as an argument and converts all of the columns to the correct data type by
# converting the date into a date data type and the prices into integers


def changedtype(df):
    list = df.columns
    for i in range(len(list)):
        if list[i] == "Date":
            df[list[i]] = pd.to_datetime(df[list[i]])
        else:
            df[list[i]] = df[list[i]].apply(tonum)
    # This sets all dates in the correct order
    df.sort_values("Date", inplace=True)
    return df.info()


# Makes use of the function above
changedtype(bit_df)

# This function takes on a dataframe as an argument and
# gets the max and min closing price, as well as the day it occured
# it returns a list of lists where the first list contains the max and min price
# and the second list contains the max and min date respectively
def getmaxima(df):
    prices = []
    dates = []
    prices.append(df["Close"].max())
    dates.append(df.loc[df["Close"] == prices[0]]["Date"].item())
    prices.append(df["Close"].min())
    dates.append(df.loc[df["Close"] == prices[1]]["Date"].item())
    max_and_min = np.array([prices, dates])
    print()
    return max_and_min


# This is where the max and min get stored
orderpairs = getmaxima(bit_df)

# Now tha the data is ready, we can visualize it. Just for kicks let's use
# seaborn style.Personal preference
plt.style.use("seaborn")

# Since this is a Time Series Analysis, the date belongs to the x-axis
date = bit_df["Date"]
close = bit_df["Close"]

plt.plot_date(date, close, linestyle="solid", label="Bitcoin Price")
plt.plot_date(orderpairs[1], orderpairs[0],
              linestyle="--", label="Price change")
plt.legend()
plt.title("Bitcoin Prices From 2017 until Now")
plt.xlabel("Dates")
plt.ylabel("Price in Dollars")

# Get current figure & format
plt.gcf().autofmt_xdate()

# This DateFormatter is used to control how the dates are displayed on the x-axis.
# Once the format is established we need to pass it to the axis
date_format = mpl_dates.DateFormatter("%b, %Y,")

# get current axis
plt.gca().xaxis.set_major_formatter(date_format)

# Now we can look at it:
plt.show()
