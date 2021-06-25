# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:02:02 2021

@author: João Pedro Jacques Hoss
"""


from utils import *
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pandas as pd
import pickle



if __name__ == '__main__':
    
    # Parameters
    number_regions = 25
    scale          = 50
    std            = 15
    
    print(' ---------- Creating the environment ---------- ')
    start                = time.time()
    region_list, voronoi = create_regions(number_regions, scale, std)
    map_regions(region_list, voronoi)
    print(' ---------- Environment created ---------- ')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    # %%
    
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
    population_list   = get_population_list(domestic_list)
    
    pacient_zero                    = random.choice(population_list)
    pacient_zero.type               = 'Infected'
    pacient_zero.days_till_symptoms = 4
    
    susceptible   = get_num_state_population(population_list, 'Susceptible')
    infected      = get_num_state_population(population_list, 'Infected')
    immune        = get_num_state_population(population_list, 'Immune')
    pacients      = get_num_state_population(population_list, 'Pacient')
    dead          = get_num_state_population(population_list, 'Dead')
    total_population  = get_num_total_population(domestic_list)
    
    num_houses        = get_num_houses(domestic_list)
    num_hospitals     = get_num_hospitals(commercial_list)
    num_industries    = get_num_industries(industrial_list)
    print(' ---------- Lists gathered ----------')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    # %%
    
    print(' ---------- Generating commercial buildings ----------')
    start             = time.time()
    generate_commercial_buildings(commercial_list, len(commercial_list), total_population)
    available_jobs    = get_available_jobs(commercial_list, industrial_list)
    num_companies     = get_num_companies(commercial_list)
    num_restaurants   = get_num_restaurants(commercial_list)
    num_hospital_beds = get_num_hospital_beds(commercial_list)
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    # %%
    
    print(' ---------- Generating jobs ----------')                                     ## If it gives error "Cannot choose from an empty sequence" just ty again
    start = time.time()                                                                 ## I have no more sanity left to fix it, but eventually it works 
    create_jobs(population_list, commercial_list, industrial_list)                      ## IT WILL WORK EVENTUALLY ! Sometimes it gives error 6 times before working
    print(' ---------- Jobs created ----------')
    print(' ---------- Execution time: {:.2f}s ----------\n\n'.format(time.time() - start))
    
    # %%
    
    ## ---------------------- CONTROL VARIABLES ----------------------
    
    color_occupancy = update_color_and_occupancy(domestic_list, commercial_list, industrial_list)
    
    new_cases                = []
    new_deaths               = []
    daily_occupancy          = []
    num_susceptible          = []
    num_infected             = []
    num_immune               = []
    num_pacients             = []
    num_dead                 = []
    daily_average_protection = []
    daily_average_resistance = []
    daily_average_awareness  = []
    daily_averega_age        = []
    daily_risk               = []
    daily_colors             = []
    ## ---------------------- STARTING CONDITIONS ----------------------
    
    daily_risk.append(0)
    new_cases.append(0)
    new_deaths.append(0)
    daily_occupancy.append(get_average_occupancy(commercial_list))
    num_susceptible.append(susceptible)
    num_infected.append(infected)
    num_immune.append(immune)
    num_pacients.append(pacients)
    num_dead.append(dead)
    daily_average_protection.append(get_average_protection(domestic_list))
    daily_average_resistance.append(get_average_resistance(domestic_list))
    daily_average_awareness.append(get_average_awareness(domestic_list))
    daily_averega_age.append(get_average_age(domestic_list))
    daily_colors.append(color_occupancy)
    HOSPITAL_LIST = get_hospital_list(commercial_list)
    
    DAYS  = 90
    steps = 7
        
    buildings_location = get_buildings_xy(domestic_list, commercial_list, industrial_list)
    
    # %%
    
    ## ------------------------- SIMULATION --------------------------------
    
    for day in range(600):

        print('\nDay: ' + str(day + 1) + '\n')
        update_population(population_list, daily_risk[-1], HOSPITAL_LIST)
        update_transportation(domestic_list)
        update_restaurants(commercial_list)
        
        color_occupancy = update_color_and_occupancy(domestic_list, commercial_list, industrial_list)
        
        for stage in range(steps):
            
            start = time.time()
            daily_routine(population_list, stage)
            print('Stage ' + str(stage) + ' Done!!')
            print(' ---------- Execution time: {:.2f}s ----------'.format(time.time() - start))
            
        ## ---------------------- End of day conditions ----------------------
        
        susceptible        = get_num_state_population(population_list, 'Susceptible')
        infected           = get_num_state_population(population_list, 'Infected')
        immune             = get_num_state_population(population_list, 'Immune')
        pacient            = get_num_state_population(population_list, 'Pacient')
        dead               = get_num_state_population(population_list, 'Dead')
        
        hospital_occupancy = get_average_occupancy(commercial_list)
        total_population   = get_num_total_population(domestic_list)
        
        today_cases        = abs(infected - num_infected[-1])
        today_deaths       = abs(dead - num_dead[-1])
        
        risk               = (pow(today_cases, 13/8) + pow(today_deaths, 13/8))*((hospital_occupancy/total_population))
        
        new_cases.append(today_cases)
        new_deaths.append(today_deaths)
        daily_occupancy.append(get_average_occupancy(commercial_list))
        num_susceptible.append(susceptible)
        num_infected.append(infected)
        num_immune.append(immune)
        num_pacients.append(pacient)
        num_dead.append(dead)
        daily_average_protection.append(get_average_protection(domestic_list))
        daily_average_resistance.append(get_average_resistance(domestic_list))
        daily_average_awareness.append(get_average_awareness(domestic_list))
        daily_averega_age.append(get_average_age(domestic_list))
            
        daily_risk.append(risk)        
        daily_colors.append(color_occupancy)
    
    # %%
    
    plt.style.use('dark_background')
    fig = plt.figure(figsize = (20, 20))
    ax  = fig.add_subplot(111, projection = '3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.get_zaxis().set_ticks([])
    ax.get_zaxis().line.set_linewidth(0)
    ax.grid(False) 
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    
    x      = buildings_location[:, 0]
    y      = buildings_location[:, 1]
    bottom = np.zeros(shape = x.shape)
    width  = 5
    top    = []
    colors = []
    
    for i in range(len(color_occupancy)):
        colors.append(color_occupancy[i][0])
        occupancy = color_occupancy[i][1]
        
        if color_occupancy[i][0] == '#03F4FC' or color_occupancy[i][0] == '#FC0304' or color_occupancy[i][0] == '#003638':
            top.append(0.6 + occupancy/5)
            
        if color_occupancy[i][0] == '#2CFC03' or color_occupancy[i][0] == '#FC0303' or color_occupancy[i][0] == '#000000':
            top.append(0.5 + occupancy/5)
            
        if color_occupancy[i][0] == '#FCA503' or color_occupancy[i][0] == '#FC0302' or color_occupancy[i][0] == '#382100':
            top.append(0.6 + occupancy/5)
            
        if color_occupancy[i][0] == '#1F02FA' or color_occupancy[i][0] == '#4A0057' or color_occupancy[i][0] == '#200066':
            top.append(0.8 + occupancy/5)
            
    ax.view_init(azim = 20, elev = 20)
    ax.axis('off')
    value = 400
    while value != -450:
        ax.plot([-400, 400], [value, value], 0, color = '#5C2C6D', zorder = 2)
        ax.plot([value, value], [-400, 400], 0, color = '#5C2C6D', zorder = 2)
        value -= 50
        
    ax.set_zlim((0, 7))
    ax.bar3d(x, y, bottom, width, width, top, shade = True, color = colors)
    
# %%

dataframe = pd.DataFrame(columns = ['Susceptible', 'Infected', 'Immune', 'Pacient', 'Dead',
                                    'Occupancy', 'Average Protection', 'Average Awareness',
                                    'Average Resistance', 'Risk'])
dataframe['Susceptible']        = num_susceptible    
dataframe['Infected']           = num_infected
dataframe['Immune']             = num_immune
dataframe['Pacient']            = num_pacients
dataframe['Dead']               = num_dead
dataframe['Occupancy']          = daily_occupancy
dataframe['Average Protection'] = daily_average_protection
dataframe['Average Resistance'] = daily_average_resistance
dataframe['Average Awareness']  = daily_average_awareness
dataframe['Risk']               = daily_risk
           
dataframe.to_csv('C:/Users/Joao/Simulation/EXPERIMENTS/Population_1/data_round_1.csv')
np.save('C:/Users/Joao/Simulation/EXPERIMENTS/Population_1/buildings_location.npy', buildings_location)

with open('C:/Users/Joao/Simulation/EXPERIMENTS/Population_1/colors_occupanies_round_1', 'wb') as file:
    pickle.dump(daily_colors, file)

# %%
import mplcyberpunk 
plt.figure(figsize = (20, 20))

plt.plot(num_susceptible, color = 'purple')
plt.plot(num_infected, color = 'blue')
mplcyberpunk.add_glow_effects()





res = []
for person in population_list:
    res.append(person.resistance)