# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 23:12:28 2021

@author: Shaunak_Sensarma
"""

#Class for person name (first name and last name) and amount payable for parking.
#class is called from database code to maintain record of persons.

class Person:
    """A sample person class"""

    #initialising name and payable amount
    
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        print(last)

    #Email of person.

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    #CREATING FULL NAME FROM FIRST NAME AND LAST NAME.
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "person('{}', '{}', {})".format(self.first, self.last, self.pay)