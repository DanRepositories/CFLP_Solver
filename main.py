from amplpy import AMPL, Environment, DataFrame
import random

import numpy as np
from parseProblem import Parser
from simulated_anneling import SimulatedAnneling
from my_utility import check_feasibility, load_config

def generate_random_solution(n):
	"""
	Funcion encargada de generar una solucion inicial aleatoria de centros abiertos asociados al vector X
	@param n: número de centros
	@return warehouses: vector binario con los centros abiertos
	"""
	warehouses = [0] * n
	for i in range(n):
		if random.random() < 0.6:
			warehouses[i] = 1

	return warehouses

def get_next_step(current_solution):
	"""
	Encargada de generar una nueva solución del vector X con los centros abiertos aplicando swap a sus indices
	@param current_solution: solución actual del problema (X)
	@return new_solution: nueva solución del vector X
	"""
	new_solution = current_solution.copy()

	while True:
		# Se toman 2 indices de manera aleatoria
		indexes_to_swap = random.sample(list(range(n)), 2)
		
		for index in indexes_to_swap:
			new_solution[index] = 1 ^ new_solution[index]

		# Se valida factibilidad de la nueva solución
		if check_feasibility(new_solution, Q, D, cnf['relaxed']):
			break

	return new_solution

def objective_function(warehouses):
	"""
	Encargada de calcular la función objetivo del problema CFLP. Utilizando AMPL para el problema de asignacion
	y la suma de los costos asociados a abrir los centros.
	@param warehouse: vector binario con los centros abiertos
	@return fitness_cflp_problem: resultado de la funcion objetivo evaluada del CFLP
	"""
	# Se establecen los centro abiertos del problema de asignacion y se resuelve
	x.set_values(warehouses)
	ampl.solve()

	# Se obtiene el fitness del problema de asignacion
	fitness_assignment_problem = float(ampl.get_current_objective().value())

	# Se obtiene el costo de los centros que estan abiertos
	cost_open_warehouses = sum([F[i] * warehouses[i] for i in range(n)])

	# El fitness del cflp sera el fitness del problema de asignacion mas el costo de los warehouses
	fitness_cflp_problem = fitness_assignment_problem + cost_open_warehouses

	return fitness_cflp_problem

# Se carga las configuraciones iniciales
cnf = load_config("config.csv")

# Se parsea el problema original a un archivo .dat para ser leido por AMPL
file_data = f'{cnf["instance_folder"]}/{cnf["instance_file"]}.txt'
file_parsed = f'{cnf["output_folder"]}/{cnf["instance_file"]}.dat'

parser = Parser()
parser.readFile(file_data)
parser.dumpData(file_parsed)

n = parser.n			# Cantidad de centros de distribucion
F = parser.F			# Costo de instalacion de los centros de distribucion
D = parser.D			# Vector con las demandas de los clientes
Q = parser.Q			# Vector con las capacidades de los centros de distribucion

# Se carga AMPL
ampl = AMPL(Environment(cnf["ampl_install_folder"]))
ampl.reset()

# Se lee el modelo del problema
ampl.read(cnf["ampl_model"])

# Se leen los datos de la instancia actual
ampl.read_data(file_parsed)
x = ampl.get_parameter('X')
y = ampl.get_variable('y')

t0 = 2000
tmin = 5
alpha = 0.95

sa = SimulatedAnneling(objective_function, generate_random_solution, get_next_step, n, t0, tmin, alpha, cnf['max_iter'])

# Se válida la factibilidad del problema
if check_feasibility([1] * n, Q, D, relaxed=cnf['relaxed']):
	x_best, fit_best = sa.execute()
	print("\nFitness: ",fit_best)
	np.savetxt("warehouses.csv", np.array(x_best), fmt="%d")
	np.savetxt("clients.csv", np.array(y.get_values().to_list()))
else:
	print("Problema no factible")
