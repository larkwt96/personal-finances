# You get a loan of 20_000

# Interest is 4.3
# Inflation is 3
mo = 205.36*12
total = 0
for year in range(1, 11):
    total += mo / (1.03)**year
print(total/20_000)


