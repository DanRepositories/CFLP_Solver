from amplpy import AMPL, Environment, DataFrame
import random
from parseProblem import Parser
from simulated_anneling import SimulatedAnneling


AMPL_INSTALL_FOLDER = '/Users/dansantos/Downloads/ampl_macos64'
INSTANCE_FOLDER = 'instances'
INSTANCE_FILE = 'cap62'
OUTPUT_FOLDER = 'output_problems'
AMPL_MODEL = 'models/assignment_model.mod'


def generate_random_solution(n):
	# Generacion del nuevo conjunto de centros abiertos
	warehouses = [0] * n
	for i in range(n):
		if random.random() < 0.6:
			warehouses[i] = 1

	return warehouses

def get_next_step(current_solution):
        new_solution = current_solution.copy()

        # Take 2 random indexes
        indexes_to_swap = random.sample(list(range(n)), 2)
        idx1, idx2 = indexes_to_swap[0], indexes_to_swap[1]

        # Swap the values from the indexes
        new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
        return new_solution

def objective_function(warehouses):
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


## Se parsea el problema original a un archivo .dat para ser leido por AMPL
file_data = f'{INSTANCE_FOLDER}/{INSTANCE_FILE}.txt'
file_parsed = f'{OUTPUT_FOLDER}/{INSTANCE_FILE}.dat'

parser = Parser()
parser.readFile(file_data)
parser.dumpData(file_parsed)

n = parser.n			# Cantidad de centros de distribucion
F = parser.F			# Costo de instalacion de los centros de distribucion

# Se carga AMPL
ampl = AMPL(Environment(AMPL_INSTALL_FOLDER))
ampl.reset()

# Se lee el modelo del problema
ampl.read(AMPL_MODEL)

# Se leen los datos de la instancia actual
ampl.read_data(file_parsed)
x = ampl.get_parameter('X')

t0 = 200
tmin = 5
alpha = 0.9

sa = SimulatedAnneling(objective_function, generate_random_solution, get_next_step, n, t0, tmin, alpha)

print('\n',sa.execute())
