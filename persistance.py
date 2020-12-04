import atexit
import sqlite3

DB_NAME = 'moncafe.db'


# Data Transfer Objects:
class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Coffee_stand:
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Activity:
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


# --------------------------------------------------------------------------------

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
            INSERT INTO suppliers (id,name,contact_information) VALUES (?, ?,?)
        """, [supplier.id, supplier.name, supplier.contact_information])

    # def find(self, num):
    #     c = self._conn.cursor()
    #     c.execute("""
    #             SELECT num,expected_output FROM suppliers WHERE num = ?
    #         """, [num])
    #
    #     return _Suppliers(*c.fetchone())


class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO employees (id,name,salary,coffee_stand) VALUES (?, ?,?,?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def find(self, employee_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM employees WHERE id = ?
        """, [employee_id])
        return Employee(*c.fetchone())


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
            INSERT INTO products (id, description, price,quantity) VALUES (?, ?, ?,?)
        """, [product.id, product.description, product.price, product.quantity])

    # def find_all(self):
    #     c = self._conn.cursor()
    #     all = c.execute("""
    #         SELECT student_id, assignment_num, grade FROM grades
    #     """).fetchall()
    #
    #     return [Grade(*row) for row in all]


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
                INSERT INTO coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
            """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])
    #
    # def find_all(self):
    #     c = self._conn.cursor()
    #     all = c.execute("""
    #             SELECT student_id, assignment_num, grade FROM grades
    #         """).fetchall()
    #     return [Grade(*row) for row in all]


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
                INSERT INTO activities (product_id,quantity, activator_id,date) VALUES (?, ?,?,?)
            """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    #
    # def find_all(self):
    #     c = self._conn.cursor()
    #     all = c.execute("""
    #             SELECT student_id, assignment_num, grade FROM grades
    #         """).fetchall()
    #     return [Grade(*row) for row in all]


# ------------------------------------------------------------------------------------


class _Repository:

    # def __init__(self):
    #     self._conn = sqlite3.connect(DB_NAME)
    #     self.suppliers = _Suppliers(self._conn)
    #     self.employees = _Employees(self._conn)
    #     self.products = _Products(self._conn)
    #     self.coffee_stands = _Coffee_stands(self._conn)
    #     self.activities = _Activities(self._conn)

    def create_repo(self):
        self._conn = sqlite3.connect(DB_NAME)
        self.suppliers = _Suppliers(self._conn)
        self.employees = _Employees(self._conn)
        self.products = _Products(self._conn)
        self.coffee_stands = _Coffee_stands(self._conn)
        self.activities = _Activities(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()
        # os.remove('moncafe.db')  # For debug only!!!!

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id  INTEGER PRIMARY KEY,
                name    TEXT    NOT NULL,
                salary  REAL NOT NULL,
                coffee_stand    INTEGER INTEGER REFERENCES Coffee_stand(id) 
            );
    
            CREATE TABLE suppliers (
                id  INTEGER PRIMARY KEY,
                name    TEXT    NOT NULL, 
                contact_information TEXT
            );
             
            CREATE TABLE coffee_stands (
                id  INTEGER PRIMARY KEY,
                location    TEXT    NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE products (
                id  INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price   REAL    NOT NULL,
                quantity    INTEGER NOT NULL
            );
             
            CREATE TABLE activities (
                product_id  INTEGER INTEGER REFERENCES Product(id),
                quantity    INTEGER NOT NULL,
                activator_id    INTEGER    NOT NULL,
                date    DATE    NOT NULL
            );
         """)

    def findProduct(self, id):
        int_id = int(id)
        c = self._conn.cursor()
        all = c.execute("""SELECT id,description,price ,quantity FROM products WHERE id = ?"""
                        , [int_id])
        return all

    def updateProduct(self, ID, Q):
        int_id = int(ID)
        int_q = int(Q)
        c = self._conn.cursor()
        c.execute("""UPDATE products SET quantity = (?) WHERE id=(?)
             """, [int_q, int_id])
        return

    def findAllEmployee(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM employees ORDER BY id""")
        return all

    def findAllProducts(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM products ORDER BY id""")
        return all

    def findAllSuppliers(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM suppliers ORDER BY id""")
        return all

    def findAllActivities(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM activities ORDER BY date""")
        return all

    def findAllCoffee_stands(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM coffee_stands ORDER BY id""")
        return all

    def findActivitiesReport(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT activities.date, products.description , products.quantity , employees.name , suppliers.name
        FROM activities
        LEFT JOIN products ON products.id = activities.product_id 
        LEFT JOIN Employees ON employees.id = activities.activator_id 
        LEFT JOIN Suppliers ON suppliers.id = activities.activator_id
        ORDER BY date""").fetchall()
        return all


    def findAllEmployeeByName(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM employees ORDER BY name""")
        return all


    def findLocationByName(self, empName):
        c = self._conn.cursor()
        stand = c.execute("""SELECT coffee_stand FROM employees WHERE name=(?)""", [empName]).fetchone()
        cofStand = stand[0]
        location = c.execute("""SELECT location FROM coffee_stands WHERE id=(?)""", [cofStand]).fetchone()
        return location[0]

    def findTotalSalesIncome(self, empId):
        c = self._conn.cursor()
        products = c.execute("""SELECT product_id,quantity FROM activities WHERE activator_id=(?)""", [empId])
        sum = 0
        for prod in products:
            if prod[1] > 0:
                prodPrice = c.execute("""SELECT price FROM products WHERE id=(?)""", [prod[0]])
                sum = sum + prodPrice * prod[1]
        return sum


repo = _Repository()
atexit.register(repo._close)
