# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:53:36 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
import random

def normal(mean, std):
    
    result = np.random.normal(loc = mean, scale = std)
    if result < 0:
        result = 0
    if result > 1:
        result = 1
        
    return result

class Person:
    
    def __init__(self, wealth_base, house):
        
        self.awareness         = normal(0.5, 0.3)
        self.resistance        = normal(0.5, 0.23)
        self.fanciness         = normal(wealth_base, 0.23)
        self.influence         = normal(0.5, 0.23)
        self.age               = int(np.random.normal(loc = 35, scale = 15))
        if self.age < 18:
            self.age = 18
        
        self.health            = (random.choices(['Healthy', 'Unhealthy'],
                                                 weights = (1 - (0.5 + (self.age - 35)/abs(self.age + 35)), 0.5 + (self.age - 35)/abs(self.age + 35))))[0]
        if self.health == 'Unhealthy':
            self.disease_intensity = normal(0.5 + (self.age - 35)/(self.age + 35), 0.23)
        else:
            self.disease_intensity = 0
            
        self.transportation    = (random.choices(['Public', 'Private'],
                                                weights = (1 - normal((0.5 + self.fanciness)/2, 0.23), normal((0.5 + self.fanciness)/2, 0.23))))[0]
        self.lunch_routine     = (random.choices(['Alone', 'Restaurant'],
                                                weights = (1 - normal((0.5 + self.fanciness)/2, 0.23), normal((0.5 + self.fanciness)/2, 0.23))))[0]
        self.house             = house
        self.workplace         = 0
        self.contagius         = 0
        
        
        
    def update_workplace(self, workplace):
        self.workplace = workplace
   
    def update_risk(self, new_risk):                                           ## Updates at the start of each day
        self.resistance = self.resistance - self.awareness*pow(new_risk, 3/2)
        if self.resistance < 0:
            self.resistance = 0
        
    def update_resistance(self):                                               ## Updates at the start of each day
        self.resistance = self.resistance*(1 + pow(self.resistance, 3/2))
        if self.resitance > 1:
            self.resistance = 1
    
    def interaction_routine(self, step):
        
        if step == 0:
            self.routine_0()
        if step == 1:
            self.routine_1()
        if step == 2:
            self.routine_2()
        if step == 3:
            self.routine_3()
        if step == 4:
            self.routine_4()
        if step == 5:
            self.routine_5()
        if step == 6:
            self.routine_6()
            
    def routine_0(self):                                                       ## At home
        protection = self.protection
        infected_members = self.house.get_state_members('Infected')
        if len(infected_members) != 0:
            contagius_total = 0
            
            for member in infected_members:
                contagius_total += member.contagius
            
            average_contagius = total/len(infected_members)
            contagius_factor  = pow(average_contagiu, 1/len(infected_members))
            
            contagius_probability = (1 - self.protection)*contagius_factor
            
            result_infection = (random.choices(['Not Infected', 'Infected'],
                                                  weights = (1 - contagius_probability, contagius_probability)))[0]
            if result_infection == 'Infected':
                self = Infected(self)
            
    def routine_1(self):                                                       ## Going to work
            
    def routine_2(self):                                                       ## At work
            
    def routine_3(self):                                                       ## Lunch time
            
    def routine_4(self):                                                       ## At work
            
    def routine_5(self):                                                       ## Going home
            
    def routine_6(self):                                                       ## At home
        
class Susceptible(Person):
    
    def __init__(self, Person):
        
        self.type              = 'Susceptible'
        self.awareness         = Person.awareness
        self.resistance        = Person.resistance
        self.fanciness         = Person.fanciness
        self.influence         = Person.influence
        self.age               = Person.age
        self.health            = Person.health
        self.disease_intensity = Person.disease_intensity
        self.transportation    = Person.transportation
        self.lunch_routine     = Person.lunch_routine
        self.house             = Person.house
        self.workplace         = Person.workplace
        self.contagius         = Person.contagius
        self.protection        = 1 - pow(Person.resistance, 3/2)
        
    def update_risk(self, new_risk):                                           ## Updates at the start of each day
        self.resistance = self.resistance - self.awareness*pow(new_risk, 3/2)
        if self.resistance < 0:
            self.resistance = 0
        
    def update_resistance(self):                                               ## Updates at the start of each day
        self.resistance = self.resistance*(1 + pow(self.resistance, 3/2))
        if self.resitance > 1:
            self.resistance = 1
    
class Infected(Person):
    
    def __init__(self, Person):
        
        self.type              = 'Infected'
        self.risk              = Person.risk
        self.awareness         = Person.awareness
        self.resistance        = Person.resistance
        self.fanciness         = Person.fanciness
        self.influence         = Person.influence
        self.age               = Person.age
        self.health            = Person.health
        self.disease_intensity = Person.disease_intensity
        self.house             = Person.house
        self.workplace         = Person.workplace
        
        
        
        
        
        
class Big:
    
    def __init__(self):
        self.num = 10
        
    def change_type(self):
        
        if self.type == 'Small':
            self.turn_to_medium()
        
        if self.type == 'Medium':
            self.turn_to_small()
        
        
        
class Small(Big):
    
    def __init__(self, Big):
        self.num = Big.num
        self.type = 'Small'
         
    def turn_to_medium(self):
        self = Medium(self)
        
class Medium(Big):
    
    def __init__(self, Big):
        self.num = Big.num
        self.type = 'Medium'
        
    def turn_to_small(self):
        self = Small(self)
        
        
        
        
a = Small(Big())
b = Medium(Big())
a.type
b.type
a.change_type()
b.change_type()
a.type
b.type
c = Medium(a)
