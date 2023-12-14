import math
largest = 0

def isPrime(n):
    if n % 2 != 0:
        prime = True
        for i in range(3, math.floor(n ** 0.5) + 1, 2):
            if n % i == 0:
                prime = False
        return prime
    elif n == 2:
        return True
    else:
        return False

def getPrimeFactors(n):
    primeFactors = []

    for factor in range(1, n + 1):
        if n % factor == 0 and isPrime(factor):
            primeFactors.append(factor)
    return primeFactors

def getRecurringLength(decimal):
    decimal = int(str(decimal)[2:])
    return decimal
    
for num in range(2, 100):
    factors = getPrimeFactors(num)
    factors = list(filter((1).__ne__, factors))
    factors = list(filter((2).__ne__, factors))
    factors = list(filter((5).__ne__, factors))
    if len(factors) != 0:
        dec = getRecurringLength(1/num)
        if len(str(dec)) != str(dec).count(str(dec)[0]):#removes most single recurring decimals
            print(f'1/{num}: 0.{dec}')
    
