values = []

def f(a, b):
    return a ** b

for a in range(2, 101):
    for b in range(2, 101):
        if f(a, b) not in values:
            values.append(f(a, b))
print(len(values))
