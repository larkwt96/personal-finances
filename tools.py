import math
import numpy as np

tax_brackets = [
    (.1, 9_700),
    (.12, 39_475),
    (.22, 84_200),
    (.24, 160_725),
    (.32, 204_100),
    (.35, 510_300),
    (.37, np.inf),
]
default_deduction = 12_000


def tax(salary, deduction=default_deduction):
    tax = 0
    last_level = 0
    taxable_salary = salary - deduction
    for rate, level in tax_brackets:
        if taxable_salary > level:
            tax += rate * (level-last_level)
        else:
            tax += rate * (taxable_salary - last_level)
            break
        last_level = level
    return tax


def post_tax(salary, deduction=default_deduction):
    return salary - tax(salary, deduction)


def grow(yearly_deposits, rate, time, initial_balance=0):
    total = initial_balance
    for i in range(time):
        total += yearly_deposits
        total *= rate
    return total


def today_value(value, time):
    return value / 1.03**time


def simulate(salary, time, r401k=19_000, rira=6_000, exp=3_000):
    # gains
    savings = 12_000
    saving_intrest = savings * (1.019 / 1.0256 - 1)

    # costs
    taxes = tax(salary - r401k)

    # revenue
    free = salary - taxes - r401k - rira - exp
    untaxed = grow(r401k + rira, 1.0725, time)
    taxed = grow(free + saving_intrest, 1.0617, time)
    return savings + untaxed + taxed


def simulate_house(salary, time, r401k=19_000, rira=6_000, exp=3_000, house_down=.2*600_000):
    # gains
    savings = 12_000
    saving_interest = savings * (1.019 / 1.0256 - 1)

    # costs
    taxes = tax(salary - r401k)

    # revenue
    free = salary + saving_interest - taxes - r401k - rira - exp
    untaxed = grow(r401k + rira, 1.0725, time)

    # house
    waiting = math.ceil(house_down*1.05 / free)
    print(f'must save for {waiting} years')
    taxed = grow(free, 1.0617, max(time-waiting, 0))
    return savings + untaxed + taxed
