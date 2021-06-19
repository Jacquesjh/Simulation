# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:02:02 2021

@author: João Pedro Jacques Hoss
"""

import numpy as np
from environment import *
import matplotlib.pyplot as plt
from utils import *

number_regions = 25
scale          = 100
std            = 15

region, vor = create_regions(number_regions, scale, std)
map_regions(region, vor)

