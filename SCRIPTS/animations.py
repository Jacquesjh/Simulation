# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 14:11:30 2021

@author: Joao
"""
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
from mpl_toolkits.mplot3d import axes3d
from matplotlib.ticker import MaxNLocator
import os
import moviepy.video.io.ImageSequenceClip
import pickle


dataframe        = pd.read_csv('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/data_round_1.csv')
total_population = dataframe['Susceptible'][0] + dataframe['Infected'][0]

buildings_location = np.load('C:/Users/Joao/Simulation/EXPERIMENTS/Population_1/buildings_location.npy')
file = open('C:/Users/Joao/Simulation/EXPERIMENTS/Population_1/colors_occupanies_round_1', 'rb')
all_colors = pickle.load(file)

plt.style.use('dark_background')
font = 'Oswald'

# %%

## --------------------------- POPULATION GRAPHS ---------------------------

for i in range(2, len(dataframe)):
    
    fig = plt.figure(figsize = (20, 15))
    im  = fig.add_subplot(111)
    im.tick_params(axis = 'both', labelsize = 20)
    im.xaxis.set_major_locator(MaxNLocator(integer = True))
    plt.title('POPULATION', fontname = font, fontsize = 30)
    plt.xlabel('Days', fontname = font, fontsize = 20, labelpad = 10)
    plt.ylabel('%', fontname = font, fontsize = 20, labelpad = 10, rotation = 0)
    im.grid(False)  
    
    im.plot(dataframe['Susceptible'].iloc[: i]*100/total_population, color = '#54FF29', label = 'Susceptible')    
    im.plot(dataframe['Infected'].iloc[: i]*100/total_population, color = '#AD29FF', label = 'Infected')    
    im.plot(dataframe['Immune'].iloc[: i]*100/total_population, color = '#26FFD0', label = 'Immune')    
    im.plot(dataframe['Pacient'].iloc[: i]*100/total_population, color = '#FF661F', label = 'Pacient')    
    im.plot(dataframe['Dead'].iloc[: i]*100/total_population, color = '#FF1F44', label = 'Dead')
    
    plt.legend(fontsize = 'xx-large')
    plt.ylim((0, 105))
    if i == 1:
        plt.xlim((0, len(dataframe['Susceptible'].iloc[: i])))
    else:        
        plt.xlim((0, len(dataframe['Susceptible'].iloc[: i - 1])))
    mplcyberpunk.add_glow_effects(im)
    
    save_name = 0
    if i < 10:
        save_name = '00' + str(i)
    else:
        if i < 100:
            save_name = '0' + str(i)
        else:
            save_name = str(i)
    plt.savefig('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/population/pop_' + save_name+ '.png')
    plt.close()
    
image_folder = 'C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/population/'
fps = 20

image_files = [image_folder + '/' + img for img in os.listdir(image_folder) if img.endswith('.png')]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps = fps)
clip.write_videofile('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/population/population_evolution.mp4')  

# %%

## --------------------------- STATUS GRAPHS ---------------------------

for i in range(2, len(dataframe)):

    fig = plt.figure(figsize = (20, 15))
    im  = fig.add_subplot(111)
    im.tick_params(axis = 'both', labelsize = 20)
    im.xaxis.set_major_locator(MaxNLocator(integer = True))
    plt.title('STATUS', fontname = font, fontsize = 30)
    plt.xlabel('Days', fontname = font, fontsize = 20, labelpad = 10)
    plt.ylabel('%', fontname = font, fontsize = 20, labelpad = 10, rotation = 0)
    im.grid(False)  
    
    im.plot(dataframe['Occupancy'].iloc[: i]*100, color = '#FF901F', label = 'Occupancy')    
    im.plot(dataframe['Average Resistance'].iloc[: i]*100, color = '#5C2C6D', label = 'Average Resistance')    
    im.plot(dataframe['Risk'].iloc[: i]*100, color = '#5DA4A6', label = 'Risk')
    
    plt.legend(fontsize = 'xx-large')
    plt.ylim((0, 105))
    if i == 1:
        plt.xlim((0, len(dataframe['Susceptible'].iloc[: i])))
    else:        
        plt.xlim((0, len(dataframe['Susceptible'].iloc[: i - 1])))
    mplcyberpunk.add_glow_effects(im)
    
    save_name = 0
    if i < 10:
        save_name = '00' + str(i)
    else:
        if i < 100:
            save_name = '0' + str(i)
        else:
            save_name = str(i)
            
    plt.savefig('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/status/status_' + save_name+ '.png')
    plt.close()
    
    
image_folder = 'C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/status/'
fps = 20

image_files = [image_folder + '/' + img for img in os.listdir(image_folder) if img.endswith('.png')]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps = fps)
clip.write_videofile('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/status/status_evolution.mp4')

# %%

## --------------------------- STATUS GRAPHS ---------------------------
'''
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

azimute = 0
i = 0
'''

azimute = 0
j       = 0

for color_occupancy in all_colors:
     
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
                
    ax.view_init(azim = azimute, elev = 20)
    
    azimute += 360*1/len(all_colors)
    ax.axis('off')
    value = 400
    
    while value != -450:
        ax.plot([-400, 400], [value, value], 0, color = '#5C2C6D', zorder = 2)
        ax.plot([value, value], [-400, 400], 0, color = '#5C2C6D', zorder = 2)
        value -= 50
        
    save_name = 0
    
    if j < 10:
        save_name = '00' + str(j)
    else:
        if j < 100:
            save_name = '0' + str(j)
        else:
            save_name = str(j)
    j += 1
    
    ax.set_zlim((0, 7))
    ax.bar3d(x, y, bottom, width, width, top, shade = True, color = colors)
    plt.savefig('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/3D/city_' + save_name + '.png')
    plt.close()
    

image_folder = 'C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/3D/'
fps = 10

image_files = [image_folder + '/' + img for img in os.listdir(image_folder) if img.endswith('.png')]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps = fps)
clip.write_videofile('C:/Users/Joao/Simulation/EXPERIMENTS/POPULATION_1/round_1/3D/city_evolution.mp4')