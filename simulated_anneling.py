import random
import math
import numpy as np
class SimulatedAnneling():
    def __init__(self, function, generate_initial, next_step, D, T0, Tmin, alpha, max_iter):
        """
        Contructor del objeto self el cual almacena las variables necesarias para el funcionamiento de la heurística
        @param self: objeto a inicializar
        @param function: funcion objetivo del algoritmo CFLP
        @param generate_initial: funcion encargada de crear una solucion inicial del vector x con los centros abiertos
        @param next_step: función encargada de obtener una nueva solución aplicando swap en sus indices
        @param D: vector con las demandas de los clientes (1,m)
        @param T0: temperatura inicial del algoritmo
        @param Tmin: temperatura minima que puede alcanzar la heurística para terminar el proceso
        @param alpha: constante encargada de actualizar la temperatura
        @param max_iter: cantidad de iteraciones maximas para terminar el proceso de la heuristica
        """
        self.function = function
        self.generate_initial_solution = generate_initial
        self.next_step = next_step
        self.T0 = T0
        self.Tmin = Tmin
        self.alpha = alpha
        self.X = np.array([])
        self.Xfitness = 0       # Fitness de la solución X actual
        self.best = np.array([])
        self.F_min = 0          # Fitness de la mejor solución
        self.D = D
        self.max_iter = max_iter

    def update_temp(self, current_temp):
        """
        Actualiza la temperatura de la heurística multiplicandola por alpha 
        @param self: objeto con las variables necesarias para el funcionamiento de la heurística
        @current_temp: temperatura actual de  la heurística   
        @return new_temp: nueva temperatura generada
        """
        new_temp = self.alpha * current_temp
        return new_temp

    def get_probability(self, delta_fitness, current_temp):
        """
        Calcula la probabilidad asociada a la exploración del algoritmo 
        @param self: objeto con las variables necesarias para el funcionamiento de la heurística 
        @param delta_fitness: diferencia entre el mejor fitness y el actual fitness obtenido
        @param current_temp: temperatura actual de la heurística
        @return probability: probabilidad de exploración del algoritmo
        """
        probability = math.exp(-delta_fitness / current_temp)
        return probability

    def execute(self):
        """
        Encargada de ejecutar la heurística simulated annealing
        @param self: objeto con las variables necesarias para el funcionamiento de la heurística
        @returns self.best y self.F_min: que representa al mejor vector X con los centros abiertos y el fitness de la funcion
        objetivo evaluada con el vector X respectivamente
        """
        self.X = self.generate_initial_solution(self.D)
        self.Xfitness = self.function(self.X)
        self.best = self.X.copy()
        self.F_min = self.Xfitness

        fitness_array = []
        t = self.T0
        current_iter = 0

        while (current_iter < self.max_iter):

            # Se almacena el mejor fitness actual
            fitness_array.append(self.F_min)

            # Se genera una nueva solución a partir de la solución actual
            newX = self.next_step(self.X)
            newX_fitness = self.function(newX)
        
            delta_fitness = newX_fitness - self.Xfitness

            # Actualizamos la solución actual del problema
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

            # Actualizamos temperatura de la heurística
            t = self.update_temp(t)
            if t < self.Tmin:
                t = self.Tmin

            current_iter += 1

        return self.best, self.F_min
