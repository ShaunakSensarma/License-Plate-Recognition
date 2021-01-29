# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:32:27 2021

@author: Shaunak_Sensarma
"""

#CREATING DATABASE to store individual names and their payable amount

#writing queries for inserting, getting person by name, updating payable amount
#and removing person from the database.

import sqlite3
from person import Person
conn = sqlite3.connect(':memory:')          #connecting to database.

c = conn.cursor()

#CREATE TABLE.

c.execute("""CREATE TABLE employees (
            first text,
            last text,
            pay integer
            )""")

#INSERTING NAME AND PAY VALUES IN TABLE

def insert_per(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

#GETTING NAMES

def get_per_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()

#UPDATING PAY VALUE
    
def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})

#REMOVING PERSONS.
        
def remove_per(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})

emp_1 = Person('Car', 'HR26DK8337', 50)
emp_2 = Person('Car', 'MH12DE1433', 100)

#INSERTION BY VALUE.

insert_per(emp_1)
insert_per(emp_2)
