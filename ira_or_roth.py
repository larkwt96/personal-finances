import numpy as np

"""
This tool lets you figure out how much money you're missing out on if you
contribute to a Roth IRA.

Since tax gets applied beforehand, you don't get any interest on it.

If you want to have 100k when you retire, then invest only in Roth. If you
want to have a smaller income, then go for traditional IRA.
"""


# Util
k = 1000
ira_dept = 6*k  # ignores change at 50
tax_brackets = [
    (.1, 9700),
    (.12, 39475),
    (.22, 84200),
    (.24, 160725),
    (.32, 204100),
    (.35, 510300),
    (.37, np.inf),
]


# Config
salary = 60*k
retire_salary = 0
expenditure = 20*k
nonqual = 1 + 5 / 100  # 5% inflation adjusted taxed investment rate
qual = 1 + 7 / 100  # 7% inflation adjusted untaxed investment rate
years = 35


def post_tax(salary):
    tax = 0
    last_level = 0
    for rate, level in tax_brackets:
        if salary > level:
            tax += rate * (level-last_level)
        else:
            tax += rate * (salary - last_level)
            break
        last_level = level
    return salary - tax


def grow(year_dept, rate, time):
    total = 0
    for i in range(time):
        total += year_dept
        total *= rate
    return total


def roth():
    left_over = post_tax(salary) - expenditure - ira_dept
    roth_prof = grow(ira_dept, qual, years)
    tax_prof = grow(left_over, nonqual, years)
    return roth_prof, tax_prof, (roth_prof + tax_prof) / 25 + retire_salary


def ira():
    left_over = post_tax(salary - ira_dept) - expenditure
    ira_prof = grow(ira_dept, qual, years)
    tax_prof = grow(left_over, nonqual, years)
    return ira_prof, tax_prof, post_tax(retire_salary + ira_prof / 25) + tax_prof / 25


print('roth', roth())
print('ira', ira())
