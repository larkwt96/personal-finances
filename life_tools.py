import numpy as np

def parse(num):
    num = np.array(num, dtype=np.float64)
    if num.shape == ():
        num = np.array([num])
    return num

