#!/usr/bin/env python3

import numpy as np

class Salary:
    tax_brackets = [
        (.1, 9700),
        (.12, 39475),
        (.22, 84200),
        (.24, 160725),
        (.32, 204100),
        (.35, 510300),
        (.37, np.inf),
    ]

    def __init__(self, salary):
        self.salary = salary
        self.tax = 0
        last_level = 0
        for rate, level in Salary.tax_brackets:
            if self.salary > level:
                self.tax += rate * (level-last_level)
            else:
                self.tax += rate * (self.salary - last_level)
                break
            last_level = level
        self.taxed_salary = self.salary - self.tax
        self.tax_rate = self.tax / self.salary

class House:
    def __init__(self, rent, people=1):
        self.total_rent = rent
        self.rent = self.total_rent / people
        self.yearly_cost = self.rent * 12

class Life:
    def __init__(self, salary, house, commute, desc):
        # commute in hours, assumes 8 hr day
        commute_rate = 8 / (8 + 2 * commute)

        self.desc = desc
        self.gain = salary.taxed_salary
        self.cgain = salary.taxed_salary*commute_rate
        self.loss = house.yearly_cost
        self.net = self.gain - self.loss
        self.cnet = self.cgain - self.loss

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Desc: {}\n'.format(self.desc) + \
               'Gain: {}\n'.format(self.gain) + \
               'C-Gain: {}\n'.format(self.cgain) + \
               'Loss: {}\n'.format(self.loss) + \
               'Net: {}\n'.format(self.net) + \
               'C-Net: {}\n'.format(self.cnet) + \
               '\n'

if __name__ == '__main__':
    broom_house = House(1800, 2)
    lohi_house = House(2100, 2)
    tech_house = House(1300)

    k = 10**3
    s60k = Salary(60*k)
    s65k = Salary(65*k)
    s70k = Salary(70*k)
    s75k = Salary(75*k)
    s80k = Salary(80*k)

    ph = 1/60
    c15 = 15*ph
    c30 = 30*ph
    c45 = 45*ph
    c60 = 60*ph

    jobs = []

    #jobs.append(Life(s60k, broom_house, 0, 'front range 60'))
    jobs.append(Life(s65k, broom_house, c15, 'front range 65'))
    jobs.append(Life(s70k, broom_house, c15, 'front range 70'))
    jobs.append(Life(s70k, broom_house, c60, 'broom tb 70'))
    jobs.append(Life(s70k, broom_house, c30, 'broom tb 70 train'))
    jobs.append(Life(s75k, broom_house, c60, 'broom tb 75'))
    jobs.append(Life(s80k, broom_house, c60, 'broom tb 80'))
    jobs.append(Life(s70k, lohi_house, c30, 'lohi tb'))
    #jobs.append(Life(s70k, tech_house, c15, 'tech tb'))

    print('C-NET')
    for job in sorted(jobs, key=lambda x:x.cnet, reverse=True):
        print(job)

    #print('NET')
    #for job in sorted(jobs, key=lambda x:x.net, reverse=True):
        #print(job)
