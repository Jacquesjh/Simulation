# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:18:17 2021

@author: Joao
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull
from person import *

class CommercialRegion():
    
    def __init__(self, distance, area, x, y):
        
        self.type     = 'Commercial'
        self.color    = 'blue'
        self.distance = distance
        self.area     = area
        self.x_       = x
        self.y_       = y
    
class House():
    def __init__(self, distance, color, wealth_base, area):
        
        self.type        = 'House'
        self.color       = color
        self.distance    = distance
        self.wealth      = wealth_base
        self.num_members = int(np.random.normal((2/wealth)*3.5/(1 + 200*pow(np.e, - pow(area, 2)/2000)) + 1, 1/wealth,  1))
        self.members     = {}
        
    #def generate_members(self, wealth):
        
    def get_all_members(self):
        people = []
            
        for member in self.members:
            people.append(member)
                
        return people
        
    def num_state_members(self, state):
        '''Catch the number of members in a house in the specified state
        
        state = 'Susceptible', 'Infected', 'Immune', 'Dead'
        '''
        infected = 0
        
        for member in self.members:
            if member.type == 'Infected':
                infected += 1
            
        return infected
                           
    def get_state_members(self, state):
        '''Create a list of members in a house in the specified state
            
            state = 'Susceptible', 'Infected', 'Immune', 'Dead'
        '''
        infected = []
            
        for member in self.members:
            if member.type == state:
                infected.append(member)
                
        return infected
        
class DomesticRegion():

    def __init__(self, distance, area, x, y, scale):
        
        self.type          = 'Domestic'
        self.color         = 'green'
        self.distance      = distance
        self.area          = area
        self.x_            = x
        self.y_            = y
        self.wealth        = 0.8/(1 + distance*pow(np.e, - scale/area)) + 0.2
        self.num_buildings = int(np.random.normal(area*pow(scale, 1/4), distance*pow(scale, 1/2), 1))
        self.buildings     = {}
        
        
    def get_wealth(self):
        return self.wealth
    
    def get_xy(self):
        return self.x_, self.y_
    
    def get_area(self):
        return self.area
    
    def get_distance(self):
        return self.distance
    
    def create_buildings(self):
        for i in range(self.num_buildings):
            building = House(self.distance, self.color, self.wealth, self.area)
            self.buildings[i] = buildings
    
    def get_region_population(self):
        region_population = []
        for house in self.buildings:
            members = house.get_members()
            
            for member in members:
                region_population.append(member)
                
        return region_population
    
class IndustrialRegion():

    def __init__(self, distance, area, x, y):
        
        self.type     = 'Industrial'
        self.color    = 'orange'
        self.distance = distance
        self.area     = area
        self.x_       = x
        self.y_       = y

def create_regions(number_regions, scale, std):
    
    city_center         = [scale/2, scale/2]
    max_distance        = pow(2*scale/2, 1/2)
    region_centers      = np.random.normal(scale/2, std, (number_regions, 2))
    region_centers = np.append(region_centers, [[999,999], [-999,999], [999,-999], [-999,-999]], axis = 0)
    region_areas, vor   = region_area(region_centers)
    regions             = []
    
    for i in range(len(region_centers)):
        
        area = region_areas[i]
        x    = region_centers[i, 0]
        y    = region_centers[i, 1]
        distance_from_center = pow(pow(city_center[0] - x, 2) + 
                                   pow(city_center[1] - y, 2), 1/2)
        
        ## Weights of probabilities of each type o region
        commercial_weight = 0.7*pow(np.e, - pow(distance_from_center, 2)/(2*scale)) + 0.1
        
        if distance_from_center < 25:
            industrial_weight = 0.1
        
        else:
            industrial_weight = 0.8/(1 + scale*pow(np.e, - distance_from_center/pow(max_distance, 1/2)))
        
        domestic_weight = 1 - commercial_weight - industrial_weight        
        
        choices     = ('Domestic', 'Commercial', 'Industrial')
        region_type = random.choices(choices, weights = (domestic_weight, 
                                                         commercial_weight,
                                                         industrial_weight))
        
        if region_type == ['Domestic']:
            region = DomesticRegion(distance_from_center, area, x, y, scale)
            regions.append(region)
            
        if region_type == ['Commercial']:
            region = CommercialRegion(distance_from_center, area, x, y)
            regions.append(region)
            
        if region_type == ['Industrial']:
            region = IndustrialRegion(distance_from_center, area, x, y)
            regions.append(region)
        
    return regions, vor

def map_regions(regions, vor):
    
    voronoi_plot_2d(vor, show_points=True, show_vertices=False)
    for r in range(len(vor.point_region)):
        region = vor.regions[vor.point_region[r]]
        
        if regions[r].type == 'Domestic':
            color = 'green'
            
        if regions[r].type == 'Commercial':
            color = 'blue'
            
        if regions[r].type == 'Industrial':
            color = 'orange'
    
        if not -1 in region:
            polygon = [vor.vertices[i] for i in region]
            plt.fill(*zip(*polygon), color = color)
    plt.xlim((0, 100))
    plt.ylim((0, 100))
    plt.show()
            
def region_area(region_centers):
    
    vor  = Voronoi(region_centers)
    area = np.zeros(vor.npoints)
    
    
    for i, reg_num in enumerate(vor.point_region):
        indices = vor.regions[reg_num]
        
        if -1 in indices:
            area[i] = 0
            
        else:
            area[i] = ConvexHull(vor.vertices[indices]).volume
            
    area = np.where(area == 0, np.mean(area), area)
    return area, vor

#def create_population(region_list):
    