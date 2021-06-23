# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 17:27:56 2021

@author: João Pedro Jacques Hoss
"""
import sys
sys.path.append('C:/Users/Joao/Simulation')
import numpy as np
from matplotlib import pyplot as plt
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull
import environment

def generate_commercial_buildings(commercial_list, number_commercial_regions, total_population):
    for region in commercial_list:
        region.generate_buildings(number_commercial_regions, total_population)

def create_jobs(population_list, commercial_list, industrial_list):
    index = 0
    
    for commercial in commercial_list:
        for company in commercial.companies:
            workers = population_list[index: index + company.num_workers]
            company.generate_jobs(workers)
            index += company.num_workers
            
    for industrial in industrial_list:
        for industry in industrial.industries:
            workers = population_list[index: index + industry.num_workers]
            industry.generate_jobs(workers)
            index += industry.num_workers


def create_population(region_list):
    for region in region_list:
        if region.type == 'Domestic':
            region.generate_region_population()
        

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
            region = environment.DomesticRegion(distance_from_center, area, x, y, scale)
            regions.append(region)
            
        if region_type == ['Commercial']:
            region = environment.CommercialRegion(distance_from_center, area, x, y, scale)
            regions.append(region)
            
        if region_type == ['Industrial']:
            region = environment.IndustrialRegion(distance_from_center, area, x, y, scale)
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
            plt.fill(*zip(*polygon), color = color, alpha = 0.6)
            
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

def get_available_jobs(commercial_list, industrial_list):
    
    jobs = 0
    for commercial in commercial_list:
        for company in commercial.companies:
            jobs += company.num_workers
            
    for industrial in industrial_list:
        for industry in industrial.industries:
            jobs += industry.num_workers
            
    return jobs


def get_num_total_population(region_list):
    num = 0
    for region in region_list:
        if region.type == 'Domestic':
            num += region.get_num_region_population()
            
    return num

def get_population_list(domestic_list):
    population_list = []
    for region in domestic_list:
        for building in region.buildings:
            for member in building.members:
                population_list.append(member)
                
    random.shuffle(population_list)
    return population_list

def get_num_houses(domestic_list):
    num = 0
    for region in domestic_list:
        num += region.num_buildings
        
    return num

def get_num_companies(commercial_list):
    num = 0
    for region in commercial_list:
        num += region.num_companies
        
    return num

def get_num_restaurants(commercial_list):
    num = 0
    for region in commercial_list:
        num += region.num_restaurants
        
    return num

def get_num_industries(industrial_list):
    num = 0
    for region in industrial_list:
        num += region.num_industries
        
    return num

def get_num_hospitals(commercial_list):
    num = 0
    for region in commercial_list:
        num += region.num_hospitals
        
    return num

def get_num_hospital_beds(commercial_list):
    num = 0
    for region in commercial_list:
        try:
            for hospital in region.hospitals:
                num += hospital.num_beds
        except:
            pass
        
    return num
                
def update_population(population_list, risk):
    for person in population_list:
        if person.type != 'Dead':
            person.daily_update(risk)
        
def get_total_occupancy(commercial_list):
    occ = []
    for region in commercial_list:
        if len(region.hospitals) != 0:
            for hospital in region.hospital:
                occ.append(hospital.get_occupancy)
                
    return occ

def get_average_occupancy(commercial_list):
    occ = get_total_occupancy(commercial_list)
    
    return np.mean(occ)

def get_average_fanciness(domestic_list):
    fancy = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                fancy.append(person.fanciness)

    return np.mean(fancy)

def get_average_resistance(domestic_list):
    res = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                res.append(person.resistance)

    return np.mean(res)

def get_average_age(domestic_list):
    age = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                age.append(person.age)

    return np.mean(age)

def get_num_state_population(domestic_list, state):
    num = 0    
    for region in domestic_list:
        num += region.get_num_state_members(state)
            
    return num

def get_state_population(domestic_list, state):
    pop = []
    for region in domestic_list:            
        for member in region.get_state_members:
            pop.append(member)
    return pop

def get_domestic_regions(region_list):
    domestics = []
    for region in region_list:
        if region.type == 'Domestic':
            domestics.append(region)
    return domestics

def get_commercial_regions(region_list):
    commercial = []
    for region in region_list:
        if region.type == 'Commercial':
            commercial.append(region)
    return commercial

def get_industrial_regions(region_list):
    industrial = []
    for region in region_list:
        if region.type == 'Industrial':
            industrial.append(region)
    return industrial
