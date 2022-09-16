import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import kotirovka as kt

plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')
df = pd.read_csv(kt.GAZPROM, sep=';')
# Set the date as the index


# # график
# plt.figure(figsize=(12.2, 4.5))  # width = 12.2in, height = 4.5
# plt.plot(df['<CLOSE>'], label='Close Price')  # plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
# plt.title('Close Price History')
# plt.xlabel('Date', fontsize=18)
# plt.ylabel('Close Price USD ($)', fontsize=18)
# plt.legend(df.columns.values, loc='upper left')
# plt.show()

# подсчет индекса mfi
typical_price = (df['<CLOSE>'] + df['<HIGH>'] + df['<LOW>']) / 3
period = 14
money_flow = typical_price * df['<VOL>']

positive_flow = []  # Create a empty list called positive flow
negative_flow = []  # Create a empty list called negative flow
# Loop through the typical price
for i in range(1, len(typical_price)):
    if typical_price[i] > typical_price[i - 1]:  # if the present typical price is greater than yesterdays typical price
        positive_flow.append(money_flow[i - 1])  # Then append money flow at position i-1 to the positive flow list
        negative_flow.append(0)  # Append 0 to the negative flow list
    elif typical_price[i] < typical_price[i - 1]:  # if the present typical price is less than yesterdays typical price
        negative_flow.append(money_flow[i - 1])  # Then append money flow at position i-1 to negative flow list
        positive_flow.append(0)  # Append 0 to the positive flow list
    else:  # Append 0 if the present typical price is equal to yesterdays typical price
        positive_flow.append(0)
        negative_flow.append(0)

positive_mf = []
negative_mf = []
for i in range(period - 1, len(positive_flow)):
    positive_mf.append(sum(positive_flow[i + 1 - period: i + 1]))
# Get all of the negative money flows within the time period
for i in range(period - 1, len(negative_flow)):
    negative_mf.append(sum(negative_flow[i + 1 - period: i + 1]))

mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))
df2 = pd.DataFrame()
df2['MFI'] = mfi
# Create and plot the graph
# plt.figure(figsize=(12.2, 4.5))  # width = 12.2in, height = 4.5
# plt.plot(df2['MFI'], label='MFI')  # plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
# plt.axhline(10, linestyle='--', color='orange')  # Over Sold line (Buy)
# plt.axhline(20, linestyle='--', color='blue')  # Over Sold Line (Buy)
# plt.axhline(80, linestyle='--', color='blue')  # Over Bought line (Sell)
# plt.axhline(90, linestyle='--', color='orange')  # Over Bought line (Sell)
# plt.title('MFI')
# plt.ylabel('MFI Values', fontsize=18)
# plt.legend(df2.columns.values, loc='upper left')
# plt.show()

new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi

def get_signal(data, high, low):
    buy_signal = []  # The stock was over sold
    sell_signal = []  # The stock was over bought

    for j in range(len(data['MFI'])):
        if data['MFI'][j+period] > high:  # Then the stock is over bought, you should sell
            buy_signal.append(np.nan)
            sell_signal.append(data['<CLOSE>'][j+period])
        elif data['MFI'][j+period] < low:  # Then the stock is over sold, you should buy
            buy_signal.append(data['<CLOSE>'][j+period])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
    return (buy_signal, sell_signal)


new_df['Buy'] = get_signal(new_df, 80, 20)[0]
new_df['Sell'] = get_signal(new_df, 80, 20)[1]
print(new_df)
# # Show the new dataframe
# plt.figure(figsize=(12.2,4.5))
# plt.plot(new_df.index, new_df['<CLOSE>'],alpha = 0.5, label='Close Price')
# plt.scatter(new_df.index, new_df['Buy'], color = 'green', label='Oversold/ Buy Signal', marker = '^', alpha = 1)
# plt.scatter(new_df.index, new_df['Sell'], color = 'red', label='Overbought/ Sell Signal', marker = 'v', alpha = 1)
# plt.title('Close Price')
# plt.xlabel('Date',fontsize=18)
# plt.xticks(rotation = 45)
# plt.ylabel('Close Price USD ($)',fontsize=18)
# plt.legend( loc='upper left')
# plt.show()
