class Parser:

    def __init__(self):
        self.n = 0        # Cantidad de clientes
        self.m = 0        # Cantidad de warehouses
        self.D = None     # Demanda de los clientes (1,m)
        self.F = None     # Costo de construir los warehouses (1,n)
        self.Q = None     # Capacidad de los warehouses (1,n)
        self.C = None     # Costo de abastecer a los clientes (m,n)
        self.X = None     # Warehouses abiertos

    def dumpData(self, filename):
        with open(filename, 'w') as file:
            self.writeParam(file, 'n', self.n)
            self.writeParam(file, 'm', self.m)
            self.writeArray(file, 'Q', self.Q)
            self.writeArray(file, 'D', self.D)
            #self.writeArray(file, 'F', self.F)
            self.writeMatrix(file, 'C', self.C)
            self.writeArray(file, 'X', self.X)

    def writeParam(self, file, name_param, param):
        file.write(f'param {name_param} := {param};\n')

    def writeArray(self, file, name_param, array):
        file.write(f'param {name_param} := ')
        for i, e in enumerate(array):
            file.write(f'{i + 1} {e}    ')
        file.write(';\n\n')

    def writeMatrix(self, file, name_param, matrix):
        file.write(f'param {name_param} : ')
        cols = len(matrix[0])
        rows = len(matrix)

        for j in range(cols):
            file.write(f'{j + 1}    ')
        file.write(':= ')

        for i in range(rows):
            file.write(f'\n{i + 1}    ')
            for j in range(cols):
                file.write(f'{matrix[i][j]}    ')
            
        file.write(';\n\n')

            
    def readFile(self, filename):
        with open(filename) as file:
            n, m = self.readFirstLine(file)

            capacity, cost = self.readWarehousesInfo(file, n)

            demand, client_costs = self.readClients(file, n, m)

            self.n = n
            self.m = m
            self.D = demand
            self.F = cost
            self.Q = capacity
            self.C = client_costs

        self.X = [0] * self.n

    def readFirstLine(self, file):
        first_line = file.readline()
        data = first_line.strip().split(' ')
        n, m = data
        return int(n), int(m)

    def readWarehousesInfo(self, file, n):
        capacity = [0] * n
        cost = [0] * n
        for i in range(n):
            data = file.readline().strip().split(' ')
            current_capacity = int(data[0])
            current_cost = float(data[1])

            capacity[i] = current_capacity
            cost[i] = current_cost

        return capacity, cost

    def readClients(self, file, n, m):
        demands = [0] * m
        client_costs = []

        for i in range(m):
            current_demand, demand_cost = self.readClientInfo(file, n)
            demands[i] = current_demand
            client_costs.append(demand_cost)

        return demands, client_costs

    def readClientInfo(self, file, n):
        demand = float(file.readline().strip())
        demand_cost = []

        for line in file:
            data = list(map(lambda x: float(x), line.strip().split(' ')))
            demand_cost = demand_cost + data

            if len(demand_cost) == n:
                break

        return demand, demand_cost

