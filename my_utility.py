def check_feasibility(x, capacity, demands, relaxed=False):
	# Comentar
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
    cnf = dict()
    
    with open(filename) as file:
        cnf['ampl_install_folder'] = file.readline().strip()
        cnf['instance_folder'] = file.readline().strip()
        cnf['instance_file'] = file.readline().strip()
        cnf['output_folder'] = file.readline().strip()
        cnf['ampl_model'] = file.readline().strip()

    return cnf
