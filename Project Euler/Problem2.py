"""By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms."""
sum = 0
fibValues = [1, 1]
while fibValues[-1] < 4000000:
    fibValues.append(fibValues[-1] + fibValues[-2])

for value in fibValues:
    if value % 2 == 0:
        sum  += value

print(sum)