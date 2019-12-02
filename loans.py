import numpy as np
from data import loan_data
from model import Model, Bank
from math import ceil


class Statement:
    def __init__(self, balance, interest, payment, month, elr):
        self._balance = balance
        self._interest = interest
        self._payment = payment
        self._month = month
        self._elr = elr

    @property
    def balance(self):
        return self._balance

    @property
    def interest(self):
        return self._interest

    @property
    def payment(self):
        return self._payment

    @property
    def month(self):
        return self._month

    @property
    def final_total(self):
        return self.balance + self.interest

    @property
    def final_balance(self):
        return self.final_total - self.payment

    @property
    def elr(self):
        return self._elr

    def __str__(self):
        pre = 'Month: {}\n'.format(self.month)
        np.set_printoptions(precision=2)
        line1 = '{}+{}-{}\n'.format(self.balance, self.interest, self.payment)
        line2 = '={}-{}\n'.format(self.final_total, self.payment)
        line3 = '={}\n'.format(self.final_balance)
        eqn = '{}{}{}'.format(line1, line2, line3)
        return pre + eqn


class Bank:
    def __init__(self, loans: np.ndarray | float, rates: np.ndarray | float, upfront: float = None):
        self.loans = np.array(100*loans, dtype=int)  # cents
        self.rates = np.array(rates / 100
        self.upfront=upfront
        self.reset()

    @property
    def elr(self):
        total=np.sum(self.balance)
        return np.sum(self.rates * self.balance / total)

    def set_upfront(self, upfront):
        self.upfront=upfront

    def pay(self, payment):
        self.payment += payment

    def reset(self):
        self.month=1
        self.history=[]
        if self.upfront is not None:
            interest=np.zeros_like(self.loans)
            self.balance=self.loans-self.upfront
            statement=Statement(self.loans, interest,
                                  self.upfront, 0, self.elr)
            self.history.append(statement)
        else:
            self.balance=np.copy(self.loans)
        self.payment=np.zeros_like(self.loans)

    @property
    def interest(self):
        interest=self.balance * self.rates / 12
        return interest

    @property
    def total(self):
        return self.balance + self.interest

    def step_month(self):
        statement=Statement(np.copy(self.balance),
                              self.interest, self.payment, self.month, self.elr)
        self.history.append(statement)
        self.balance += self.interest - self.payment
        self.balance[self.balance < 1e-4]=0
        self.payment=np.zeros_like(self.balance)
        self.month += 1


def round_up(val, ndigits=2):
    adj=10**ndigits
    return ceil(adj*val)/adj


def mo_pay(loans, rates, upfront=0, minimum=0):
    pass


if __name__ == "__main__":
    loans, rates=loan_data

    upfront=0  # pool to pay upfront
    minimum=0  # mo min

    bank=Bank(loans, rates, upfront)
    elr=np.sum(loans * rates / np.sum(loans))
    print(loans, rates, elr)

    model=Model([np.sum(loans)], [elr], minimum=minimum)
    mo_pay=round_up(model.get_plan(upfront=upfront))
    print('consolidated', mo_pay)
    run=model.run(upfront=upfront, mo_total=mo_pay)
    total_paid=round_up(np.sum([statement.payment for statement in run]))
    print('total paid:', total_paid)

    print()
    model=Model(loans, rates, minimum=minimum)
    mo_pay=round_up(model.get_plan(upfront=upfront))
    run=model.run(upfront=upfront, mo_total=mo_pay)
    print('split loans', mo_pay)
    total_paid=round_up(np.sum([statement.payment for statement in run]))
    print('total paid:', total_paid)
