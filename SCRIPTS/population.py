# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:53:36 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
import random

class Person:
    
    def __init__(self, wealth_base):
        
        global daily_deaths
        global daily_cases
        global hospital_occupation
        
        self.resistance        = np.random.normal(loc = 0.5, scale = 0.23)
        self.fanciness         = np.random(wealth_base)
        self.influence         = np.random.normal(loc = 0.5, scale = 0.23)
        self.age               = np.random()
        self.disease           = random.choice(self.age)
        if self.disease == 1:
            self.disease_intensity = np.random(self.age)            
        self.transportation    = random.choices(self.fanciness)
        self.lunch_routine     = random.choices(self.fanciness)
        
        
person = Person(0.6)
