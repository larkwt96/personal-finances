import numpy as np
import calendar
import matplotlib.pyplot as plt


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
    def __init__(self, loans, rates, upfront=None):
        self.loans = loans
        self.rates = rates / 100
        self.upfront = upfront
        self.reset()

    @property
    def elr(self):
        total = np.sum(self.balance)
        return np.sum(self.rates * self.balance / total)

    def set_upfront(self, upfront):
        self.upfront = upfront

    def pay(self, payment):
        self.payment += payment

    def reset(self):
        self.month = 1
        self.history = []
        if self.upfront is not None:
            interest = np.zeros_like(self.loans)
            self.balance = self.loans-self.upfront
            statement = Statement(self.loans, interest,
                                  self.upfront, 0, self.elr)
            self.history.append(statement)
        else:
            self.balance = np.copy(self.loans)
        self.payment = np.zeros_like(self.loans)

    @property
    def interest(self):
        interest = self.balance * self.rates / 12
        return interest

    @property
    def total(self):
        return self.balance + self.interest

    def step_month(self):
        statement = Statement(np.copy(self.balance),
                              self.interest, self.payment, self.month, self.elr)
        self.history.append(statement)
        self.balance += self.interest - self.payment
        self.balance[self.balance < 1e-4] = 0
        self.payment = np.zeros_like(self.balance)
        self.month += 1


class Model:
    '''
    The goal is to find out the best way to pay off my student loans.

    I can pay monthley
    '''

    def __init__(self, loans, rates, minimum=None):
        self.loans = np.array(loans, dtype=np.float64).reshape(-1)
        self.rates = np.array(rates, dtype=np.float64).reshape(-1)
        if minimum is None:
            self.minimum = None
        elif np.isscalar(minimum):
            self.minimum = minimum * np.ones_like(self.loans)
        else:
            self.minimum = np.array(minimum)

    def is_close_to_zero(self, arr):
        return np.all(np.isclose(arr, np.zeros_like(arr), atol=1e-3))

    def get_min_payment(self, balance, minimum=None):
        if minimum is None:
            return np.zeros_like(balance)
        else:
            return np.minimum(balance, minimum)

    def distribute(self, balance, total_budget, minimum=None, rates=None):
        tol = 1e-4
        if rates is None:
            rates = self.rates
        payment = self.get_min_payment(balance, minimum)
        budget = max(total_budget - np.sum(payment), 0)
        while max(budget, 0) > 0 and max(np.sum(balance - payment), 0) > 0:
            #metric = balance-payment
            #metric = balance*rates
            #metric = (balance-payment)*rates

            # This one I think is optimal (via testing and light research)
            metric = rates
            highest_rate = np.argmax(metric)
            new_payment = payment[highest_rate] + budget
            if new_payment >= balance[highest_rate]:  # if pays off balance
                payment[highest_rate] = balance[highest_rate]
                budget = total_budget - np.sum(payment)  # get remaining
                rates[highest_rate] = 0
            else:
                payment[highest_rate] = new_payment
                budget = 0
        return payment

    def run(self, upfront=0, mo_total=0, max_months=1200):
        """
        The rule: pay the mimimum and then the highest rates
        mo_total is the budget, but minimum payments will cause over budget
        """
        upfront_payment = self.distribute(self.loans, upfront)
        bank = Bank(self.loans, self.rates, upfront_payment)
        rates = np.copy(self.rates)
        for _ in range(max_months):
            balance = bank.total
            if np.all(np.isclose(balance, np.zeros_like(balance), atol=1e-4)):
                break

            if self.minimum is None:
                minimum = bank.interest
            else:
                minimum = self.minimum
            payment = self.distribute(balance, mo_total,
                                      minimum=minimum,
                                      rates=rates)
            bank.pay(payment)
            bank.step_month()
        return bank.history

    def get_plan(self, upfront=0, min_months=120):
        if self.minimum is not None:
            mo_min = np.sum(self.minimum)
        else:
            mo_min = 0
        mo_total = mo_min
        inc = 1000
        while inc >= 1e-4:
            new_mo_total = mo_total+inc
            run = self.run(upfront=upfront, mo_total=new_mo_total)
            if run[-1].month <= min_months:
                inc = inc / 10
                continue
            mo_total = new_mo_total
            if mo_total < mo_min:
                return mo_min
        mo_total = new_mo_total
        return mo_total

        mo_total *= .5
        current_run = self.run(upfront=upfront, mo_total=mo_total)
        last_mo_total = mo_total
        while current_run[-1].month > min_months:
            print('here')
            last_mo_total = mo_total
            mo_total *= 1.05
            current_run = self.run(upfront=upfront, mo_total=mo_total)
        mo_total = last_mo_total
        while current_run[-1].month > min_months:
            print('here')
            last_mo_total = mo_total
            mo_total -= 1
            current_run = self.run(upfront=upfront, mo_total=mo_total)
        mo_total = last_mo_total
        while current_run[-1].month > min_months:
            print('here')
            last_mo_total = mo_total
            mo_total -= .0001
            current_run = self.run(upfront=upfront, mo_total=mo_total)
        return mo_total

    def multi_plot(self, x, ys, labels=None):
        if labels is None:
            labels = list(range(1, len(ys)+1))
        for i, y in enumerate(ys.T):
            plt.plot(x, y, label=labels[i])

    def plot(self, statements):
        balances = np.array([statement.balance for statement in statements])
        interests = np.array([statement.interest for statement in statements])
        payments = np.array([statement.payment for statement in statements])
        months = np.array([statement.month for statement in statements])
        final_totals = np.array(
            [statement.final_total for statement in statements])
        final_balances = np.array(
            [statement.final_balance for statement in statements])

        loan_names = ['loan({:.5})'.format(loan)
                      for loan in statements[0].balance]

        plt.figure()
        plt.subplot(411)
        plt.ylabel('balance')
        self.multi_plot(months, final_balances, loan_names)
        plt.legend()

        plt.subplot(412)
        plt.ylabel('total balance')
        plt.plot(months, np.sum(final_balances, axis=1))

        plt.subplot(413)
        plt.ylabel('payments')
        self.multi_plot(months, payments, loan_names)
        plt.legend()

        plt.subplot(414)
        plt.ylabel('total payments')
        plt.plot(months, np.sum(payments, axis=1))

        plt.tight_layout()
        plt.show(True)
