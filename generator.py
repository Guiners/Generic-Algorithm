
import numpy as np
import random as random
import pandas as pd
import pygame
import os
import time

file = np.loadtxt('ks_50_0', dtype=int)
genes = int(file[0,0].copy())
#individual = 16
capacity = file[0,1].copy()
#print(file[0,1].copy())
items = file[1:,].copy()

#creating dataframe
ratio = []
for i in range(genes):
    ratio.append(items[i,0]/items[i,1])

data = {
        'value': items[:,0],
        'weight': items[:,1],
        'ratio': ratio }

table_of_items = pd.DataFrame(data, columns=['value', 'weight', 'ratio'])
#table_of_items = table_of_items.sort_values('ratio', ascending = False)  # sorting data frame
#table_of_items = table_of_items.reset_index(drop=True)

#poloso
def fcelu_test():  # test
    weight_for_fcelu = 0
    bound = 0  # biggest value possible
    number_of_row = 0  # number of row
    storage = 0

    for i in range(genes):
        if weight_for_fcelu < capacity:
            bound += table_of_items.iat[number_of_row, 1]  # adding value of another item
            weight_for_fcelu += table_of_items.iat[number_of_row, 2]  # adding weight of another item
            if weight_for_fcelu < capacity:
                number_of_row += 1  # getting in to lower row

            else:
                bound -= table_of_items.iat[number_of_row, 1]  # deleting value of item which made backpack too heavy
                weight_for_fcelu -= table_of_items.iat[
                    number_of_row, 2]  # deleting weight of item which made backpack too heavy
                break
                """
                storage = capacity - weight_for_fcelu  # counting how much weight it can accualy fit in
                weight_for_fcelu += storage  # adding this value
                # print('p=',p,'/',df.iat[l+1,2])
                storage = storage / table_of_items.iat[number_of_row + 1, 2]  # counting value of left space
                # print('p=', p)
                # print('p', p, '*',df.iat[l+1,1])
                storage = storage * table_of_items.iat[number_of_row + 1, 1]  # counting value of left space
                # print('=',p)
                bound += round(storage, 2)  # adding it to value
                """
        break

        if weight_for_fcelu == capacity:  # ending the loop
            break
    print('bound =', bound, 'weight_fcelu =', weight_for_fcelu)


def populationn(gen, individual):
    populatioon = np.zeros((individual, gen)) #makeing array of 0
    for i in range(individual):
        weight = 0 #weight of individual
        place = 0 #item to take
        for j in range(gen):
            place = random.randrange(0, gen)
            b = random.random() #take or not the item
            if b > 0.49:
                populatioon[i, place] = 1 #addin item
                weight += table_of_items.iat[place,1]
                if weight > capacity: #if its in capacity
                  populatioon[i,place] = 0

    return populatioon


def calc_backpack(population, data): #tu moze byc bład
    population_size = population.shape
    values_weights = np.zeros((population_size[0],2))
    for i in range(population_size[0]):
        for j in range(population_size[1]):
            if population[i, j] == 1:
                values_weights[i,0] += data.iat[j,0] #value
                values_weights[i,1] += data.iat[j,1] #weight
   # print(values_weights)
    return values_weights




def rating(stats, capacity, best_all):
    best_in_pop = 0
    stats_size = stats.shape
    rate = np.zeros((stats_size[0],))
    for i in range(stats_size[0]):
        if stats[i, 1] <= capacity: # checking if weight of this backpack is in capacity
            if stats[i, 0] > 0:  # u cant divide by 0
                rate[i] += stats[i, 0]
            else:
                rate[i] = 0

            if rate.item(i) >= best_all: #getting best individual in all population
               best_all = rate.item(i)

            if rate.item(i) > best_in_pop: #getting best individual in this population
                best_in_pop = rate.item(i)
        else:
            rate[i] = 0

    #print('o',rate)
    return rate, best_all, best_in_pop

#teraz funkcja selekcji - turniejowa


#przebudowac
def tournament(population, rating, number):
    winers = []  #best individuals

    not_zero_ratio = []  # nuumber of rows, where weight of backpack < capacity
    average = []
    for i in range(len(population[:, 0])):
        not_zero_ratio.append(i)  # nuumber of rows, where weight of backpack =< capacity
        average.append(rating[i])

    for k in range(int((len(population[:, 0])))):
        rivals = []
        not_zero_ratio_temporary = not_zero_ratio.copy()  # making copy of the list
        for j in range(int((len(population[:, 0]) * number))):  # random take 40 individuals and choosing the best
            chance = random.choice(not_zero_ratio_temporary)
            #print('kupa',j,chance)
            #print(population[chance])
            if len(rivals) > 0:
                #print(rating[rivals[0]], '<', rating[chance])
                if rating[rivals[0]] < rating[chance]:  # comparing new row with last winner
                    rivals.pop()
                    rivals.append(chance)  # variable in rivals has the highest ratio
            else:
                rivals.append(chance)
            not_zero_ratio_temporary.remove(chance)  # removing used row
        winers.append(rivals[0])

    average = sum(average) / len(average)
    #xprint(winers)
    #print(len(winers))

    return winers, average


#przejrzec
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
            child1 = population[winers[0]]
            child2 = population[winers[1]]
            new_population.append(child1)
            new_population.append(child2)
            winers.pop(0)
            winers.pop(0)

    new_population = np.asanyarray(new_population)

    #print(new_population)

    return new_population





#przejrzec
def mutacja_test(population2, chance, genes, number):
    population2_size = population2.shape
    for i in range(population2_size[0]):
        chance_for_mutation = random.random()
        # print(a)
        if chance_for_mutation < chance:
            for k in range(number):
                mutation_place = random.randint(0, genes - 1)
                # print('b=',b)
                # print(popu[i])
                ones = []
                zeros = []

                if population2[i, mutation_place] == 1:  # mutation
                    population2[i, mutation_place] = 0
                    for k in range(len(population2[i,:])):
                        if population2[i,k] == 0:
                            zeros.append(k)
                            #print(zeros)
                    population2[i,(random.choice(zeros))] = 0



                else:
                    population2[i, mutation_place] = 1
                    for k in range(len(population2[i,:])):
                        if population2[i,k] == 1:
                            ones.append(k)
                            #print(ones)
                    population2[i,(random.choice(ones))] = 0

    return population2

            # print(popu[i])
            #print("osobnik numer", i, "zmutował")



#print("population")
#for i in range(individual):
    #print(population[i])
#print(table_of_items)
#print('capacity:', capacity)

#stats
individual = 40
population_number = 10000
number_of_individuals_in_tournament = 0.4
chance_for_mutation = 0.5
chance_for_hybridization = 0.85
number_of_changes_in_mutation = 1
best_in_all = 0
population = 0
i = 0
average = 0
best_in_population = 0

pygame.init()

screen_width = 1300
screen_height = 800
background_colour = (0,0,0)
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(background_colour)
pygame.display.set_caption("Generic Algorithm")
font = pygame.font.Font(os.path.join("font.ttf"), 25)
font_color = (0, 255, 65)

clock = pygame.time.Clock()


""""
nump = np.random.randint(2, size=50)

nump1 = np.array2string(nump, separator=".")
text_best_individual = font.render(nump1, True, (0,255,65))

file_name = font.render('File name: ' + "x", True, (0,255,65))
text1 = font.render('Population number: ' + str(i), True, (0,255,65))
text2 = font.render('Best individual in all populations: ' + str(best_in_all), True, (0,255,65))
text3 = font.render('Avrage: ' + str(avrage), True, (0,255,65))
text4 = font.render('Currently best individual: ' + str(best_in_population), True, (0,255,65))
text5 = font.render('Individuals: ' + str(individual), True, (0,255,65))
text6 = font.render('Genes: ' + str(genes), True, (0,255,65))
text7 = font.render('Chance for mutation: ' + str(chance_for_mutation), True, (0,255,65))
text8 = font.render('Click SPACE to start', True, (0,255,65))
nump = np.random.randint(2, size=50)
"""


def draw():
    screen.fill(background_colour)

    #nump = np.random.randint(2, size=50)#zmiana potem na najlepszego
    #nump1 = np.array2string(nump, separator=".")
    text1 = font.render('Population number: ' + str(i), True, font_color)
    text2 = font.render('Best individual in all populations: ' + str(best_in_all), True, font_color)
    text3 = font.render('Average: ' + str(average), True, font_color)
    text4 = font.render('Currently best individual: ' + str(best_in_population), True, font_color)
    text5 = font.render('Individuals: ' + str(individual), True, font_color)
    text6 = font.render('Genes: ' + str(genes), True, font_color)
    text7 = font.render('Chance for mutation: ' + str(chance_for_mutation), True, font_color)
    text8 = font.render('Click SPACE to start', True, font_color)


    screen.blit(text1, (10, 10))
    screen.blit(text3, (10, (20 + text1.get_height())))
    screen.blit(text2, (10, (30 + text1.get_height() * 2)))
    screen.blit(text4, (10, (40 + text1.get_height() * 3)))
    screen.blit(text5, (10, (50 + text1.get_height() * 4)))
    screen.blit(text6, (10, (60 + text1.get_height() * 5)))
    screen.blit(text7, (10, (70 + text1.get_height() * 6)))
    screen.blit(text8, (10, (screen_height - text1.get_height())))

    pygame.display.flip()
    pygame.display.update()


draw()
########matrix
def matrix(population):
    startx = 480
    starty = 60
    sizex = screen_width - startx - 10
    sizey = screen_height - starty - 10
    pop_size = population.shape
    rect_sizex = sizex/pop_size[1]    #size of single rect
    rect_sizey = sizey/pop_size[0]
    text1 = font.render('G  E  N  E  S', True, font_color)
    screen.blit(text1, (startx + sizex * 0.5 - text1.get_width(), starty - 50 ))
    #text2 = font.render('...' + str(genes - 2) + ',' + str(genes - 1) + ',' + str(genes), True, font_color)
    #screen.blit(text2, (startx + sizex - text2.get_width(), starty - 50 ))
    name = 'INDIVIDUALS'
    counter = 0
    for k in name:
        counter +=1
        text2 = font.render(str(k), True, font_color)
        screen.blit(text2, (startx - text2.get_width() - 25, starty + 100 + (text2.get_height() * counter)))

    pygame.display.flip()
    pygame.display.update()
    for i in range(pop_size[0]):
        for j in range(pop_size[1]):
            if population[i,j] == 1:
                pygame.draw.rect(screen,font_color,(startx + rect_sizex*j, starty + rect_sizey*i,rect_sizex,rect_sizey), 2)
            else:
                pygame.draw.rect(screen,(0,0,0),(startx + rect_sizex*j, starty + rect_sizey*i,rect_sizex,rect_sizey))

        """if i%2 == 0:
            pygame.display.flip()
            pygame.display.update()"""

    pygame.display.flip()
    pygame.display.update()
running = True
while running:
    clock.tick(20)
    keys =pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print(1)
        while best_in_all == 0:
            best_in_all = 0
            population = populationn(genes, individual)
            backpack_stats = calc_backpack(population, table_of_items)
            adaptation, best_in_all, best_in_population = rating(backpack_stats , capacity, best_in_all)

        for i in range(population_number):
            matrix(population)
            backpack_stats = calc_backpack(population, table_of_items)
            adaptation, best_in_all, best_in_population = rating(backpack_stats, capacity, best_in_all)
            print("the best individual in population number",i ,"has", best_in_population, 'value')
            #print(adaptation)
            best40, average = tournament(population, adaptation, number_of_individuals_in_tournament)
            print("average of this population is equal", average)
            #print('assdasdasdsaadadssdasas' ,int((len(population[:,0]) * 0.4)))
            population = hybridization(population, best40, probability= chance_for_hybridization, gen=genes)
            population = mutacja_test(population, chance_for_mutation, genes, number_of_changes_in_mutation)
            draw()
            time.sleep(0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


