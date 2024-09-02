# This file is part of the TCAS Server. Do not redistribute.
# Defines Puck_Server class, derived from Puck class; adds init method

import numpy as np
import pygame
import puck

class Puck_Server(puck.Puck):
    SCALE = 10
    FUEL = 200.0

    def __init__(self, id, t, s, v):
        self.id = id
        self.alive = True
        self.state = "alive"
        self.name = ""
        self.t = t
        self.s = s
        self.v = v
        self.a = np.array([0.0, 0.0])
        self.fuel = Puck_Server.FUEL
        self.points = 0

    def set_name(self, name):
         self.name = name

    def set_acceleration(self, acceleration):
         self.a = acceleration

    def add_points(self, points):
        self.points += points

    def farewell(self):
        print(f"Puck {self.id} ({self.name}): {self.state}, {self.points} Punkte.")

    def kill(self, screen, reason):
        self.show(screen, pygame.Color("black"))
        self.alive = False
        self.state = reason
        self.farewell()

    def show(self, screen, color):
        pygame.draw.circle(screen, color,
                          (Puck_Server.SCALE*self.s[0],
                           Puck_Server.SCALE*self.s[1]),
                           Puck_Server.SCALE*Puck_Server.RADIUS)


    def update(self, screen, t, box):
        self.show(screen, pygame.Color("black"))
        dt = t - self.t
        self.t = t
        delta_v = self.a*dt
        delta_fuel = np.linalg.norm(delta_v)
        if delta_fuel > 0.0 and delta_fuel <= self.fuel:
            self.fuel -= delta_fuel
        else:
            delta_v = 0.0
        self.s += (self.v + 0.5*delta_v)*dt
        self.v +=  delta_v
#       bounce on box walls
        if self.s[0] - Puck_Server.RADIUS < box.xmin:
            self.s[0]  = 2.0*(box.xmin + Puck_Server.RADIUS) - self.s[0]
            self.v[0] = -self.v[0]
            self.add_points(1)
        if self.s[0] + Puck_Server.RADIUS > box.xmax:
            self.s[0]  = 2.0*(box.xmax - Puck_Server.RADIUS) - self.s[0]
            self.v[0] = -self.v[0]
            self.add_points(1)
        if self.s[1] - Puck_Server.RADIUS < box.ymin:
            self.s[1]  = 2.0*(box.ymin + Puck_Server.RADIUS) - self.s[1]
            self.v[1] = -self.v[1]
            self.add_points(1)
        if self.s[1] + Puck_Server.RADIUS > box.ymax:
            self.s[1]  = 2.0*(box.ymax - Puck_Server.RADIUS) - self.s[1]
            self.v[1] = -self.v[1]
            self.add_points(1)
        self.show(screen, pygame.Color("white"))
