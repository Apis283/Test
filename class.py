import numpy as np
import time


"""The Loop Approach"""
# celsius_temps = [0, 10, 20, 30, 40, 50]
# fahrenheit_temps = []

# for temp in celsius_temps:
#     fahrenheit = (temp * 9/5) + 32
#     fahrenheit_temps.append(fahrenheit)

# print(fahrenheit_temps)

"""The Vectorized Approach"""
# celsius_temps = np.array([0, 10, 20, 30, 40, 50])
# fahrenheit_temps = (celsius_temps * 9/5) + 32

# print(fahrenheit_temps)

"""The Loop Approach"""
# revenues = [1000, 1500, 800, 2000, 1200]
# costs = [600, 900, 500, 1100, 700]
# tax_rates = [0.15, 0.18, 0.12, 0.20, 0.16]

# profits = []
# for i in range(len(revenues)):
#     gross_profit = revenues[i] - costs[i]
#     net_profit = gross_profit * (1 - tax_rates[i])
#     profits.append(net_profit)

# print(profits)

"""The Vectorized Approach"""
# revenues = np.array([1000, 1500, 800, 2000, 1200])
# costs = np.array([600, 900, 500, 1100, 700])
# tax_rates = np.array([0.15, 0.18, 0.12, 0.20, 0.16])

# gross_profits = revenues - costs
# net_profits = gross_profits * (1 - tax_rates)

# print(net_profits)


"""The Vectorized Approach"""
# Create a large dataset
size = 1000000
data = list(range(size))
np_data = np.array(data)

# Test loop-based approach
start_time = time.time()
result_loop = []
for x in data:
    result_loop.append(x ** 2 + 3 * x + 1)
loop_time = time.time() - start_time

# Test vectorized approach
start_time = time.time()
result_vector = np_data ** 2 + 3 * np_data + 1
vector_time = time.time() - start_time

print(f"Loop time: {loop_time:.4f} seconds")
print(f"Vector time: {vector_time:.4f} seconds")
print(f"Speedup: {loop_time / vector_time:.1f}x faster")