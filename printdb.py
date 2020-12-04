from persistance import repo


def printActivities():
    all = repo.findAllActivities()
    for row in all:
        print(row)


def printCoffee_stands():
    all = repo.findAllCoffee_stands()
    for row in all:
        print(row)


def printEmployees():
    all = repo.findAllEmployee()
    for row in all:
        print(row)


def printProducts():
    all = repo.findAllProducts()
    for row in all:
        print(row)


def printSuppliers():
    all = repo.findAllSuppliers()
    for row in all:
        print(row)


def printEmployeesReport():
    all = repo.findAllEmployeeByName()
    for row in all:
        name = row[1]
        salary = row[2]
        location = repo.findLocationByName(name)
        sum = repo.findTotalSalesIncome(name)
        print(name, salary, location, sum)


def printActivityReport():
    all = repo.findActivitiesReport()
    if len(all) > 0:
        print("Activities Report")
        for row in all:
            print(row)


def printdb():
    print("Activities")
    printActivities()
    print("Coffee stands")
    printCoffee_stands()
    print("Employees")
    printEmployees()
    print("Products")
    printProducts()
    print("Suppliers")
    printSuppliers()
    print("")
    print("Employees report")
    printEmployeesReport()
    print("")
    printActivityReport()


repo.create_repo()
printdb()