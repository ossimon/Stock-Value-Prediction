import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

log_file = "../logs/EURUSD=X-2023-01-01-2024-01-01-42-logs.csv"

df = pd.read_csv(log_file)

# plot a very big graph with dates on x-axis and budget on y-axis
plt.figure(figsize=(20, 6))
plt.plot(df["date"], df["cost"], linestyle="-")

# Add colored points
colors = df["bought_stocks"]
scatter = plt.scatter(df["date"], df["cost"], norm=mcolors.TwoSlopeNorm(0), c=colors, cmap='seismic_r')
cbar = plt.colorbar(scatter)
cbar.set_label('Stocks transactions')

plt.xlabel("Date")
plt.xticks([], rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()
plt.show()