def main(gridSize):
    routes = []
    for i in range(2 ** (gridSize * 2)):
        value = bin(i)[2:]
        binary = ""
        for i in range(gridSize * 2 - len(value)):
            binary += "0"
        binary += value
        if binary.count("0") == binary.count("1"):
            routes.append(binary)
    print(f'{gridSize} || {len(routes)}')

for i in range(1, 21):
    main(i)
    