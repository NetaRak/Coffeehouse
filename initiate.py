import os

import persistance
from persistance import repo


def fill_tables():
    f = open("config.txt", "r")
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        splited = line.split(',')
        if splited[0] == "C":
            coffee_stand = persistance.Coffee_stand(splited[1], splited[2][1:], splited[3])
            repo.coffee_stands.insert(coffee_stand)
        elif splited[0] == "S":
            supplier = persistance.Supplier(splited[1], splited[2][1:], splited[3][1:])
            repo.suppliers.insert(supplier)
        elif splited[0] == "E":
            employee = persistance.Employee(splited[1], splited[2][1:], splited[3], splited[4])
            repo.employees.insert(employee)
        elif splited[0] == "P":
            product = persistance.Product(splited[1], splited[2][1:], splited[3], 0)
            repo.products.insert(product)


if os.path.isfile('moncafe.db'):
    os.remove('moncafe.db')
repo.create_repo()
repo.create_tables()
fill_tables()

