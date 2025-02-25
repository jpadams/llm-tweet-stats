import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

# ============================
# 1. Load and prepare data
# ============================
data = pd.read_csv('data.csv', parse_dates=['date'])
data.sort_values('date', inplace=True)
data.set_index('date', inplace=True)

# ============================
# 2. Calculate slopes
# ============================
# Compute time differences in minutes between consecutive points
time_diff = data.index.to_series().diff().dt.total_seconds() / 60

# Compute the slope (impressions per minute) between consecutive points
data['slope'] = data['impressions'].diff() / time_diff

# ============================
# 3. Calculate difference in slopes ("slope_diff")
# ============================
# This shows how much the slope changes between consecutive intervals
data['slope_diff'] = data['slope'].diff()

# Set a threshold for a "sharp" increase in slope (here, 8 impressions/minute)
slope_threshold = 8
bursts = data[data['slope_diff'] > slope_threshold]

# ============================
# 4. Determine markers using previous points
# ============================
# For each burst, we'll use the point immediately preceding it (if available)
burst_marker_dates = []
burst_marker_impressions = []

for burst_dt in bursts.index:
    pos = data.index.get_loc(burst_dt)
    if pos > 0:  # Check that there is a previous point
        prev_dt = data.index[pos - 1]
        burst_marker_dates.append(prev_dt)
        burst_marker_impressions.append(data.loc[prev_dt, 'impressions'])

# ============================
# 5. Plot the data
# ============================
plt.figure(figsize=(10, 5))

# Plot the impressions in a goldenrod color
plt.plot(data.index, data['impressions'], color='#DAA520', label='Impressions')

# Mark burst markers in red with an "X"
plt.scatter(burst_marker_dates, burst_marker_impressions,
            color='red', marker='x', s=100, zorder=3, label='Sharp Increase)')

# Annotate each burst marker with its datetime
for dt in burst_marker_dates:
    annotation = dt.strftime('%Y-%m-%d %H:%M')
    plt.text(dt, data.loc[dt, 'impressions'], annotation, fontsize=8, rotation=45)

# ============================
# 6. Formatting
# ============================
# Calculate interval for ~10 evenly spaced x-axis labels
date_range = (data.index.max() - data.index.min()).days
interval = max(1, math.ceil(date_range / 10))

# Set up date formatting on the x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))
plt.gcf().autofmt_xdate()

plt.title('Impressions with Sharp Increase in Slope')
plt.xlabel('Date')
plt.ylabel('Impressions')
plt.legend()
plt.grid(True, linestyle='--', color='lightgray')
plt.tight_layout()

# Optionally annotate the most recent value
most_recent_value = data['impressions'].iloc[-1]
x_coord = data.index[-1]
y_coord = max(data['impressions']) * 0.8
plt.text(x_coord, y_coord, str(most_recent_value), fontsize=20, ha='center')

# Save and display the figure
plt.savefig('graph.png')
