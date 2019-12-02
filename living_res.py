#!/usr/bin/env python3

import numpy as np
from data import living_data
from tools import parse

salaries, commutes, housings, peoples = living_data

# 2019
hours_per_day = 8
tax_brackets = [
    (.1, 9700),
    (.12, 39475),
    (.22, 84200),
    (.24, 160725),
    (.32, 204100),
    (.35, 510300),
    (.37, np.inf),
]


def tax_single(amount):
    tax = 0
    last_level = 0
    for rate, level in tax_brackets:
        if amount > level:
            tax += rate * (level - last_level)
        else:
            tax += rate * (amount - last_level)
            break
        last_level = level
    return tax

def tax(amount):
    amount = parse(amount)
    return np.array(list(map(tax_single, amount)))

def taxed_salary(amount):
    amount = parse(amount)
    return amount - tax(amount)

def housing(housing, people=1):
    housing = parse(housing)
    people = parse(people)
    return housing[:, None] / people

def yearly_housing(housing_rate, people=1):
    # result of housing or normal rate vector or scalar
    housing_rate = parse(housing_rate)
    if len(housing_rate.shape) == 2:
        return 12 * housing_rate
    else:
        return 12 * housing(housing_rate, people)

# Note on commute formulas: I'm not sure which is best, but I typically use the
# effective salary one. to understand the diffence, think about the extremes. A
# custom value is simple, but hard to assume. Effective will assume any work
# regardless of commute has value, but that value does approach zero, but it
# never goes negative. That implies that extreme commutes are still valid.
# Commute value assumes that time away from work is just as valuable as when
# working. From society's perspective, this is usually false. That's where
# effective is more realistic and makes this aspect less sensitive. Use it how
# you will.

def commute_value_custom(salary, commute, value=15):
    # Custom hourly value. Issue: assumes 5 days a wk 52 weeks a year
    salary = parse(salary)[:, None]
    commute = parse(commute)
    value = parse(value)
    return np.ones_like(salary) * value * commute * 5 * 52

def commute_value_effective_salary(salary, commute):
    # Salary pays for commute and hours. This is value of commute under that
    # assumption. Salary removing commute.
    salary = parse(salary)[:, None]
    commute = parse(commute)
    total = commute + hours_per_day
    return salary * commute / total

def commute_value_from_salary(salary, commute, adjust=.5):
    # find hourly rate from salary, multiply by commute. Depends on hours
    # worked per day.
    commute = parse(commute)
    return adjust * salary * commute / hours_per_day


def report(salaries, commutes, housings, peoples):
    gain = salaries
    # salaries x commutes
    loss = tax(salaries)[:, None] + commute_value_effective_salary(salaries, commutes)
    yearly_housing_rates = np.unique(yearly_housing(housings, peoples).reshape(-1))
    loss = loss[:, :, None] + yearly_housing_rates

    total = gain[:, None, None] - loss

    #print(salaries)
    #print(commutes)
    #print(yearly_housing_rates)
    ind_raveled = np.argsort(total, axis=None)
    ind = np.unravel_index(ind_raveled, total.shape)
    #si = ind[0][0]
    #ci = ind[1][0]
    #ri = ind[2][0]
    #total_ = salaries[si] - (tax(salaries[si]) + commute_value_effective_salary(salaries[si], commutes[ci]) + yearly_housing_rates[ri])
    #print(total_)
    #print(total[ind][0])

    sis, cis, ris = ind
    print('{:20}{:20}{:20}{:20}'.format('salary', 'commute', 'housing', 'value'))
    length = len(sis)
    for i in range(length):
        i = length - 1 - i
        salary = salaries[sis[i]]
        commute = commutes[cis[i]]
        housing = yearly_housing_rates[ris[i]]
        value = total[ind][i]
        np.set_printoptions(precision=2)
        print('{:20}{:20}{:20}{:20}'.format(salary, commute, housing, value))

report(salaries, commutes, housings, peoples)