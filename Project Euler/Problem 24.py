def permutation(lst):
 
    if len(lst) == 0:
        return []
    elif len(lst) == 1:
        return [lst]
    l = []
    for i in range(len(lst)):
       m = lst[i]
       remLst = lst[:i] + lst[i+1:]
       for p in permutation(remLst):
           l.append([m] + p)
    return l
 
data = list('0123456789')

listData = permutation(data)
listData.sort()
print(listData[999999])
