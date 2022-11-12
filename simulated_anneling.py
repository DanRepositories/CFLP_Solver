import random
import math
import numpy as np

class SimulatedAnneling():
    def __init__(self, function, generate_initial, next_step, D, T0, Tmin, alpha):
        self.function = function
        self.generate_initial_solution = generate_initial
        self.next_step = next_step
        self.T0 = T0
        self.Tmin = Tmin
        self.alpha = alpha
        self.X = np.array([])
        self.Xfitness = 0       # Fitness of current X solution
        self.best = np.array([])
        self.F_min = 0          # Fitness of best solution
        self.D = D

    def update_temp(self, current_temp):
        new_temp = self.alpha * current_temp
        return new_temp

    def get_probability(self, delta_fitness, current_temp):
        probability = math.exp(-delta_fitness / current_temp)
        return probability

    def execute(self):
        self.X = self.generate_initial_solution(self.D)
        self.Xfitness = self.function(self.X)
        self.best = self.X.copy()
        self.F_min = self.Xfitness

        t = self.T0
        while t > self.Tmin:
            # Generate a new solution from the current X solution
            newX = self.next_step(self.X)
            newX_fitness = self.function(newX)
        
            delta_fitness = newX_fitness - self.Xfitness

            if delta_fitness < 0:
                self.X = newX.copy()
                self.Xfitness = newX_fitness
            else:
                p = self.get_probability(delta_fitness, t)

                if random.random() < p:
                    self.X = newX.copy()
                    self.Xfitness = newX_fitness

            if self.Xfitness < self.F_min:
                self.best = self.X.copy()
                self.F_min = self.Xfitness

            t = self.update_temp(t)

        return self.best, self.F_min

