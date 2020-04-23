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
individual = 100
value = np.random.randint(15, size=genes)  # getting values
weight = np.random.randint(3, 9, size=genes)  # getting weight
capacity = int(weight.sum() * 0.55)  # getting capacity
things = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])  # object names
ratio = []  # counting ratio value/weight

for i in range(len(things)):  # counting ratio for every
    ratio.append(round(value[i] / weight[i], 2))

# creating dataframe
data = {'name': things,
        'value': value,
        'weight': weight,
        'ratio': ratio}

table_of_items = pd.DataFrame(data, columns=['name', 'value', 'weight', 'ratio'])
table_of_items = table_of_items.sort_values('ratio', ascending=False)  # sorting data frame
table_of_items = table_of_items.reset_index(drop=True)

"""
def fcelu_test():  # test
    weight_for_fcelu = 0  # to do wyjebania cala raczej
    bound = 0  # biggest value possible
    number_of_row = 0  # number of row
    storage = 0

    for i in range(len(things)):
        if weight_for_fcelu < capacity:
            bound += table_of_items.iat[number_of_row, 1]  # adding value of another item
            weight_for_fcelu += table_of_items.iat[number_of_row, 2]  # adding weight of another item
            if weight_for_fcelu < capacity:
                number_of_row += 1  # getting in to lower row
            else:
                bound -= table_of_items.iat[number_of_row, 1]  # deleting value of item which made backpack too heavy
                weight_for_fcelu -= table_of_items.iat[
                    number_of_row, 2]  # deleting weight of item which made backpack too heavy
                storage = capacity - weight_for_fcelu  # counting how much weight it can accualy fit in
                weight_for_fcelu += storage  # adding this value
                # print('p=',p,'/',df.iat[l+1,2])
                storage = storage / table_of_items.iat[number_of_row + 1, 2]  # counting value of left space
                # print('p=', p)
                # print('p', p, '*',df.iat[l+1,1])
                storage = storage * table_of_items.iat[number_of_row + 1, 1]  # counting value of left space
                # print('=',p)
                bound += round(storage, 2)  # adding it to value

        if weight_for_fcelu == capacity:  # ending the loop
            break
    print('bound =', bound, 'weight_fcelu =', weight_for_fcelu)
"""

def populationn(gen, individual):  # funkcja robienia populacji
    population1 = np.random.randint(2, size = (individual, gen))

    return population1


def calc_backpack(population, data):
    population_size = population.shape
    values_weights = np.zeros((population_size[0],2))
    for i in range(population_size[0]):
        for j in range(population_size[1]):
            if population[i, j] == 1:
                values_weights[i,0] += data.iat[j,1] #value
                values_weights[i,1] += data.iat[j,2] #weight
   # print(values_weights)
    return values_weights

def rating(stats, capacity):
    stats_size = stats.shape
    rate = np.zeros((stats_size[0],))
    for i in range(stats_size[0]):
        if stats[i, 1] <= capacity: # checking if weight of this backpack is in capacity
            if stats[i, 0] > 0: # u cant divide by 0
                rate[i] += round(stats[i, 0] / stats[i, 1], 2) #counting ratio value divieded by weight
            else:
                rate[i] = 0

    return rate

#teraz funkcja selekcji - turniejowa

def tournament(population, rating):
    winers = []  #best individuals
    not_zero_ratio = [] #nuumber of rows, where weight of backpack < capacity
    for i in range(len(population[:,0])):
        if rating[i] >= 0:
            not_zero_ratio.append(i) #nuumber of rows, where weight of backpack =< capacity
    for k in range(int((len(population[:,0]) * 0.4))):
        rivals = []
        not_zero_ratio_temporary = not_zero_ratio.copy() #makeing copy of the list
        for j in range(int((len(population[:,0]) * 0.4))): #random take 40 individuals and choosing the best
            chance = random.choice(not_zero_ratio_temporary)
            if len(rivals) > 0:
                if rating[rivals[0]] <= rating[chance]: #comparing new row with last winner
                    rivals.pop()
                    rivals.append(chance) #variable in rivals has the highest ratio
            else:
                rivals.append(chance)
            not_zero_ratio_temporary.remove(chance) #removing used row
        winers.append(rivals[0])
    print(winers)
    print(len(winers))

    return winers


def hybridization(population, winers, probability, gen):
    new_population = []
    while len(winers) != 0:
        #print('winners', len(winers))
        chance_for_hybrid = random.random() #git
        if chance_for_hybrid <= probability: #git
            place_of_hybrid = random.randrange(gen)
            child1 = np.concatenate(([population[winers[0],  : place_of_hybrid], population[winers[1], place_of_hybrid - gen:]]))   #git
            child2 = np.concatenate(([population[winers[1], :place_of_hybrid], population[winers[0], place_of_hybrid - gen:]]))  #git
            new_population.append(child1)
            new_population.append(child2)
            #print(child1)
            #print(child2)
            winers.pop(0)
            winers.pop(0)

        else:
            winers.pop(0)
            winers.pop(0)
    new_population = np.asanyarray(new_population)
    print(new_population)

    return new_population






def mutacja_test(population2, chance):
    population2_size = population2.shape

    for i in range(population2_size[1]):
        chance_for_mutation = random.random()
        # print(a)
        if chance_for_mutation < chance:
            mutation_place = random.randint(0, genes - 1)
            # print('b=',b)
            # print(popu[i])

            if population2[i, mutation_place] == 1:  # mutation
                population2[i, mutation_place] = 0
            else:
                population2[i, mutation_place] = 1
            # print(popu[i])
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
population = populationn(genes, individual)

for i in range(2):
    #print(table_of_items)
    #print('capacity:', capacity)
    #fcelu_test()
    #print(population)
    backpack_stats = calc_backpack(population, table_of_items)
    #print(backpack_stats)
    adaptation = rating(backpack_stats, capacity)
    #print(adaptation)
    best40 = tournament(population, adaptation)
    #print('assdasdasdsaadadssdasas' ,int((len(population[:,0]) * 0.4)))
    population = hybridization(population, best40, probability=0.85, gen=genes)
    mutacja_test(population, 0.02)
