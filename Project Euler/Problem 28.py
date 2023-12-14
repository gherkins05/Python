gridSize = 1001
location = [int((gridSize + 1) / 2), int((gridSize + 1) / 2)] #x, y
spiral = []


for i in range(gridSize + 2):
    line = []
    for ii in range(gridSize + 2):
        line.append(0)
    spiral.append(line)

counter = 1
previousDirection = "u"

while spiral[1][-2] == 0:
    spiral[location[1]][location[0]] = counter
    if previousDirection == "u":#go right
        location[0] += 1
        if spiral[location[1] + 1][location[0]] == 0:
            previousDirection = "r"

    elif previousDirection == "r":#go down
        location[1] += 1
        if spiral[location[1]][location[0] - 1] == 0:
            previousDirection = "d"

    elif previousDirection == "d":#go left
        location[0] -= 1
        if spiral[location[1] - 1][location[0]] == 0:
            previousDirection = "l"

    elif previousDirection == "l":#go up
        location[1] -= 1
        if spiral[location[1]][location[0] + 1] == 0:
            previousDirection = "u"
    counter += 1

tally = -1
for i in range(len(spiral)):
    tally += spiral[i][i]
    tally += spiral[len(spiral) - i - 1][i]

print(tally)
