'''
COMPLETED ON REPLIT
 3
4 9

replace the 3 with a 12 since its the largest value the 3 can get


     6
    4 5
   2 9 3

longest route is 6, 5, 9 = 20

      6
    13 14
   2  9  3

      6
    13 14

      20
    13  14

      20

final number should be the solution
    
'''

exampleTriangle = [
[3],
[7, 4],
[2, 4, 6],
[8, 5, 9, 3]]

problemTriangle = [
["75"],
["95", "64"],
["17", "47", "82"],
["18", "35", "87", "10"],
["20", "04", "82", "47", "65"],
["19", "01", "23", "75", "03", "34"],
["88", "02", "77", "73", "07", "63", "67"],
["99", "65", "04", "28", "06", "16", "70", "92"],
["41", "41", "26", "56", "83", "40", "80", "70", "33"],
["41", "48", "72", "33", "47", "32", "37", "16", "94", "29"],
["53", "71", "44", "65", "25", "43", "91", "52", "97", "51", "14"],
["70", "11", "33", "28", "77", "73", "17", "78", "39", "68", "17", "57"],
["91", "71", "52", "38", "17", "14", "91", "43", "58", "50", "27", "29", "48"],
["63", "66", "04", "68", "89", "53", "67", "30", "73", "16", "69", "87", "40", "31"],
["04", "62", "98", "27", "23", "09", "70", "98", "73", "93", "38", "53", "60", "04", "23"]]

class Node:
    def __init__(self, location, value):
        self.location = location
        self.value = value
        self.previousNode = None

def getMax(arr):
    data = [0, 0]   #[value, index]
    for i in range(len(arr)):
        if int(arr[i]) > int(data[0]):
            data = [arr[i], i]
    return data


def generateNodes(triangle):
    for i in range(len(triangle)):
        for ii in range(len(triangle[i])):
            triangle[i][ii] = Node([i, ii], triangle[i][ii])
           
generateNodes(exampleTriangle)





    

