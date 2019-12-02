#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import numpy as np
from data import loan_data  # comment this out to use example
from model import Model


def demo_find_monthly_payment(upfront=0, minimum=0):
    """
    minimum can be an integer or a vector. The integer is the minimum payment
    requirement. It can be 0. If None, it will default to the interest.
    """
    model = Model(loans, rates, minimum=minimum)
    yrs = [1, 2, 3, 4, 5, 8, 10, 12, 15, 20, 25, 30]
    yrs = [10]
    for i in yrs:
        mo_total = model.get_plan(upfront=upfront, min_months=i*12)
        print('{} years: ${:.2f} per mo (${:.2f} per yr)'.format(
            i, mo_total, mo_total*12))
    return model.get_plan(upfront=upfront, min_months=120)


def demo_test_monthly_payment(upfront=0, minimum=0, mo_total=200):
    model = Model(loans, rates, minimum=minimum)
    run = model.run(upfront, mo_total)
    print(*run[:3])
    print('...')
    print()
    print(*run[-2:])

    print("years:", run[-1].month/12)
    return run


if __name__ == "__main__":
    loans = [5000, 5000, 7000, 7000]
    rates = [4.29, 3.76, 4.45, 5.05]

    # uncomment this to unpack loan_data
    loans, rates = loan_data

    print('total loans:', np.sum(loans))
    invest = 0000
    upfront_payment = 0000
    monthly_minimum_payment = 0

    monthly_payment = demo_find_monthly_payment(upfront=upfront_payment,
                                                minimum=monthly_minimum_payment)

    run = demo_test_monthly_payment(
        upfront=upfront_payment, minimum=monthly_minimum_payment, mo_total=monthly_payment)

    elrs = [mo.elr for mo in run]
    plt.plot(elrs)
    plt.plot([0, 120], [.07*.65, .07*.65])
    plt.show(True)

    print('monthly payment', monthly_payment)
    total_loans = np.sum(loans)
    print('total loans:', total_loans)
    total_paid = np.sum([statement.payment for statement in run])
    print('total paid:', total_paid)

    interest_total = total_paid - total_loans
    print('total interest:', interest_total)
    invest_total = invest*(1.07**10) - invest
    print('investment', invest_total)
    total_loss = invest_total - interest_total
    print('total loss', total_loss)
