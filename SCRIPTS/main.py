# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:02:02 2021

@author: João Pedro Jacques Hoss
"""
import sys
sys.path.append('C:/Users/Joao/Simulation')
from utils import *
import time
## ----------------------- GLOBAL VARIABLES -----------------------
'''
global daily_deaths
global daily_cases
global hospital_occupancy
global total_population
global risk

#risk               = (pow(daily_cases, 5/4) + pow(daily_deaths, 13/8))*((hospital_occupancy/total_population))
risk E [0, 1]
'''


if __name__ == '__main__':
    
    # Parameters
    number_regions = 15
    scale          = 100
    std            = 15
    
    print(' ---------- Creating the environment ---------- ')
    start                = time.time()
    region_list, voronoi = create_regions(number_regions, scale, std)
    map_regions(region_list, voronoi)
    print(' ---------- Environment created ---------- ')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    print(' ---------- Generating population ----------')
    start = time.time()
    create_population(region_list)
    print(' ---------- Population created ----------')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    print(' ---------- Gathering lists ----------')
    start             = time.time()
    domestic_list     = get_domestic_regions(region_list)
    commercial_list   = get_commercial_regions(region_list)
    industrial_list   = get_industrial_regions(region_list)
    
    num_susceptible   = get_num_state_population(domestic_list, 'Susceptible')
    num_infected      = get_num_state_population(domestic_list, 'Infected')
    num_immune        = get_num_state_population(domestic_list, 'Immune')
    num_pacient       = get_num_state_population(domestic_list, 'Pacient')
    num_dead          = get_num_state_population(domestic_list, 'Dead')
    total_population  = get_num_total_population(domestic_list)
    population_list   = get_population_list(domestic_list)
    
    num_houses        = get_num_houses(domestic_list)
    num_hospitals     = get_num_hospitals(commercial_list)
    num_industries    = get_num_industries(industrial_list)
    print(' ---------- Lists gathered ----------')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    print(' ---------- Generating commercial buildings ----------')
    start             = time.time()
    generate_commercial_buildings(commercial_list, len(commercial_list), total_population)
    available_jobs    = get_available_jobs(commercial_list, industrial_list)
    num_companies     = get_num_companies(commercial_list)
    num_restaurants   = get_num_restaurants(commercial_list)
    num_hospital_beds = get_num_hospital_beds(commercial_list)
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    print(' ---------- Generating jobs ----------')
    start = time.time()
    create_jobs(population_list, commercial_list, industrial_list)
    print(' ---------- Jobs created ----------')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    ## ---------------------- CONTROL VARIABLES ----------------------
    daily_cases        = []
    daily_deaths       = []
    daily_risk         = []
    daily_occupancy    = []
    list_susceptible   = []
    list_infected      = []
    list_immune        = []
    list_pacients      = []
    list_dead          = []
    average_fanciness  = []
    average_resistance = []
    averega_age        = []
    
    
    ## ---------------------- STARTING CONDITIONS ----------------------
    
    daily_cases.append(0)
    daily_deaths.append(0)
    daily_risk.append(0)
    daily_occupancy.append(get_average_occupancy(commercial_list))
    list_susceptible.append(num_susceptible)
    list_infected.append(num_infected)
    list_immune.append(num_immune)
    list_pacients.append(num_pacients)
    list_dead.append(num_dead)
    average_fanciness.append(get_average_fanciness(domestic_list))
    average_resistance.append(get_average_reistance(domestic_list))
    
    DAYS = 365
    step = 0
    risk = 0
    '''
        The steps are the stages of the day of a person
            0 - staying in house
            1 - going to work
            2 - at work
            3 - lunching
            4 - at work
            5 - coming back from work
            6 - staying in house
            *Repeat
    '''
    for day in range(DAYS):
        
        update_population(population_list, risk)
        
        for stage in range(steps):
            pass
            
        ## ---------------------- End of day conditions ----------------------
        
        daily_cases.append(0)
        daily_deaths.append(0)
        daily_risk.append(0)
        daily_occupancy.append(get_average_occupancy(commercial_list))
        list_susceptible.append(num_susceptible)
        list_infected.append(num_infected)
        list_immune.append(num_immune)
        list_pacients.append(num_pacients)
        list_dead.append(num_dead)
        average_fanciness.append(get_average_fanciness(domestic_list))
        average_resistance.append(get_average_reistance(domestic_list))
            