"""Which starting number, under one million, produces the longest collatz chain?"""

largestIterations = 0
maxIterations = 0
data = [[1, 1]]

def collatz(num):
    iterations = 0
    holder = num
    while holder != 1:
        if holder % 2 == 0:
            holder = holder / 2
            iterations += 1
        else:
            holder = 3 * holder + 1
            iterations += 1
    iterations += 1
    return iterations


for i in range(2, 1000000):
    data.append([i, collatz(i)])

m = [1, 1]
for i in range(len(data)):
    if m[1] < data[i][1]:
        m[1] = data[i][1]
        m[0] = i + 1

print(m[0])