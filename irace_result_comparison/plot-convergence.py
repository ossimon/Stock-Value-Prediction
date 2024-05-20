import pandas as pd
import matplotlib.pyplot as plt

# Load the data
default_params = pd.read_csv('../reports/data/default_params-usd-eur-23-24-200000-evals.csv')
irace_optimized = pd.read_csv('../reports/data/meta_prams-usd-eur-23-24-200000-evals.csv')
default_x = default_params['evaluation']
print(default_params.columns)
default_y = -1 * default_params['bestever'] - 1e6

irace_x = irace_optimized['evaluation']
irace_y = -1 * irace_optimized['bestever'] - 1e6

# set figure size to 10x6
plt.figure(figsize=(7, 4))

# Plot the data
plt.plot(default_x, default_y, label='Domyślne Parametry')
plt.plot(irace_x, irace_y, label='Parametry Zoptymalizowane przez iRACE')
plt.xlabel('Ewaluacja')
plt.ylabel('Zysk [PLN]')

plt.axvline(x=10000, c='r', linestyle='--', label='Liczba ewaluacji użyta w irace')

plt.legend()
plt.title('Porównanie zysku na kursie USD w zależności od ewaluacji')

# Save the plot
plt.savefig('Profit comparison.jpg')

# Display the plot
plt.show()
