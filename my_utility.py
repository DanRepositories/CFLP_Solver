def check_feasibility(x, capacity, demands, relaxed=False):
	"""
	Encargada de validar la instancia con respecto a la capacidad de los centros y la demanda de los clientes
	@param x: vector binario con solo valores 1 
	@param capacity: vector con la capacidad de cada uno de los centros
	@param demands: vector con las demandas de los clientes
	@param relaxed: variable boolean que valida si es un problema relajado (True) o no relajado (False)
	@return Boolean: True si es factible, False si no es factible
	"""
	sum_capacities = 0
	for i, c in enumerate(capacity):
		sum_capacities = sum_capacities + c * x[i]

	sum_demands = sum(demands)
	
	if relaxed:
		return sum_demands <= sum_capacities
	else:
		max_demands = max(demands)
		max_capacity = max(capacity)
		return sum_demands <= sum_capacities and max_demands <= max_capacity

def load_config(filename):
	"""
	Encargada de leer la configuracion desde el archivo config.csv y almacenarlos en un diccionario de datos cnf
	@param filename: nombre del archivo .csv
	@return cnf: diccionario con los datos de la configuración
	"""
	cnf = dict()
	
	with open(filename) as file:
		cnf['ampl_install_folder'] = file.readline().strip()
		cnf['instance_folder'] = file.readline().strip()
		cnf['instance_file'] = file.readline().strip()
		cnf['output_folder'] = file.readline().strip()
		cnf['ampl_model'] = file.readline().strip()
		cnf['max_iter'] = int(file.readline().strip())
		cnf['relaxed'] = int(file.readline().strip()) == 1

	return cnf
