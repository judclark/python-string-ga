from fuzzywuzzy import fuzz
import random
import string

class Word:

    def __init__(self, length):

        self.string = ''.join(random.choice(string.printable) for char in range(length))
        self.fitness = -1

    def __str__(self):
        return 'Word: ' + str(self.string) + ' Fitness: ' + str(self.fitness)



def main(population, generations, input_str, length, mut_perc):

    words = init_word(population, length)

    for generation in range(generations):

        print("Generation " + str(generation) + ": ")

        words = fitness(words, input_str)
        words = selection(words)
        words = crossover(words, length, population)
        words = mutation(words, mut_perc)

        for word in words:
            if(word.fitness >= 1.0):
                print("Complete!")
                exit(0);


# INITIALIZE POPULATION #
def init_word(population, length):
    words = []
    for each in range(population):
        words.append(Word(length))

    return words


# UPDATE POPULATIONS FITNESS ACCORDING TO TARGET WORD #
def fitness(words, target):
    for word in words:
        score = 0
        for i in range(len(word.string)):

            if(word.string[i] == target[i]):
                score= score + 1

        word.fitness = score/len(word.string)
    return words


# SORT THE POPULATION BY BEST FITNESS SCORE AND SELECT THE BEST#
def selection(words):
    words = sorted(words, key=lambda word: word.fitness, reverse=True)
    print ('\n'.join(map(str, words)))
    words = words[:int(len(words)/5)]

    return words

# CREATES NEW POPULATION FROM THE BEST OF PREV GENERATION #
def crossover(words, str_len,population):
    offspring = []
    for each in range(int((population-len(words))/2)):
        parent_1 = random.choice(words)
        parent_2 = random.choice(words)

        child_1 = Word(str_len)
        child_2 = Word(str_len)

        rand_index = random.randint(0, str_len)
        child_1.string = parent_1.string[:rand_index] + parent_2.string[rand_index:]
        child_2.string = parent_1.string[:rand_index] + parent_2.string[rand_index:]

        offspring.append(child_1)
        offspring.append(child_2)

    words.extend(offspring)

    return words


def mutation(words, mut_perc):
    for word in words:
        mutate = random.randint(1, 100)
        if(mutate <= mut_perc) :
            letter_index = random.randint(0, len(word.string)-1)
            word.string = word.string[:letter_index] + random.choice(string.printable) + word.string[letter_index+1:]

    return words

# SHOULD RUN FASTER IF THE OPONENENT IS FASTER #

if __name__ == '__main__':
    population = 50
    generations = 1000
    mut_perc = 5
    input_str = "Hello."
    str_len = len(input_str)
    main(population, generations, input_str, str_len, mut_perc)
