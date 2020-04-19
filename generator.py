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
value = np.random.randint(15, size = genes) #getting values
weight = np.random.randint(3,9, size = genes) #getting weight
capacity = int(weight.sum()*0.55) #getting capacity
things = np.array(['a','b','c','d','e','f','g','h']) #object names
ratio = [] #counting ratio value/weight

for i in range(len(things)): #counting ratio for every
    ratio.append(round(value[i]/weight[i], 2))

#creating dataframe
data = {'name': things,
        'value': value,
        'weight': weight,
        'ratio': ratio}

table_of_items = pd.DataFrame(data, columns = ['name', 'value', 'weight', 'ratio'])
table_of_items = table_of_items.sort_values('ratio', ascending = False)  #sorting data frame
table_of_items = table_of_items.reset_index(drop = True)

def fcelu_test(): #test
    weight_for_fcelu = 0
    bound = 0 #biggest value possible
    number_of_row = 0 #number of row
    storage = 0

    for i in range(len(things)):
        if weight_for_fcelu < capacity:
            bound += table_of_items.iat[number_of_row, 1] #adding value of another item
            weight_for_fcelu += table_of_items.iat[number_of_row, 2] #adding weight of another item
            if weight_for_fcelu < capacity:
                number_of_row += 1 #getting in to lower row
            else:
                bound -= table_of_items.iat[number_of_row, 1] #deleting value of item which made backpack too heavy
                weight_for_fcelu -= table_of_items.iat[number_of_row, 2] #deleting weight of item which made backpack too heavy
                storage = capacity - weight_for_fcelu #counting how much weight it can accualy fit in
                weight_for_fcelu += storage #adding this value
                #print('p=',p,'/',df.iat[l+1,2])
                storage = storage / table_of_items.iat[number_of_row + 1, 2] #counting value of left space
                #print('p=', p)
                #print('p', p, '*',df.iat[l+1,1])
                storage = storage * table_of_items.iat[number_of_row + 1, 1] #counting value of left space
                #print('=',p)
                bound += round(storage,2) #adding it to value

        if weight_for_fcelu == capacity: #ending the loop
            break
    print('bound =', bound, 'weight_fcelu =', weight_for_fcelu)

def pop(geny, osobniki):
    population1 = np.zeros((osobniki, geny + 4)) #creating array full of zeros to make shape of array
    #4 bo wartosc, waga, ratio, czy mieści się w plecaku
    for i in range(osobniki):
        for j in range(geny):
            chance = random.random()
            if chance > 0.50:
                population1[i, j] = 1 # is it taking this item
                population1[i, geny] += table_of_items.iat[j, 1]   #value of every item in backpack
                population1[i, geny + 1] += table_of_items.iat[j, 2]   #weight of every item in backpack
                population1[i, geny + 2] =  round(population1[i,geny] / population1[i,geny + 1],2)  #ratio value/weight
                #moze zamiast ratio wstawic tu b
                if population1[i, geny + 1] <= capacity: #is backpack in capacity
                    population1[i, geny + 3] = 1
                else:
                    population1[i, geny + 3] = 0
                #czy mam stowrzyc funckje celu tak jak normalnie w problemie plecakowym to b?

    return population1


def mutacja_test(population2, szansa):
    for i in range(individual):
        chance_for_mutation = random.random()
        #print(a)
        if chance_for_mutation < szansa:
            mutation_place = random.randint(0, genes - 1)
            #print('b=',b)
            #print(popu[i])

            if population2[i, mutation_place] == 1: #mutation
                population2[i, mutation_place] = 0
            else:
                population2[i, mutation_place] = 1
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
print(table_of_items)
print('capacity:', capacity)
fcelu_test()
print(population)
mutacja_test(population, 0.02)
