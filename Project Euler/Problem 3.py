import math
"""What is the largest prime factor of the number 600851475143?"""
primeFactor = 1

def isPrime(num):
    prime = True
    for i in range(3, math.floor(num ** 0.5) + 1, 2):
        if num % i == 0:
            prime = False
    return prime

for i in range(3, math.floor(600851475143 ** 0.5) + 1, 2):
    if 600851475143 % i == 0 and isPrime(i) and i > primeFactor:
        primeFactor = i

print(primeFactor)