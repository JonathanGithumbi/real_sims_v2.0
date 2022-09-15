from itertools import cycle

names=['jonathan','mburu','githumbi']

names_iterator = iter(names)


i =1
while i != 10:
    print(next(names_iterator,"end"))
    i = i+1
    
