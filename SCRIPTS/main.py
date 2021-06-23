# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:02:02 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
from environment import *
import matplotlib.pyplot as plt
from utils import *


## ----------------------- GLOBAL VARIABLES -----------------------

global daily_deaths
global daily_cases
global hospital_occupancy
global total_population
global risk
#risk               = (daily_deaths + daily_deaths)/(hospital_occupancy*total_population)

risk           = 0
number_regions = 25
scale          = 100
std            = 15

region, vor = create_regions(number_regions, scale, std)
map_regions(region, vor)

create_population(region)

test = region[4]

test.generate_region_population()
test.buildings[0].generate_house_members()
build = test.buildings[0]
build.generate_house_members()


global risk 
risk = 1
person = Person(0.5)

