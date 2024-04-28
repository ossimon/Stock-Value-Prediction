import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../logs_1_1_1.csv")

# plot a very big graph with dates on x-axis and budget on y-axis
plt.figure(figsize=(20, 6))
plt.plot(df["date"], df["cost"], linestyle="-")

# Add colored points
colors = [
    "red" if bought_stocks <= 0 else "green" for bought_stocks in df["bought_stocks"]
]
plt.scatter(df["date"], df["cost"], c=colors)

plt.xlabel("Date")
plt.xticks([], rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()
plt.show()
