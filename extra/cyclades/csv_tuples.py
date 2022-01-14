from csv import reader
with open('sociopro.csv', 'r') as csvfile:
    reader = reader(csvfile, delimiter=';')
    output = tuple(map(tuple, reader))
    print(output)
