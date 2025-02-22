import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

# ============================
# 1. Load and prepare data
# ============================
data = pd.read_csv('data.csv', parse_dates=['date'])

# Sort data by date if not already sorted
data.sort_values('date', inplace=True)

# Set the date column as the index
data.set_index('date', inplace=True)

# ============================
# 2. Calculate differences
# ============================
# 'diff()' gives the change in impressions since the previous timestamp
data['diff'] = data['impressions'].diff()

# ============================
# 3. Detect "significant bursts"
# ============================
# Rolling window size for computing the mean and std of 'diff'
window_size = 5  # try smaller or larger if you want more/less sensitivity
rolling_mean = data['diff'].rolling(window_size).mean()
rolling_std = data['diff'].rolling(window_size).std()

# Define threshold: for example, any jump > mean + 2*std is "significant"
N = 2
threshold = rolling_mean + (N * rolling_std)

# Identify bursts
bursts = data[data['diff'] > threshold]

# ============================
# 4. Plot the data
# ============================
plt.figure(figsize=(10, 5))

# Plot the impressions in a goldenrod color
plt.plot(data.index, data['impressions'], color='#DAA520', label='Impressions')

# Mark bursts in red with an "X"
plt.scatter(bursts.index, bursts['impressions'], color='red', marker='x', s=100, zorder=5, label='Significant Growth')

# ============================
# 5. Formatting
# ============================
# Calculate interval for ~10 evenly spaced x-axis labels
date_range = (data.index.max() - data.index.min()).days
interval = max(1, math.ceil(date_range / 10))

# Set up date formatting on the x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))
plt.gcf().autofmt_xdate()

# Add a dashed grid in light gray
plt.grid(True, linestyle='--', color='lightgray')

# Title and labels
plt.title('Impressions with Significant Growth Bursts')
plt.xlabel('Date')
plt.ylabel('Impressions')
plt.legend()

# Optionally annotate the most recent value
most_recent_value = data['impressions'].iloc[-1]
x_coord = data.index[-1]
y_coord = max(data['impressions']) * 0.8
plt.text(x_coord, y_coord, str(most_recent_value), fontsize=20, ha='center')

# Save the figure
plt.savefig('graph.png')
