import math
"""What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?"""

def isPrime(num):
    prime = True
    if num == 2:
        return True
    elif num % 2 == 0:
        prime = False
    else:
        for i in range(3, math.floor(num ** 0.5) + 1, 2):
            if num % i == 0:
                prime = False
    return prime

def primeFactors(num):
    primeFactors = []
    numToTest = 2
    while num != 1:
        if num % numToTest == 0 and isPrime(numToTest):
            primeFactors.append(numToTest)
            num = int(num / numToTest)
            numToTest = 2
        else:
            numToTest += 1
    return primeFactors

m = 20
factors = []
uFactors = []
product = 1

for num in range(2, m + 1):
    factors += primeFactors(num)

for item in factors:
    if item not in uFactors:
        uFactors.append(item)

for value in uFactors:
    most = 0
    for i in range(2, m + 1):
        most = max(primeFactors(i).count(value), most)
    product *= value ** most

print(product)