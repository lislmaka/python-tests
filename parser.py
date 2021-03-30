import random

r = 0
l = 0

for i in range(1000):
    v = random.randint(0, 1)
    if v == 0:
        r += 1
    else:
        l += 1

print('l = ', l, ', r = ', r)
