RESET_VALUE = 6
NEW_VALUE = RESET_VALUE + 2

Age = int
Population = dict[Age, int]

def step_forward(population: Population) -> Population:
    next_population: Population = {}
    for i in range(1, NEW_VALUE + 1):
        # Decrement ages
        next_population[i-1] = population.get(i, 0)
    # Add new births
    next_population[NEW_VALUE] = population.get(0, 0)
    # Put parents back into the population
    next_population.setdefault(RESET_VALUE, 0)
    next_population[RESET_VALUE] += population.get(0, 0)

    return next_population

if __name__ == '__main__':
    content: str = open('input.txt').read()
    ages: list[Age] = [int(val) for val in content.strip().split(',')]
    population: Population = {age: ages.count(age) for age in set(ages)}

    for _ in range(80):
        population = step_forward(population)

    total_population: int = sum(population.values())
    print('Part 1')
    print(total_population)

    # Part 2
    population: Population = {age: ages.count(age) for age in set(ages)}

    for _ in range(256):
        population = step_forward(population)

    total_population: int = sum(population.values())
    print('Part 2')
    print(total_population)
