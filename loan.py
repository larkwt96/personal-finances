import numpy as np

loans = np.array([6295.32, 8241.12, 844.72, 7740.56])
rates = np.array([4.29, 3.76, 4.45, 5.05])

print(np.sum(loans * rates) / np.sum(loans))
