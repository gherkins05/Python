"""Find the largest palindrome made from the product of two 3-digit numbers."""
largest = 0
for i in range(100, 1000):
    for ii in range(100, 1000):
        if [*str(i * ii)][::-1] == [*str(i * ii)]:
            largest = max(i * ii, largest)
print(largest)