import random

# Generiere 10.000 Zufallszahlen und speichere sie in random.txt
with open('random.txt', 'w+') as file:
    for _ in range(10000):
        random_number = random.randint(1, 1000)
        file.write(f'{random_number}\n')