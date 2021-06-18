# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:02:02 2021

@author: Joao
"""
import numpy as np
from environment import *
import matplotlib.pyplot as plt
#from person import *

num_regions = 25
scale       = 100
std         = 15

region, vor = create_regions(num_regions, scale, std)
map_regions(region, vor)
for each in region:
    plt.scatter(each.x_, each.y_, color = each.color, linewidth = 7)
    plt.xlim((0, 100))
    plt.ylim((0, 100))    


from shapely.geos import polygonize
from shapely.geometry import LineString, MultiPolygon, MultiPoint, Point

points = region_centers
pts = MultiPoint([Point(i) for i in points])
mask = pts.convex_hull.union(pts.buffer(10, resolution=5, cap_style=3))
result = MultiPolygon(
    [poly.intersection(mask) for poly in polygonize(lines)])
