# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:18:17 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
import random
from population import Person, normal


class Company:
    
    def __init__(self, color, region):
        self.type         = 'Company'
        self.color        = color
        self.num_workers  = int(np.random.normal(loc   = 40,
                                                 scale = 10))
        if self.num_workers < 10:
            self.num_workers = 10
    
        self.workers      = []
        self.home_office  = normal(mean = 0.6, std = 0.23)
        self.interactions = []
        self.remote       = False
        self.region       = region
    
    def update_color(self):
        if self.get_num_state_workers('Infected') > int(self.num_workers/2):
            self.color = '#FC0304'
        if self.get_num_state_workers('Dead') > int(0.9*self.num_workers):
            self.color = '#003638'
        
    def work_from_home(self, risk):
        self.remote = random.choices([False, True],
                                     weights = (1 - (self.home_office + risk)/2, (self.home_office + risk)/2))[0]
        
    def generate_jobs(self, population_list):
        
        if len(population_list) != 0:
            
            for worker in population_list:
                self.workers.append(worker)
                worker.update_workplace(self)
                
            if len(self.workers) != 1:
                self.generate_interactions()
    
    def generate_interactions(self):
        
        if len(self.workers) != 1:
            
            for worker in self.workers:
                num_coworkers = int(np.random.normal(loc   = 6,
                                                     scale = 2))
                if num_coworkers < 3:
                    num_coworkers = 3
                        
                coworkers = []
                possible_coworkers = self.workers.copy()
                possible_coworkers.remove(worker)
                
                for i in range(num_coworkers):
                    coworker = random.choice(possible_coworkers)
                    coworkers.append(coworker)
                    possible_coworkers.remove(coworker)
                    
                pass_list = {'Worker': worker,
                             'Coworkers': coworkers}
                
                self.interactions.append(pass_list)
                
    def get_num_state_workers(self, state):
        num = 0
        for worker in self.workers:
            if worker.type == state:
                num += 1
                
        return num
                
    def get_state_worker(self, state):
        list_workers = []
        for worker in self.workers:
            if worker.type == state:
                list_workers.append(worker)
                
        return list_workers
    
    def get_coworkers(self, worker):
        coworkers = []
        for interaction in self.interactions:
            if interaction['Worker'] == worker:
                coworkers = interaction['Coworkers']
                break
            
        return coworkers
        
    
class Restaurant:
    
    def __init__(self, color):
        self.type         = 'Restaurant'
        self.color        = color
        self.num_clients  = int(np.random.normal(loc   = 40,
                                                 scale = 10))
        self.clients      = []
        self.interactions = []
    
    
class Hospital:
    
    def __init__(self, color, region):
        self.type     = 'Hospital'
        self.color    = '#1F02FA'
        self.num_beds = 0
        self.pacients = []
        self.region   = region
        
    def update_color(self):
        if self.get_occupancy() > 0.9:
            self.color = '#4A0057'
        else:
            if self.get_occupancy() > 0.7:
                self.color = '#200066'
        
    def generate_beds(self, num_commercial_regions, total_population):
        self.num_beds = int(np.random.normal(loc   = 3*total_population/(10000*num_commercial_regions),
                                             scale = 0.23*3*total_population/(10000*num_commercial_regions)))
        if self.num_beds < 3:
            self.num_beds = 3
        
    def get_num_pacients(self):
        return len(self.pacients)
    
    def get_pacients(self):
        return self.pacients
    
    def add_pacient(self, pacient):
        self.pacients.append(pacient)
        
    def get_occupancy(self):
        return len(self.pacients)/self.num_beds
        
    
class CommercialRegion:
    
    def __init__(self, distance, area, x, y, scale):
        self.type             = 'Commercial'
        self.color            = '#03F4FC'
        self.distance         = distance        
        
        if area > pow(np.pi*pow(scale, 1/2), 2):
            self.area         = pow(np.pi*pow(scale, 1/2), 2)/2            
        else:
            self.area         = area
            
        self.x                = x
        self.y                = y
        self.scale            = scale
        self.num_companies    = 0
        self.num_restaurants  = 0
        self.num_hospitals    = random.choice((0, 1, 2))
        self.hospitals        = []
        self.rest_clients     = 0
        self.infected_clients = 0
        
        self.buildings_xy    = []
        self.radius          = pow(area/np.pi, 1/2)
        
        if self.num_hospitals != 0:
            for i in range(self.num_hospitals):
                self.hospitals.append(Hospital(self.color, region = self))
                radius = self.radius*np.random.random()
                angle  = 2*np.pi*np.random.random()
                x      = self.x + radius*np.cos(angle)
                y      = self.y + radius*np.sin(angle)
                self.buildings_xy.append([x, y])
                
        self.companies       = []
        self.restaurants     = []
    '''
    def get_buildings_location(self):
        data = []
        
        if self.num_hospitals != 0:
            for i in range(self.num_hospitals):
                temp = {'Type': self.hospitals[i].type, 'x': self.buildings_xy[i][0], 'y': self.buildings_xy[i][0]}
                data.append(temp)    
        for j in range(self.num_hospitals, len(self.buildings_xy)):
            temp = {'Type': 'Company', 'x': self.buildings_xy[j][0], 'y': self.buildings_xy[j][1]}
            data.append(temp)
            
        return data
    '''
    
    def update_restaurants(self):
        possible_clients = (self.get_state_population('Susceptible')
                            + self.get_state_population('Infected')
                            + self.get_state_population('Immune'))
        
        for client in possible_clients:
            if client.lunch_routine == 'Restaurant' and client.workplace.remote == False and client.quarantine == False:
                self.rest_clients += 1
                
                if client.type == 'Infected' and client.days_till_symptoms < 3:
                    self.infected_clients += 1
        
        
    def generate_buildings(self, num_commercial_regions, total_population):
            
        self.num_companies = int(np.random.normal(loc   = 50*(self.area/self.scale),
                                                  scale = 0.23*40*(self.area/self.scale)))
        if self.num_companies < 20:
            self.num_companies = 20
            
        for i in range(self.num_companies):
            self.companies.append(Company(self.color, region = self))
            radius = self.radius*np.random.random()
            angle  = 2*np.pi*np.random.random()
            x      = self.x + radius*np.cos(angle)
            y      = self.y + radius*np.sin(angle)
            self.buildings_xy.append([x, y])
            
            
        self.num_restaurants = int(np.random.normal(loc = 0.1*self.num_companies,
                                                    scale = 0.23*0.01*self.num_companies))
        for i in range(self.num_restaurants):
            self.restaurants.append(Restaurant(self.color))
            
        for hospital in self.hospitals:
            hospital.generate_beds(num_commercial_regions, total_population)
            
    def get_num_state_population(self, state):
        num = 0
        for company in self.companies:
            num += company.get_num_state_workers(state)
            
        return num
    
    def get_state_population(self, state):
        list_pop = []
        for company in self.companies:
            for worker in company.get_state_worker(state):
                list_pop.append(worker)
                
        return list_pop
    
    
class House:
    
    def __init__(self, color, wealth_base, domestic_region):
        self.type            = 'House'
        self.color           = color
        self.wealth          = wealth_base
        self.num_members     = int(np.random.normal(loc   = (5 + 1/pow(wealth_base, 1/2)),
                                                    scale = 1/pow(wealth_base, 1/2)))
        if self.num_members < 1:
            self.num_members = 1
        self.members         = []
        self.domestic_region = domestic_region
        
    def generate_house_members(self):
        self.members = []
        for i in range(self.num_members):
            self.members.append(Person(self.wealth, self))
        
    def get_all_members(self):
        return self.members
        
    def get_num_state_members(self, state):
        num_state = 0        
        for member in self.members:
            if member.type == state:
                num_state += 1
            
        return num_state
                           
    def get_state_members(self, state):
        list_members = []            
        for member in self.members:
            if member.type == state:
                list_members.append(member)
                
        return list_members
    
    def update_color(self):
        if self.get_num_state_members('Infected') > int(self.num_members/2):
            self.color = '#FC0303'
            
        if self.get_num_state_members('Dead') > int(0.9*self.num_members):
            self.color = '#000000'


class DomesticRegion:
    
    def __init__(self, distance, area, x, y, scale):
        self.type                = 'Domestic'
        self.color               = '#2CFC03'
        self.distance            = distance
        
        if area > pow(np.pi*pow(scale, 1/2), 2):
            self.area            = pow(np.pi*pow(scale, 1/2), 2)/2  
            
        else:
            self.area            = area
            
        self.x                   = x
        self.y                   = y
        self.wealth              = 0.8/(1 + distance*pow(np.e, - scale/area)) + 0.2
        self.num_buildings       = int(abs(np.random.normal(loc   = 1.5*distance*(pow(self.area/np.pi, 1/2)/self.wealth),
                                                            scale = distance*pow(scale, 1/2)/self.wealth)))
        self.buildings           = []
        self.buildings_xy        = []
        self.radius              = pow(area/np.pi, 1/2)
        
        for i in range(self.num_buildings):
            self.buildings.append(House(color = self.color, wealth_base = self.wealth, domestic_region = self))
            radius = self.radius*np.random.random()
            angle  = 2*np.pi*np.random.random()
            x      = self.x + radius*np.cos(angle)
            y      = self.y + radius*np.sin(angle)
            self.buildings_xy.append([x, y])
            
            
        self.num_passengers      = 0
        self.infected_passengers = 0
        
    def update_transportation(self):
        possible_passengers = (self.get_state_members('Susceptible')
                              + self.get_state_members('Infected')
                              + self.get_state_members('Immune'))
        
        for passenger in possible_passengers:
            if passenger.transportation == 'Public' and passenger.workplace != 0 and passenger.quarantine == False and passenger.workplace.remote == False:
                self.num_passengers += 1
                
                if passenger.type == 'Infected' and passenger.days_till_symptoms < 3:
                    self.infected_passengers += 1
        
    def get_buildings(self):
        return self.buildings
    
    def get_wealth(self):
        return self.wealth
    
    def get_xy(self):
        return self.x, self.y
    
    def get_area(self):
        return self.area
    
    def get_distance(self):
        return self.distance
    
    def get_state_members(self, state):
        list_members = []
        
        for building in self.buildings:
            for member in building.get_state_members(state):
                list_members.append(member)
                
        return list_members
    
    def get_region_population(self):
        region_population = []
        for house in self.buildings:
            for member in house.get_all_members():
                region_population.append(member)
                
        return region_population
    
    def get_num_region_population(self):
        num = 0
        for house in self.buildings:
            for member in house.get_all_members():
                num += 1
        return num
    
    def get_num_state_members(self, state):
        num_state = 0
        
        for building in self.buildings:
            num_state += building.get_num_state_members(state)
            
        return num_state
    
    def generate_region_population(self):
        for building in self.buildings:
            building.generate_house_members()
            
            
class Industry:
    
    def __init__(self, color, region):
        
        self.type         = 'Industry'
        self.color        = color
        self.num_workers  = int(np.random.normal(loc   = 1000,
                                                 scale = 0.23*1000))
        self.workers      = []        
        self.home_office  = normal(mean = 0.15, std = 0.1)
        self.interactions = []
        self.remote       = False
        self.region       = region
        
    def update_color(self):
        if self.get_num_state_workers('Infected') > int(self.num_workers/2):
            self.color = '#FC0302'
            
        if self.get_num_state_workers('Dead') > int(0.9*self.num_workers):
            self.color = '#382100'
            
    def work_from_home(self):
        self.remote = random.choices([False, True],
                                     weights = (1 - self.home_office, self.home_office))[0]
        
    def generate_jobs(self, population_list):
        
        if len(population_list) != 0:
            
            for worker in population_list:
                self.workers.append(worker)
                worker.update_workplace(self)
                
            self.generate_interactions()
    
    def generate_interactions(self):
        
        if len(self.workers) != 0:
            
            for worker in self.workers:
                num_coworkers = int(np.random.normal(loc   = 20,
                                                     scale = 4))
                if num_coworkers < 3:
                    num_coworkers = 3
                        
                coworkers = []
                possible_coworkers = self.workers.copy()
                possible_coworkers.remove(worker)
                    
                for i in range(num_coworkers):
                    coworker = random.choice(possible_coworkers)
                    coworkers.append(coworker)
                    possible_coworkers.remove(coworker)
                        
                pass_list = {'Worker': worker,
                             'Coworkers': coworkers}
                self.interactions.append(pass_list)
    
    def get_num_state_workers(self, state):
        num = 0
        for worker in self.workers:
            if worker.type == state:
                num += 1
                
        return num
    
    def get_state_worker(self, state):
        list_workers = []
        for worker in self.workers:
            if worker.type == state:
                list_workers.append(worker)
                
        return list_workers
    
    def get_coworkers(self, worker):
        coworkers = []
        for interaction in self.interactions:
            if interaction['Worker'] == worker:
                coworkers = interaction['Coworkers']
                break
            
        return coworkers

class IndustrialRegion:
    
    def __init__(self, distance, area, x, y, scale):        
        self.type           = 'Industrial'
        self.color          = '#FCA503'
        self.distance       = distance
        self.area           = area
        self.x              = x
        self.y              = y
        if area > pow(np.pi*pow(scale, 1/2), 2):
            self.area       = pow(np.pi*pow(scale, 1/2), 2)/2
        else:
            self.area       = area
        self.num_industries = int(np.random.normal(loc   = 6,
                                                   scale = 2))
        if self.num_industries < 3:
            self.num_industries = 3
            
        self.industries     = []
        self.industries_xy  = []
        self.radius         = pow(area/np.pi, 1/2)
        
        for i in range(self.num_industries):
            self.industries.append(Industry(self.color, region = self))
            radius = self.radius*np.random.random()
            angle  = 2*np.pi*np.random.random()
            x      = self.x + radius*np.cos(angle)
            y      = self.y + radius*np.sin(angle)
            self.industries_xy.append([x, y])
            
            
    def get_state_population(self, state):
        lis = []
        for industry in self.industries:
            for worker in industry.get_state_worker(state):
                lis.append(worker)
                
        return lis
    
    def get_num_state_population(self, state):
        num = 0
        for industry in self.industries:
            num += industry.get_num_state_workers(state)
            
        return num