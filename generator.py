import numpy as np
import pandas as pd
import random as random
""""
def int_list_to_str_list(set_of_items):
    items=[]
    for i in range(len(set_of_items)):
        if len(str(set_of_items[i]))==1:
                items.append(" "+str(set_of_items[i]))
        else: items.append(str(set_of_items[i]))
    return items
"""
genes = 8
individual = 6
value=np.random.randint(15, size = genes) #getting values
weight=np.random.randint(3,9, size = genes) #getting weight
capacity=int(weight.sum()*0.55) #getting capacity
things=np.array(['a','b','c','d','e','f','g','h']) #object names
ratio = [] #counting ratio value/weight

for i in range(len(things)):
    ratio.append(round(value[i]/weight[i],2))

#creating dataframe
data = {'name': things,
        'value': value,
        'weight': weight,
        'ratio': ratio}

df = pd.DataFrame(data, columns = ['name', 'value', 'weight', 'ratio'])
df = df.sort_values('ratio', ascending = False) #sorting data frame #czy trzeba to robic? czy nie lepiej kiedy losowo sa rozrzucone te watosci
df = df.reset_index(drop = True)

def fcelu_test(): #test
    w = 0 #waga
    b = 0 #maksymalna funkcja
    l = 0 #licznik/ wiersz
    p = 0 #przechowajka

    for i in range(len(things)):
        if w < capacity:
            b += df.iat[l, 1] #dodawanie wartosci
            w += df.iat[l, 2] #dodawanie wagi
            if w < capacity:
                l += 1 #licznik +1 zeby przejsc do niższego wiersza
            else:
                b -= df.iat[l, 1]
                w -= df.iat[l, 2]
                p = capacity - w
                w += p
                #print('p=',p,'/',df.iat[l+1,2])
                p = p/df.iat[l+1,2]
                #print('p=', p)
                #print('p', p, '*',df.iat[l+1,1])
                p = p*df.iat[l+1,1]
                #print('=',p)
                b += round(p,2)

        if w == capacity:
            break
    print('b =', b, 'w =', w, 'l =', l)

def pop(geny, osobniki):
    a = np.zeros((osobniki, geny + 4)) #4 bo wartosc, waga, ratio, czy mieści się w plecaku
    for i in range(osobniki):
        for j in range(geny):
            b = random.random()
            if b > 0.50:
                a[i, j] = 1 #czy bierze dany przedmiot
                a[i, geny] += df.iat[j,1]   #wartość wszystkich przedmiotow
                a[i, geny + 1] += df.iat[j,2]   #waga wszystkich przedmiotow
                a[i, geny + 2] =  round(a[i,geny] / a[i,geny + 1],2)  #stosunek wartosci do wagi
                #moze zamiast ratio wstawic tu b
                if a[i, geny + 1] <= capacity: #czy jest mieści sie w granicach plecaka
                    a[i, geny + 3] = 1
                else:
                    a[i, geny + 3] = 0
                #czy mam stowrzyc funckje celu tak jak normalnie w problemie plecakowym to b?

    return a


def mutacja_test(popu,szansa):
    for i in range(individual):
        a = random.random() #losowanie szansy na mutacje
        #print(a)
        if a < szansa:
            b = random.randint(0, genes - 1) #losowanie miejsca mutacji
            #print('b=',b)
            #print(popu[i])
            
            if popu[i, b] == 1: #mutacja
                popu[i, b] = 0
            else:
                popu[i, b] = 1
            #print(popu[i])
            print("osobnik numer", i, "zmutował")

"""
value_str=int_list_to_str_list(value)
weight_str=int_list_to_str_list(weight)

print("|"+"-"*27+"|")
print("|przedmiot | wartosc | waga |")
for i in range(len(value)):
    print("|"+"-"*27+"|")
    print("|"+things[i]+"|"+" "*3+value_str[i]+" "*4+"|"+" "*2+weight_str[i]+" "*2+"|")
print("|"+"-"*27+"|")
print("Pojemność plecaka to:", capacity)
"""

"""
def arraym(things, value, weight):
    ajtems = []
    for i in range(len(things)):
        ajtems.append([(things[i], value[i], weight[i], 0)])
    return ajtems
items = arraym(things, value, weight)
#dtype = [('name', (np.str_, 10)), ("value", np.int64), ("weight", np.int64)]
ary = np.array(items)
print(ary)
print(ary.dtype)
ac = ary[ary[:,0].argsort()]
print(ac)
"""


population = pop(genes, individual)
print(df)
print('capacity:', capacity)
fcelu_test()
print(population)
mutacja_test(population, 0.02)
