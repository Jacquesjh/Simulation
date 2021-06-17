# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:18:17 2021

@author: Joao
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from scipy.spatial import ConvexHull

class CommercialRegion():
    
    def __init__(self, distance, area, x, y):
        
        self.color    = 'blue'
        self.distance = distance
        self.area     = area
        self.x_       = x
        self.y_       = y
        
class DomesticRegion():

    def __init__(self, distance, area, x, y):
        self.color    = 'green'
        self.distance = distance
        self.area     = area
        self.x_       = x
        self.y_       = y
        self.wealth   = 
        
class IndustrialRegion():

    def __init__(self, distance, area, x, y):
        self.color    = 'orange'
        self.distance = distance
        self.area     = area
        self.x_       = x
        self.y_       = y

def create_regions(number_regions, scale, std):
    
    city_center    = [scale/2, scale/2]
    max_distance   = pow(2*scale/2, 1/2)
    region_centers = np.random.normal(scale/2, std, (number_regions, 2))
    region_areas   = region_area(region_centers)
    regions        = []
    
    for i in range(len(region_centers)):
        
        area = region_areas[i]
        x    = region_centers[i, 0]
        y    = region_centers[i, 1]
        distance_from_center = pow(pow(city_center[0] - x, 2) + 
                                   pow(city_center[1] - y, 2), 1/2)
        
        ## Weights of probabilities of each type o region
        commercial_weight = 0.8*pow(np.e, - pow(distance_from_center, 2)/(2*scale)) + 0.1
        
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
            region = DomesticRegion(distance_from_center, area, x, y)
            regions.append(region)
            
        if region_type == ['Commercial']:
            region = CommercialRegion(distance_from_center, area, x, y)
            regions.append(region)
            
        if region_type == ['Industrial']:
            region = IndustrialRegion(distance_from_center, area, x, y)
            regions.append(region)
        
    return regions
        
def region_area(region_centers):
    
    v   = Voronoi(region_centers)
    area = np.zeros(v.npoints)
    
    for i, reg_num in enumerate(v.point_region):
        indices = v.regions[reg_num]
        
        if -1 in indices:
            area[i] = 0
            
        else:
            area[i] = ConvexHull(v.vertices[indices]).volume
            
    area = np.where(area == 0, np.mean(area), area)
    return area


region = create_regions(30, 100, 15)

for each in region:
    plt.scatter(each.x_, each.y_, color = each.color, linewidth = 7)

distance = np.arange(0, 70, 1)
area = np.arange(50, 250, 10)
wealth = pow(np.e, - pow(pow(145, 1/2)/distance, 2))
plt.plot(distance, wealth)
