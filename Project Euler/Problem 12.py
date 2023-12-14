"""What is the value of the first triangle number to have over five hundred divisors?"""
def getFactors(num):
    numOfFactors = 0
    for i in range(1, round(num ** 0.5)):
        if num % i == 0:
            numOfFactors += 1
    return 2 * numOfFactors

def getTriangleNumber(n):
    return int((n ** 2 + n) / 2)
num = 1
while getFactors(getTriangleNumber(num)) <= 500:
    num += 1

print(getTriangleNumber(num))