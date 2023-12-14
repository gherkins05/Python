outcome = True
number = 1
def getFactors(number):
    factors = 0
    for i in range(1, number + 1):
        if number % i == 0:
            factors += 1
    return factors



while outcome:
    if getFactors(number) >= 2 and number % 2 == 1:
        
