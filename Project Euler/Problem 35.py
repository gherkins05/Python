circularPrimes = []


def getRotations(n):
    rotations = [n]
    for i in range(len([*str(n)]) - 1):
        value = [*str(rotations[-1])]
        print(value)
        rotations.append(f'{[*str(rotations[-1])][1:]}{[*str(rotations[-1])][0]}')

getRotations(197)
