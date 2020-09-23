# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:48:35 2020

@author: gonzr
"""
import numpy as np

class Point:
    def move(self, x, y):
        self.x = x
        self.y = y
        
    def reset(self):
        self.move(0,0)

    def calculate_distance(self, other_point):
        return np.sqrt(
            (self.x - other_point.x)**2 +
            (self.y - other_point.y)**2)


point1 = Point()
point2 = Point()
point1.reset()
point2.move(5,0)
print(point2.calculate_distance(point1))
assert(point2.calculate_distance(point1) ==
        point1.calculate_distance(point2))
point1.move(3, 4)
print(point1.calculate_distance(point2))
print(point1.calculate_distance(point1))