"""How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?"""

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
allDays = []
counter = 0
sundays = 0


class Day:

    def __init__(self, textDay, day, month, year):
        self.textDay = textDay
        self.day = day
        self.month = month
        self.year = year


for year in range(1900, 2001):
    for month in range(1, 13):
        if month in [9, 4, 6, 11]:
            daysAmount = 30
        elif month == 2:
            if year % 4 == 0 or (year % 100 == 0 and year % 400 == 0):
                daysAmount = 29
            else:
                daysAmount = 28
        else:
            daysAmount = 31
        for day in range(1, daysAmount + 1):
            allDays.append(Day(days[counter], day, month, year))

            counter += 1
            if counter > 6:
                counter = 0

for date in allDays:
    if date.year > 1900 and date.day == 1 and date.textDay == "Sun":
        sundays += 1

print(sundays)
