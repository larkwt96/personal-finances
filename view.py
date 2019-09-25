import matplotlib.pyplot as plt
import numpy as np


def value(time=40, tax=.22, end_tax=.91, cap_tax=.15):
    r = 1.09/1.03
    r_mult = r ** time
    taxed_r = 1 + (r-1)*(1-cap_tax)
    taxed_r_mult = taxed_r**time

    # roth ira
    roth = 6000*r_mult

    # traditional ira
    trad = (6000*r_mult)*end_tax + 6000*tax*taxed_r_mult

    return roth, trad


roth, trad = value(35, tax=.22, end_tax=.83)
print(roth, trad, roth / trad)
roth, trad = value(35, tax=.22, end_tax=.93)
print(roth, trad, roth / trad)

# time
vals = np.array([list(value(time)) for time in range(1, 40)])
plt.title('amnt vs time')
plt.plot(vals[:, 0], label='roth')
plt.plot(vals[:, 1], label='trad')
plt.legend()

# taxes
taxes = np.arange(0, 1, .05)
vals = np.array([list(value(tax=tax, end_tax=.91)) for tax in taxes])
plt.figure()
plt.title('amnt vs tax')
plt.plot(taxes, vals[:, 0], label='roth')
plt.plot(taxes, vals[:, 1], label='trad')
plt.legend()

plt.show(True)
