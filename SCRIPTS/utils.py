# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 17:27:56 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull
from environment import *

def create_regions(number_regions, scale, std):
    
    city_center         = [scale/2, scale/2]
    max_distance        = pow(2*scale/2, 1/2)
    region_centers      = np.random.normal(scale/2, std, (number_regions - 4, 2))
    region_centers      = np.append(region_centers, [[999,999], [-999,999], [999,-999], [-999,-999]], axis = 0)
    region_areas, vor   = region_area(region_centers)
    regions             = []
    
    fix_vertices(vor)
    
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
            industrial_weight = 0.6/(1 + scale*pow(np.e, - distance_from_center/pow(max_distance, 1/2)))
        
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
    
    plt.figure(figsize = (30, 20))
    voronoi_plot_2d(vor, show_points = False, show_vertices = False)
    
    for r in range(len(vor.point_region)):
        region = vor.regions[vor.point_region[r]]
        
        if regions[r].type == 'Domestic':
            color = '#00AD2E'
            
        if regions[r].type == 'Commercial':
            color = '#0069AB'
            
        if regions[r].type == 'Industrial':
            color = '#AB6700'
    
        if not -1 in region:
            polygon = [vor.vertices[i] for i in region]
            plt.fill(*zip(*polygon), color = color, alpha = 0.8)
            
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

def fix_vertices(vor):
    for vertices in vor.vertices:
        if vertices[0] < -800:
            vertices[0] = vertices[0]/10 + 80
        else:
            if vertices[0] < -100:
                vertices[0] = vertices[0]/10 + 10
                
        if vertices[0] > 800:
            vertices[0] = vertices[0]/10 + 20
        else:
            if vertices[0] > 100:
                vertices[0] = vertices[0]/10 + 90
            
        if vertices[1] < -800:
            vertices[1] = vertices[1]/10 + 80
        else:
            if vertices[1] < -100:
                vertices[1] = vertices[1]/10 + 10
                
        if vertices[1] > 800:
            vertices[1] = vertices[1]/10 + 20
        else:
            
            if vertices[1] > 100:
                vertices[1] = vertices[1]/10 + 90

def create_population(region_list):
    for region in region_list:
        if region.type == 'Domestic':
            region.generate_region_population()
    
def normal_01(mean, std):
    
    result = np.random.normal(loc = mean, scale = std)
    if result < 0:
        result = 0
    if result > 1:
        result = 1
        
    return result