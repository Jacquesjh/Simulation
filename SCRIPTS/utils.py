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


def update_transportation(domestic_list):
    for domestic in domestic_list:
        domestic.update_transportation()
        
def update_restaurants(commercial_list):
    for commercial in commercial_list:
        commercial.update_restaurants()


def generate_commercial_buildings(commercial_list, number_commercial_regions, total_population):
    for region in commercial_list:
        region.generate_buildings(number_commercial_regions, total_population)

def create_jobs(population_list, commercial_list, industrial_list):
    index = 0
    
    for commercial in commercial_list:
        for company in commercial.companies:
            if index + company.num_workers < len(population_list):
                workers = population_list[index: index + company.num_workers]
                company.generate_jobs(workers)
                index += company.num_workers
            
    for industrial in industrial_list:
        for industry in industrial.industries:
            if index + company.num_workers < len(population_list):
                workers = population_list[index: index + industry.num_workers]
                industry.generate_jobs(workers)
                index += industry.num_workers


def create_population(region_list):
    for region in region_list:
        if region.type == 'Domestic':
            region.generate_region_population()
        

def create_regions(number_regions, scale, std):
    
    city_center         = [scale/2, scale/2]
    max_distance        = pow(scale, 1/2)
    region_centers      = np.random.normal(scale/2, std, (number_regions, 2))
    region_centers      = np.append(region_centers, [[999,999], [-999,999], [999,-999], [-999,-999]], axis = 0)
    region_areas, vor   = region_area(region_centers)
    regions             = []
    
    fix_vertices(vor)
    
    for i in range(len(region_centers) - 4):
        
        area = region_areas[i]
        x    = region_centers[i, 0]
        y    = region_centers[i, 1]
        distance_from_center = pow(pow(city_center[0] - x, 2) + 
                                   pow(city_center[1] - y, 2), 1/2)
        
        ## Weights of probabilities of each type o region
        commercial_weight = 0.6*pow(np.e, - pow(distance_from_center, 2)/(2*scale)) + 0.2
        
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
    
    for r in range(len(vor.point_region) - 4):
        region = vor.regions[vor.point_region[r]]
        
        if regions[r].type == 'Domestic':
            color = '#2CFC03'
            
        if regions[r].type == 'Commercial':
            color = '#03F4FC'
            
        if regions[r].type == 'Industrial':
            color = '#FCA503'
    
        if not -1 in region:
            polygon = [vor.vertices[i] for i in region]
            plt.fill(*zip(*polygon), color = color, alpha = 0.6)
            
    plt.xlim((0, 50))
    plt.ylim((0, 50))
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
            vertices[0] = 0
        else:
            if vertices[0] < -10:
                vertices[0] = 0
                
        if vertices[0] > 800:
            vertices[0] = 50
        else:
            if vertices[0] > 60:
                vertices[0] = 50
            
        if vertices[1] < -800:
            vertices[1] = 0
        else:
            if vertices[1] < 0:
                vertices[1] = 0
                
        if vertices[1] > 800:
            vertices[1] = 50
        else:            
            if vertices[1] > 60:
                vertices[1] = 50

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
                
def update_population(population_list, risk, hospital_list):
    for person in population_list:
        person.daily_update(risk, hospital_list)
        
def daily_routine(population_list, step):
    for person in population_list:
        person.interaction_routine(step)
        

def get_total_occupancy(commercial_list):
    occ = []
    for region in commercial_list:
        if len(region.hospitals) != 0:
            for hospital in region.hospitals:
                occ.append(hospital.get_occupancy)
                
    return occ

def get_average_occupancy(commercial_list):
    
    average_occupancy = 0
    num_hospitals     = 0
    for commercial in commercial_list:
        for hospital in commercial.hospitals:
            average_occupancy += hospital.get_occupancy()
            num_hospitals     += 1
            
    average_occupancy = average_occupancy/num_hospitals
    
    return average_occupancy

def get_average_protection(domestic_list):
    protection = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                protection.append(person.protection)

    return np.mean(protection)

def get_average_resistance(domestic_list):
    res = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                res.append(person.resistance)

    return np.mean(res)

def get_average_awareness(domestic_list):
    awareness = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                awareness.append(person.awareness)

    return np.mean(awareness)

def get_average_age(domestic_list):
    age = []
    for region in domestic_list:
        for person in region.get_region_population():
            if person.type != 'Dead':
                age.append(person.age)

    return np.mean(age)

def get_num_state_population(population_list, state):
    num = 0    
    for person in population_list:
        if person.type == state:
            num += 1
            
    return num

def get_state_population(domestic_list, state):
    pop = []
    for region in domestic_list:            
        for member in region.get_state_members():
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


def get_hospital_list(commercial_list):
    hospitals = []
    
    for commercial in commercial_list:
        for hospital in commercial.hospitals:
            hospitals.append(hospital)
            
    return hospitals


def update_color_and_occupancy(domestic_list, commercial_list, industrial_list):
    color_occupancy = []

    for domestic in domestic_list:
        for house in domestic.buildings:
            house.update_color()
            color     = house.color
            occupancy = 0
            
            for person in house.members:
                if person.type != 'Dead' and person.type != 'Pacient' and person.quarantine == True:
                    if person.workplace == 0 or person.workplace.remote == True:
                        occupancy += 1
                        
            color_occupancy.append([color, occupancy/house.num_members])
            
    for commercial in commercial_list:
        
        if commercial.num_hospitals != 0:
            for hospital in commercial.hospitals:
                hospital.update_color()
                color     = hospital.color
                occupancy = hospital.get_occupancy()
                
                color_occupancy.append([color, occupancy])
                
        for company in commercial.companies:
            company.update_color()
            color     = company.color
            occupancy = 0
            
            if company.remote == False:
                for worker in company.workers:
                    if worker.quarantine == False and worker.type != 'Dead' and worker.type != 'Pacient':
                        occupancy += 1
            color_occupancy.append([color, occupancy/company.num_workers])
                   
    for industrial in industrial_list:
        
        for industry in industrial.industries:
            industry.update_color()
            color     = industry.color
            occupancy = 0
            
            if industry.remote == False:
                for worker in industry.workers:
                    if worker.quarantine == False and worker.type != 'Dead' and worker.type != 'Pacient':
                        occupancy += 1
                        
            color_occupancy.append([color, occupancy/industry.num_workers])
            
    return color_occupancy
    
def get_buildings_xy(domestic_list, commercial_list, industrial_list):

    buildings_xy = []
    
    for domestic in domestic_list:
        buildings_xy += domestic.buildings_xy
        
    for commercial in commercial_list:
        buildings_xy += commercial.buildings_xy
    
    for industrial in industrial_list:
        buildings_xy += industrial.industries_xy
    
    buildings_location = np.zeros(shape = (len(buildings_xy), 2))
    
    for i in range(len(buildings_xy)):
        buildings_location[i, 0] = buildings_xy[i][0]
        buildings_location[i, 1] = buildings_xy[i][1]
        
    return buildings_location


