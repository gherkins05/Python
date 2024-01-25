"""Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum."""

sumOfSquares = 0
squareOfSum = 0

for i in range(1, 101):
    sumOfSquares += i ** 2
    squareOfSum += i

squareOfSum = squareOfSum ** 2

print(squareOfSum - sumOfSquares) 