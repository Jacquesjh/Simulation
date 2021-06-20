# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:18:17 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
import random
from population import *
from utils import *

class CommercialRegion():    
    def __init__(self, distance, area, x, y):        
        self.type     = 'Commercial'
        self.color    = 'blue'
        self.distance = distance
        self.area     = area
        self.x        = x
        self.y        = y
    
class House():
    def __init__(self, distance, color, wealth_base, area):
        self.type        = 'House'
        self.color       = color
        self.distance    = distance
        self.wealth      = wealth_base
        self.num_members = int(np.random.normal(loc = (4 + 1/wealth_base), scale = 1/wealth_base))
        if self.num_members < 1:
            self.num_members = 1
        self.members     = {}
        
    def generate_house_members(self):
        for i in range(self.num_members):
            self.members[i] = Person(self.wealth)
        
    def get_all_members(self):
        people = []
            
        for member in self.members:
            people.append(member)
                
        return people
        
    def num_state_members(self, state):
        '''Catch the number of members in a house in the specified state
        
        state = 'Susceptible', 'Infected', 'Immune', 'Dead'
        '''
        num_state = 0
        
        for member in self.members:
            if member.type == 'Infected':
                num_state += 1
            
        return num_state
                           
    def get_state_members(self, state):
        '''Create a list of members in a house in the specified state
            
            state = 'Susceptible', 'Infected', 'Immune', 'Dead'
        '''
        list_members = []
            
        for member in self.members:
            if member.type == state:
                list_members.append(member)
                
        return list_members
        
class DomesticRegion():
    def __init__(self, distance, area, x, y, scale):
        self.type          = 'Domestic'
        self.color         = 'green'
        self.distance      = distance
        if area > pow(np.pi*pow(scale, 1/2), 2):
            self.area = pow(np.pi*pow(scale, 1/2), 2)/2
        else:
            self.area          = area
        self.x             = x
        self.y             = y
        self.wealth        = 0.8/(1 + distance*pow(np.e, - scale/area)) + 0.2
        self.num_buildings = int(abs(np.random.normal(loc = (pow(self.area/np.pi, 1/2)/self.wealth),
                                                      scale = distance*pow(scale, 1/2)/self.wealth)))
        self.buildings     = {}
        for i in range(self.num_buildings):
            building          = House(distance = self.distance, color = self.color, wealth_base = self.wealth, area = self.area)
            self.buildings[i] = building
        
        
    def get_wealth(self):
        return self.wealth
    
    def get_xy(self):
        return self.x, self.y
    
    def get_area(self):
        return self.area
    
    def get_distance(self):
        return self.distance
    
    def get_region_population(self):
        region_population = []
        for house in self.buildings:
            members = house.get_members()
            
            for member in members:
                region_population.append(member)
                
        return region_population
    
    def num_state_members(self, state):
        num_state = 0
        
        for building in self.buildings:
            num_state += building.num_state_members(state)
            
        return num_state
    
    def get_state_members(self, state):
        list_members = []
        
        for building in self.buildings:
            for member in building.get_state_members(state):
                list_members.append(member)
                
        return list_members
    
    def generate_region_population(self):
        for building in self.buildings:
            building.generate_house_members()
            
    def get_buildings(self):
        return self.buildings
            
class IndustrialRegion():
    def __init__(self, distance, area, x, y):        
        self.type     = 'Industrial'
        self.color    = 'orange'
        self.distance = distance
        self.area     = area
        self.x        = x
        self.y        = y
