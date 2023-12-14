single = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
double = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "", "twenty", "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety"]
triple = ["", "hundred"]
quadruple = ["", "one thousand"]
mainString = ""
counter = 0
for i in range(1, 1001):
    text = ""
    holder = [*f'{(4 - len([*str(i)])) * "0"}{str(i)}']
    number = []
    text = []
    for item in holder:
        number.append(int(item))
    if number[0] == 1:
        text.append(quadruple[1])
    if number[1] != 0:
        text.append(f'{single[number[1]]} {triple[1]}')


    if number[2] != 1:
        thing = tens[number[2]] + " " + single[number[3]]#This line adds an extra 100 since the " " is added when there isnt a multiple of 10. happens 10 times every 100 ten times
        if thing != " ":
            text.append(thing)

    else:
        text.append(double[number[3]])

    string = ""
    for i in range(len(text)):
        string += text[i]
        if i < (len(text) - 1):
            string += " and "
    mainString += string
    print(string)

for char in mainString:
    if char != " ":
        counter += 1
print(counter)
