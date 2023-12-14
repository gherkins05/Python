sum = 0
fact = 1
for f in range(1, 101):
  fact *= f

for char in str(fact):
  sum += int(char)
print(sum)
