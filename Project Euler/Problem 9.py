"""There exists one pythagorean triplet where a + b + c = 1000. Find a, b, c."""

for a in range(1000):
    for b in range(1000):
        c = (a ** 2 + b ** 2) ** 0.5
        if a + b + c == 1000 and a < b < c:
            print(a * b * c)