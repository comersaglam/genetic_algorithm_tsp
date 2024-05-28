   #*genetic algorithm steps
#*  1- we have a 9*9 data frame, we choose person like travelling salesman problem style. we choose a starting point in our dataframe. 
#* row is where are we and column is where we came from. then we choose next city as row --> column and choose a new row. For ex: 7,2=9 --> 3,7=2 --> 6,3=3 etc
#* in this example, our salesman start from 2,7,3,6...
#* So we visit every number btw 1:9 and dont visit any city more than once.

#*  2- encoding scheme is easy here, traits are already in base 10 numbers. we will think them as reverse ordered distances. 
#* so the 9 point is the fittest and 0 is the lowest
#* permutation encoding

#*  3- fitness function is easy too, we are not forced to determine it as a polinomial function. Sum of all traits is the fitness score
 
#*  4- selection scheme(roulette,rank,elitist)
#* (roulette = fitness score and surviving chance is proportional)(rank = rank of fitness is reversely proportional to surviving chance)
#* (elitist = if a parent is fitter than all offspring, it takes places of worst offspring) WE will just proceed with all of em one by one
 
#*  5- crossover scheme and probability
#* PMX(partially mapped crossover(partly pos partly order)), OX(ordered crossover(order based)), 
#* ERX(edge recombinations crossover(tsp like)), CX(cyclic crossover(pos based))
 
#*  6- mutation rate and system
#* types are basically translocation, inversion, swap and shuffling mutations, (insertion, deletion and duplication are not possible in TSP)
 
#*  7- when to stop
 
#*  8- how do we search the space? what the sample size should be?

#* my random solution cities is 731862954
#* max points without mutations is (probably) 88878586 = 58
#* max with mutations is 9(max point per travel)*8(number of travels) = 72 

import random
import copy

genetic_algorithm_df = [(0, 4, 6, 2, 8, 2, 2, 8, 2),
                        (3, 0, 5, 1, 7, 1, 2, 3, 5),
                        (8, 2, 0, 4, 6, 3, 2, 6, 2),
                        (2, 1, 2, 0, 3, 2, 1, 1, 1),
                        (4, 4, 4, 6, 0, 2, 7, 2, 5),
                        (3, 8, 3, 1, 1, 0, 1, 0, 1),
                        (4, 9, 8, 2, 4, 5, 0, 7, 4),
                        (3, 3, 2, 2, 5, 7, 4, 0, 4),
                        (1, 2, 0, 1, 8, 2, 8, 4, 0)]
gen_alg_df = genetic_algorithm_df

#* 9! is the total number of possible parents. is equal to ~360k.
#* sample size would be sqrt(n) =~ 600. i rounded it to 512 = 2^9, just in case.
#* for every 2 baby, we will choose 2 parents, chance to be chosen is on selection scheme. then crossover them and create 2 offsprings

gen = 0
n_parent = 0
genmax = 0
mutationrate = 0

class Person():
    def __init__(self, index, city, score):
         self.index = index
         self.city = city
         self.score = score
    

    def __repr__(self):
         return f"*i:{self.index} , c:{self.city} , s:{self.score}*"
    
    @staticmethod
    def city_to_score(citylist):#* we create our individuals with list of order of cities visited. this function calculates score of a person,

        score_city = []

        for i,j in enumerate(citylist):
            if i+1 < len(citylist):
                score_city.append(gen_alg_df[citylist[i]-1][citylist[i+1]-1])

        total_score_city = sum(score_city)**2

        return total_score_city
    
    

def choose_f0():    #* n_parent will be our sample size. we determined it to be 512 but you can adjust from here
                            #* this generation is just for starting. from now on we breed the individuals to create next generations.
   
    global n_parent
    f0_gen_list = []
    cities = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for i in range(n_parent):
        shuffled = copy.deepcopy(cities)
        random.shuffle(shuffled)
        f0_gen_list.append(Person(i, shuffled, Person.city_to_score(shuffled)))
    
    return f0_gen_list


#* f0_gen_list goes into this func, then every new gen will get into it.
def next_gen(generation):
#* I squared all survival points because linearity can't discriminate best fit people enough. It gives definitely more reaasonable results
    survival_list = []
    totalsurvival = 0
    global genmax
    genmax = 0

#* this loop creates a list like --> lets assume, generation list members has score of 50,35,15 respectively.
    for person in generation:
        if person.score > genmax:
            genmax = person.score
        totalsurvival += person.score
        survival_list.append(totalsurvival)

    return new_gen(generation, totalsurvival, survival_list)
        
        #TODO if you want to add rank selection, implement a function that turns scores into ranks. than create totalsurvival list accordingly
#* we will create a survival_list of [50,85,100]. then we will roll a dice btw 0-100(totalsurvivalscore) and decide which interval includes that number
#* that decision will be made by another function called choose_parent. then we got the parents to crossever.


def new_gen(generation,totalsurvival,survival_list):

    global n_parent
    global gen
    index = 0
    f1_generation = []

    while index < n_parent:
        parent_1 = generation[choose_parent((totalsurvival, survival_list))]
        parent_2 = generation[choose_parent((totalsurvival, survival_list))]
        f1= ox_crossover(parent_1,parent_2)
        f1_generation.append(Person(index, f1, Person.city_to_score(f1)))
        index += 1
    global gen
    gen += 1
    
    generation = f1_generation
    return generation
    #TODO if you want to add elitist selection, here the code of "compare if a parent is higher than every offspring" will be inserted


def choose_parent(x):
    totalsurvival = x[0]
    survival_list = x[1]

    lucky_no = random.randrange(0,totalsurvival)
 
    for i in survival_list:
        if lucky_no < i:
            indexofparent = survival_list.index(i)
            break

    return indexofparent


#* pmx is designed for tsp questions! But we will use OX bc i figured it out myself during the lecture time. pmx knowledge just popped up when i was searching recently
#* So ox func works as: you cut a slice from p1 an transmit it to offspring. Other places will be filled with remaining numbers but in order that p2 have
#* such as 123/4567 and 7536142 will be like 123 than 45 in order of p2 which is 7564. so the offspring will be 1237564. Believe it or not this works
def ox_crossover(p1,p2):

    cutpoint = random.randrange(0,len(p1.city))
    chromosome1 = p1.city[0:cutpoint]
    chromosome2 = []

    for chro in p2.city:
        if chro not in chromosome1:
            chromosome2.append(chro)

    offspring = chromosome1
    offspring.extend(chromosome2)

    global mutationrate
    #if random.randint(1,1000) <= mutationrate:
     #   offspring = swap_mutation(offspring)

    return offspring


#TODO make mutation rate bound to a variable that we can easily change
#* since we have 9 long data and i dont want mutations to be so drastic that it kills the purpose of genetic algorithm. I make small changes. Best candidate is swap
def swap_mutation(f1):

    x1 = random.randint(0,len(f1))
    x2 = random.randint(0,len(f1))
    if x1 == x2:
        swap_mutation(f1)
    f1[x1], f1[x2] = f1[x2], f1[x1]
    #!f1[x2] index out of range error
    return f1


#* if the last 100 generation wont make more than 2% difference, STOP. (score would be around 60-65, so 1 point means more than %1. thats why i picked %2)
def istimetostop(listofgenmax):#* Function that return True if no radical change happen for 100 generations.
    global gen
    # If we haven't reached 100 generations, continue
    if gen <= 100:
        return True
    else:
        recentlist = listofgenmax[-100:]
        min_recent = min(recentlist)
        max_recent = max(recentlist)

        # Avoid division by zero
        if min_recent == 0:
            return True

        # Check if there's less than 2% improvement
        if (max_recent - min_recent) / min_recent > 0.02:
            return True
        else:
            return False

    

def run_genalg(current_gen):#? Dont loop recursively. Since genalg need 1000+ generations, it overwhelms the computer.
    global n_parent, gen, genmax, mutationrate

    if gen == 0:
        current_gen = choose_f0()  # Initialize first generation
    else:
        totalsurvival = 0
        survival_list = []
        genmax = 0  # Reset genmax for the new generation
        for person in current_gen:
            totalsurvival += person.score
            survival_list.append(totalsurvival)
            if person.score > genmax:
                genmax = person.score  # Update genmax

        current_gen = new_gen(current_gen, totalsurvival, survival_list)
    gen += 1  # Increment generation count
    return current_gen



def main():
    global n_parent, gen, genmax, mutationrate
    n_parent, gen, genmax, mutationrate = 1024, 0, 0, 1  # Initialize parameters
    listofgenmax, currentgen = [], []
    abs_max= 0
    while istimetostop(listofgenmax):
        currentgen = run_genalg(currentgen)
        listofgenmax.append(genmax)  # Update listofgenmax with the max score of the current generation
        if genmax >= abs_max:
            abs_max = genmax  # Keep track of the absolute maximum score achieved so far
            
        #print(f"Generation: {currentgen}, Max Score: {genmax}")
        print(f"Max Score: {int(genmax**(1/2))}")
    print(f"absmax = {int(abs_max**(1/2))}")
        


    

if __name__ == "__main__":
    main()

#TODO It somehow finds 60 almost every time(which is max) and maintain it for like 10-50 generation.
#TODO But somehow it returns to 55 or 54 everytime and ends the generation there. I can't figure out why. just recheck it later