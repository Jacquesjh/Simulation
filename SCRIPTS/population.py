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
        
        self.type               = 'Susceptible'
        self.awareness          = normal(0.5, 0.3)
        self.resistance         = normal(0.5, 0.23)
        self.fanciness          = normal(wealth_base, 0.23)
        self.influence          = normal(0.5, 0.23)
        self.age                = int(np.random.normal(loc = 35, scale = 15))
        if self.age < 18:
            self.age = 18
        
        self.health             = (random.choices(['Healthy', 'Unhealthy'],
                                                 weights = (1 - (0.5 + (self.age - 35)/abs(self.age + 35)),
                                                            0.5 + (self.age - 35)/abs(self.age + 35))))[0]
        if self.health == 'Unhealthy':
            self.disease_intensity = normal(0.5 + (self.age - 35)/(self.age + 35), 0.23)
        else:
            self.disease_intensity = 0
            
        self.transportation     = (random.choices(['Public', 'Private'],
                                                  weights = (1 - normal((0.5 + self.fanciness)/2, 0.23),
                                                             normal((0.5 + self.fanciness)/2, 0.23))))[0]
        self.lunch_routine      = (random.choices(['Alone', 'Restaurant'],
                                                  weights = (1 - normal((0.5 + self.fanciness)/2, 0.23),
                                                             normal((0.5 + self.fanciness)/2, 0.23))))[0]
        self.house              = house
        self.workplace          = 0
        self.contagius          = 0
        self.protection         = 1 - pow(self.resistance, 3/2)
        self.symptoms_type      = 0
        self.days_till_symptoms = 0
        self.days_left_infected = 0
        self.days_left_hospital = 0
        self.days_left_immunity = 0
        self.death_probability  = 0
        self.hospital           = 0
        self.quarantine         = False
        self.daily_death_prob   = 0
        
        
        
    def update_workplace(self, workplace):
        self.workplace = workplace
   
    def daily_update(self, new_risk, hospital_list):                                   ## Updates at the start of each day
    
        if self.type != 'Dead':
            
            ## Updates the resistance and protection depending on the daily risk
            
            self.resistance = self.resistance - self.awareness*pow(new_risk, 3/2)      ## Updates depending on the risk of the situation
            
            if self.resistance < 0:
                self.resistance = 0
                
            self.resistance = self.resistance*(1 + pow(self.resistance, 3/2))          ## Updates through time
            
            if new_risk > 0.5:                                                         ## Chance of the Susceptible quarantine out of will 
                self.quarantine = random.choices([False, True],
                                                 weights = (self.resistance, 1 - self.resistance))[0]
            
            if self.resistance > 1:                
                self.resistance = 1
                
            if self.type != 'Immune':                                                  ## An Immune agent has self.protection = 1 always              
                self.protection = 1 - pow(self.resistance, 3/2)
                
            if self.type == 'Infected':
                self.contagius  = normal(pow(self.protection, 1/self.symptoms_type),
                                         0.23*pow(self.protection, 1/self.symptoms_type))
                self.quarantine = random.choices([False, True],
                                                 weights = (self.resistance, 1 - self.resistance))[0]
                
            ## ----------------------------------------------------------------    
            ##
            ## Checks if is time for the Infected to show symptoms, and if so, how the symptom affect the agent
            
            if self.type == 'Infected':
                if self.days_till_symptoms > 0:
                    self.days_till_symptoms -= 1
                else:
                    if self.days_left_infected == 0:
                        
                        if self.disease_intensity == 1:                                ## So that it doesn't divides by 0 when /(1 - self.dis)
                            self.disease_intensity = 0.95
                            
                        type_3 = normal(0.05*self.age/(pow((1 - self.disease_intensity), 1/2)*35),
                                        0.05/pow(1 - self.disease_intensity, 1/2))
                        if type_3 < 1:
                            type_2 = normal(0.3*self.age/(pow((1 - self.disease_intensity),
                                                              1/2)*35), 0.23*0.3/pow(1 - self.disease_intensity, 1/2))
                        if (type_2 + type_3) > 1:
                            type_2 = 1 - type_3
                            
                        type_1 = 1 - type_2 - type_3
                        
                        self.symptoms_type = random.choices([1, 2, 3],
                                                            weights = (type_1, type_2, type_3))[0]
                        
                        if self.symptoms_type == 3:
                            for hospital in hospital_list:                             ## Try to send infected to hospital
                            
                                if hospital.get_num_pacients() < hospital.num_beds:
                                    hospital.add_pacient(self)
                                    self.hospital           = hospital
                                    self.type               = 'Pacient'
                                    self.death_probability  = normal(0.5 + (self.disease_intensity/self.age),
                                                                     self.disease_intensity/self.age)
                                    self.days_left_hospital = int(np.random.normal(loc   = 21,
                                                                                   scale = 7))
                                    self.daily_death_prob   = (self.death_probability*self.days_left_hospital)/pow(21, 3/2)
                            
                            if self.hospital == 0:                                     ## Checks if went to hospital
                                self.death_probability  = 1
                                self.days_left_infected = int(np.random.normal(loc   = 14,
                                                                               scale = 3.5))
                                
                        else:
                            self.days_left_infected = int(np.random.normal(loc   = 14,
                                                                           scale = 3.5))
                            self.contagius          = normal(pow(self.protection, 1/self.symptoms_type),
                                                             0.23*pow(self.protection, 1/self.symptoms_type))
                            
            ## ----------------------------------------------------------------
            ##
            ## Checks if and Infected's infection time is over
            
            if  self.type == 'Infected':
                if self.days_left_infected > 0:
                    self.days_left_infected -= 1
                        
                else:
                    self.type               = 'Immune'
                    self.days_left_immunity = int(np.random.normal(loc   = 180,
                                                                   scale = 32))
                    self.contagius          = 0
                    self.death_probability  = 0
                    self.awareness          = pow(self.awareness, self.symptoms_type/(3 - self.symptoms_type))
                    self.resistance         = pow(self.resistance, self.symptoms_type/(3 - self.symptoms_type))
                    
            ## ----------------------------------------------------------------
            ##
            ## Checks the situation if the agent is in hospital
            
            if self.type == 'Pacient':
                if self.days_left_hospital > 0:
                    self.days_left_hospital -= 1
                    
                else:                                                                     ## Mean the Pacient survived  
                    self.type               = 'Immune'
                    self.days_left_immunity = int(np.random.normal(loc   = 180,
                                                                   scale = 32))
                    self.contagius          = 0
                    self.death_probability  = 0
                    self.health             = 'Unhealty'
                    self.disease_intensity  = normal(0.5, 0.2)                            ## Represents the sequelaa of the pacient
                    self.awareness          = pow(self.awareness, self.symptoms_type/(3 - self.symptoms_type))
                    self.resistance         = pow(self.resistance, self.symptoms_type/(3 - self.symptoms_type))
                    self.hospital.pacients.remove(self)
                    self.hospital           = 0
                    
            ## ----------------------------------------------------------------
            ##
            ## Checks if the immunity of the Immune agent has passed    
            
            if self.type == 'Immune':
                if self.days_left_immunity > 0:
                    self.days_left_immunity -= 1
                    
                else:
                    self.type = 'Susceptible'
                    
            ## ----------------------------------------------------------------
                    
    def interaction_routine(self, step):
        
        if step == 0:                                                           ## At home
            if self.type == 'Susceptible' or self.type == 'Immune' or self.type == 'Infected':
                self.routine_at_home()
                
            if self.type == 'Pacient':
                self.pacient_routine()
                
            if self.type == 'Dead':
                pass
                
        if step == 1:                                                           ## Going to work
            if self.type == 'Susceptible' or self.type == 'Immune':
                if self.workplace != 0:
                    if self.workplace.remote == False:
                        self.routine_transportation()
                    
                    else:
                        self.routine_at_home()
                        
                else:
                    self.routine_at_home()
                        
            if self.type == 'Infected':                
                if self.workplace != 0:
                    if self.workplace.remote == False:                        
                        if self.quarantine == False:                            
                            self.routine_transportation()
                            
                        else:
                            self.routine_at_home()
                    
                    else:
                        self.routine_at_home()
                
                else:
                    self.routine_at_home()
                    
            if self.type == 'Pacient':
                self.pacient_routine()
            
            if self.type == 'Dead':
                pass
            
        if step == 2:                                                           ## At work
            if self.type == 'Susceptible' or self.type == 'Immune':
                if self.workplace != 0:                                    ## If the agent has a job
                    if self.workplace.remote == False:                          ## If the the workplace does not support remote working
                        self.routine_working()
                
                    else:
                        self.routine_at_home()
                        
                else:
                    self.routine_at_home()
                    
            if self.type == 'Infected':
                if self.workplace != 0:
                    if self.workplace.remote == False:
                        
                        if self.quarantine == False:
                            self.routine_working()
                        
                        else:
                            self.routine_at_home()
                            
                    else:
                        self.routine_at_home()
                        
                else:
                    self.routine_at_home()
                        
            if self.type == 'Pacient':
                self.pacient_routine()
            
            if self.type == 'Dead':
                pass
            
        if step == 3:                                                           ## Lunch time
            if self.type == 'Susceptible' or self.type == 'Immune':
                if self.quarantine == False:
                    if self.workplace.region == 'Commercial':
                        self.routine_lunching()
                    else:
                        self.routine_working()
                else:
                    self.routine_at_home()
            
            if self.type == 'Infected':
                if self.quarantine == False:                    
                    self.routine_lunching()
                
                else:
                    self.routine_at_home()
                        
            if self.type == 'Pacient':
                self.pacient_routine()
            
            if self.type == 'Dead':
                pass
            
        if step == 4:                                                           ## At work
            if self.type == 'Susceptible' or self.type == 'Immune':
                if self.workplace != 0:                                    ## If the agent has a job
                    if self.workplace.remote == False:                          ## If the the workplace does not support remote working
                        self.routine_working()
                
                    else:
                        self.routine_at_home()
                        
                else:
                    self.routine_at_home()
                    
            if self.type == 'Infected':
                if self.workplace != 0:
                    if self.workplace.remote == False:
                        
                        if self.quarantine == False:
                            self.routine_working()
                        
                        else:
                            self.routine_at_home()
                            
                    else:
                        self.routine_at_home()
                        
                else:
                    self.routine_at_home()
                        
            if self.type == 'Pacient':
                self.pacient_routine()
            
            if self.type == 'Dead':
                pass
            
        if step == 1:                                                           ## Going to work
            if self.type == 'Susceptible' or self.type == 'Immune':
                if self.workplace != 0:
                    if self.workplace.remote == False:
                        self.routine_transportation()
                    
                    else:
                        self.routine_at_home()
                        
                else:
                    self.routine_at_home()
                        
            if self.type == 'Infected':
                if self.workplace != 0:
                    if self.workplace.remote == False:
                        
                        if self.quarantine == False:
                            self.routine_transportation()
                        else:
                            self.routine_at_home()
                    
                    else:
                        self.routine_at_home()
                
                else:
                    self.routine_at_home()
                    
            if self.type == 'Pacient':
                self.pacient_routine()
            
            if self.type == 'Dead':
                pass
            
        if step == 6:                                                           ## At home
            if self.type == 'Susceptible' or self.type == 'Immune' or self.type == 'Infected':
                self.routine_at_home()
                
            if self.type == 'Pacient':
                self.pacient_routine()
                
            if self.type == 'Dead':
                pass
                
            
    def routine_at_home(self):
        
        ## ------------------------ Infection Gamble --------------------------
        
        infected_members = self.house.get_state_members('Infected')
        
        if self.type != 'Immune' :
            if len(infected_members) != 0:
                contagius_total = 0
                
                for member in infected_members:
                    contagius_total += member.contagius
                
                average_contagius     = contagius_total/len(infected_members)
                contagius_factor      = pow(average_contagius, 1/len(infected_members))
                contagius_probability = (1 - self.protection)*contagius_factor
                result_infection      = (random.choices(['Not Infected', 'Infected'],
                                                        weights = (1 - contagius_probability, contagius_probability)))[0]
                
                if result_infection == 'Infected':
                    self.type               = 'Infected'
                    self.days_till_symptoms = int(np.random.normal(loc   = 5,
                                                                   scale = 1))
                    if self.days_till_symptoms < 0:
                        self.days_till_symptoms = 2
                        
        ## -------------------------------------------------------------------
        ##        
        ## ------------------------ Influence Gamble -------------------------
        
        members            = self.house.get_all_members()
        average_influence  = 0
        average_resistance = 0
        alive_members      = 0
        
        for member in members:
            if member.type != 'Dead' and member.type != 'Pacient':
                average_influence  += member.influence
                average_resistance += member.resistance
                alive_members      += 1
                
        average_influence  = average_influence/alive_members
        average_resistance = average_resistance/alive_members
        
        if self.resistance > average_resistance:
            self.resistance = self.resistance + average_resistance*(self.influence - average_influence)*0.1
            
        else:
            self.resistance = self.resistance + average_resistance*(average_influence - self.influence)*0.1
            
        ## -------------------------------------------------------------------
        
    def routine_transportation(self):
        
        ## ------------------------ Infection Gamble --------------------------
        
        if self.transportation == 'Public' and self.type != 'Immune':
            
            domestic_region         = self.house.domestic_region
            num_possible_passengers = domestic_region.num_passengers
            num_infected_passengers = domestic_region.infected_passengers
            
            contagius_factor      = num_infected_passengers/num_possible_passengers
            contagius_probability = (1 - self.protection)*contagius_factor
            result_infection      = random.choices(['Not Infected', 'Infected'],
                                                   weights = (1 - contagius_probability, contagius_probability))[0]
                
            if result_infection == 'Infected':
                self.type               = 'Infected'
                self.days_till_symptoms = int(np.random.normal(loc   = 5,
                                                               scale = 1))
                if self.days_till_symptoms < 0:
                    self.days_till_symptoms = 2
                 
        ## -------------------------------------------------------------------
                
    def routine_working(self):
        
        ## ------------------------ Infection Gamble -------------------------
        
        coworkers          = self.workplace.get_coworkers(self)
        infected_coworkers = []
        contagius_total    = 0
        
        if self.type != 'Immune':
            for coworker in coworkers:
                if coworker.type == 'Infected':
                    infected_coworkers.append(coworker)
                    contagius_total += coworker.contagius
                    
            if len(infected_coworkers) != 0:
                
                average_contagius     = contagius_total/len(infected_coworkers)
                contagius_factor      = pow(average_contagius, 1/len(infected_coworkers))
                contagius_probability = (1 - self.protection)*contagius_factor
                result_infection      = (random.choices(['Not Infected', 'Infected'],
                                                        weights = (1 - contagius_probability,
                                                                   contagius_probability)))[0]
                
                if result_infection == 'Infected':
                    self.type               = 'Infected'
                    self.days_till_symptoms = int(np.random.normal(loc   = 5,
                                                                   scale = 1))
                    if self.days_till_symptoms < 0:
                        self.days_till_symptoms = 2
        
        ## -------------------------------------------------------------------
        ##
        ## ------------------------ Influence Gamble -------------------------
        
        average_influence  = 0
        average_resistance = 0
        alive_coworkers    = 0
        
        for coworker in coworkers:
            if coworker.type != 'Dead' and coworker.type != 'Pacient':
                average_influence  += coworker.influence
                average_resistance += coworker.resistance
                alive_coworkers    += 1
                
        average_influence  = average_influence/alive_coworkers
        average_resistance = average_resistance/alive_coworkers
        
        if self.resistance > average_resistance:
            self.resistance = self.resistance + average_resistance*(self.influence - average_influence)*0.1
            
        else:
            self.resistance = self.resistance + average_resistance*(average_influence - self.influence)*0.1
        
        ## -------------------------------------------------------------------
        
    def routine_lunching(self):
        
        ## ------------------------ Influence Gamble -------------------------
        
        if self.workplace.region == 'Commercial':
            if self.lunch_routine == 'Restaurant' and self.type != 'Immune':
                
                region                      = self.workplace.region
                num_clients_region          = 0
                num_infected_clients_region = 0
                num_restaurants             = region.num_restaurants
                possible_clients            = (region.get_state_population('Susceptible')
                                               + region.get_state_population('Infected') 
                                               + region.get_state_population('Immune'))
                for worker in possible_clients:
                    if worker.quarantine != True and worker.workplace.remote != True and worker.lunch_routine == 'Restaurant':
                        num_clients_region += 1
                        
                        if worker.type == 'Infected':
                            num_infected_clients_region += 1
                
                contagius_factor      = (num_infected_clients_region/num_clients_region)/num_restaurants
                contagius_probability = (1 - self.protection)*contagius_factor
                result_infection      = random.choices(['Not Infected', 'Infected'],
                                                       weights = (1 - contagius_probability, contagius_probability))[0]
                    
                if result_infection == 'Infected':
                    self.type               = 'Infected'
                    self.days_till_symptoms = int(np.random.normal(loc   = 5,
                                                                   scale = 1))
                    if self.days_till_symptoms < 0:
                        self.days_till_symptoms = 2
                        
        else:
            if self.type != 'Immune':                                           ## Means that the agent work in the industry... lunching on site
                self.routine_working()                                          ## Same routine as working
                
    def pacient_routine(self):
        result = random.choices(['Alive', 'Dead'],
                                weights = (1 - self.daily_death_prob/6, self.daily_death_prob/6))[0]
        
        if result == 'Dead':
            self.type = 'Dead'
            self.hospital.pacients.remove(self)
        
        
        