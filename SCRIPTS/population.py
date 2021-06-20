# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:53:36 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
import random
import utils

class Person:
    def __init__(self, wealth_base):  
        
        self.awareness         = utils.normal_01(0.5, 0.3)            
        #self.resistance        = utils.normal_01(0.5 - (self.awareness*risk), 0.23)
        self.resistance        = utils.normal_01(0.5 - (self.awareness), 0.23)            
        self.fanciness         = utils.normal_01(wealth_base, 0.23)
        self.influence         = utils.normal_01(0.5, 0.23)
        self.age               = np.random.normal(loc = 35, scale = 15)
        if self.age < 18:
            self.age = 18
        
        self.disease           = random.choice([0, 1], weights = [1 - (0.5 + (self.age - 35)/abs(self.age + 35)), 0.5 + (self.age - 35)/abs(self.age + 35)])        
        if self.disease == 1:
            self.disease_intensity = utils.normal_01((self.age - 35)/abs(self.age + 35), 0.23)
            
        self.transportation    = random.choices([0, 1], self.fanciness)             ## 0 = Public transportation (up to 40 others), 1 = Private transportation (2 to 4 others)
        self.lunch_routine     = random.choices([0, 1], self.fanciness)             ## 0 = Restaurant (up to 40 others), 1 = Lunching alone
        
    
person = Person(0.6)
