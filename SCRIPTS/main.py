# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:02:02 2021

@author: João Pedro Jacques Hoss
"""
import sys
sys.path.append('C:/Users/Joao/Simulation')
from utils import *
import time



if __name__ == '__main__':
    
    # Parameters
    number_regions = 35
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
    num_pacients      = get_num_state_population(domestic_list, 'Pacient')
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
    daily_cases              = []
    daily_deaths             = []
    daily_occupancy          = []
    daily_susceptible        = []
    daily_infected           = []
    daily_immune             = []
    daily_pacients           = []
    daily_dead               = []
    daily_average_fanciness  = []
    daily_average_resistance = []
    daily_averega_age        = []
    
    
    daily_risk               = []
    
    ## ---------------------- STARTING CONDITIONS ----------------------
    
    daily_cases.append(0)
    daily_deaths.append(0)
    daily_occupancy.append(get_average_occupancy(commercial_list))
    daily_susceptible.append(num_susceptible)
    daily_infected.append(num_infected)
    daily_immune.append(num_immune)
    daily_pacients.append(num_pacients)
    daily_dead.append(num_dead)
    daily_average_fanciness.append(get_average_fanciness(domestic_list))
    daily_average_resistance.append(get_average_resistance(domestic_list))
    daily_averega_age.append(get_average_age(domestic_list))
    
    
    daily_risk.append(0)
    
    HOSPITAL_LIST = get_hospital_list(commercial_list)
    
    DAYS  = 365
    steps = 7
    
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
    '''
        To create the Pacient - ZERO
    '''
    
    pacient_zero                    = random.choice(population_list)
    pacient_zero.type               = 'Infected'
    pacient_zero.days_till_symptoms = 4
    
    
    
    for day in range(DAYS):

        print('Starting the day!')        
        update_population(population_list, daily_risk[-1], HOSPITAL_LIST)
        update_transportation(domestic_list)
        update_restaurants(commercial_list)
        
        for stage in range(steps):
            
            start = time.time()
            daily_routine(population_list, stage)
            print('Stage ' + str(stage) + ' Done!!')
            print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
            
        ## ---------------------- End of day conditions ----------------------
        
        new_susceptible    = get_num_state_population(domestic_list, 'Susceptible')
        new_infected       = get_num_state_population(domestic_list, 'Infected')
        new_immune         = get_num_state_population(domestic_list, 'Immune')
        new_pacient        = get_num_state_population(domestic_list, 'Pacient')
        new_dead           = get_num_state_population(domestic_list, 'Dead')
        
        hospital_occupancy = get_average_occupancy(commercial_list)
        total_population   = get_num_total_population(domestic_list)
        
        new_cases          = new_infected - daily_infected[-1]
        new_deaths         = new_dead - daily_dead[-1]
        
        risk               = (pow(new_cases, 5/4) + pow(new_deaths, 13/8))*((hospital_occupancy/total_population))
        
        daily_cases.append(new_cases)
        daily_deaths.append(new_deaths)
        daily_occupancy.append(get_average_occupancy(commercial_list))
        daily_susceptible.append(new_susceptible)
        daily_infected.append(new_infected)
        daily_immune.append(new_immune)
        daily_pacients.append(new_pacient)
        daily_dead.append(new_dead)
        daily_average_fanciness.append(get_average_fanciness(domestic_list))
        daily_average_resistance.append(get_average_resistance(domestic_list))
        daily_averega_age.append(get_average_age(domestic_list))
            
        daily_risk.append(risk)
        
        break