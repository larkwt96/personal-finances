import numpy as np

# loans = [loans ($), rates (%)]
loan_data = np.array([6267.54, 4.290,
                      8207.92, 3.760,
                      840.55, 4.450,
                      7695.97, 5.050], dtype=np.float64).reshape(-1, 2).T

salaries = [
    60000,
    65000,
    70000,
    75000,
    80000,
    #85000,
    #90000,
    #95000,
    #100000,
    ]
commute = np.array([
    30,
    #40,
    #60,
    120,
    ], dtype=np.float64)/60
housing = [
    #1300,
    #1500,
    1800,
    #2000,
    #2300,
    ]
people = [
    #1,
    2,
    ]
living_data = tuple(map(np.array, [salaries, commute, housing, people]))