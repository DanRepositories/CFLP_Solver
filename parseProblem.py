class Parser:

    def __init__(self):
        """
        Contructor del objeto self el cual almacena las variables necesarias para el funcionamiento del parser, 
        estas se inicializan en None y 0.
        @param self: objeto a inicializar
        """
        self.n = 0        # Cantidad de clientes
        self.m = 0        # Cantidad de warehouses
        self.D = None     # Demanda de los clientes (1,m)
        self.F = None     # Costo de construir los warehouses (1,n)
        self.Q = None     # Capacidad de los warehouses (1,n)
        self.C = None     # Costo de abastecer a los clientes (m,n)
        self.X = None     # Warehouses abiertos

    def dumpData(self, filename):
        """
        Encargada de inicializar el objeto self dando uso de las diversas funciones complementarias
        como writeParam, writeArray y writeMatrix para la correcta lectura de AMPL
        @param self: objeto con las variables necesarias para el funcionamiento del parser
        @param filename: nombre del archivo a realizar el parser
        """
        with open(filename, 'w') as file:
            self.writeParam(file, 'n', self.n)
            self.writeParam(file, 'm', self.m)
            self.writeArray(file, 'Q', self.Q)
            self.writeArray(file, 'D', self.D)
            #self.writeArray(file, 'F', self.F)
            self.writeMatrix(file, 'C', self.C)
            self.writeArray(file, 'X', self.X)

    def writeParam(self, file, name_param, param):
        """
        Encargada generar los parametros con sus respectivos valores obtenidos desde el .txt
        @param self: objeto con las variables necesarias para el funcionamiento del parser
        @param file: archivo donde es almacenada la conversion
        @param name_param: nombre del parametro 
        @param param: vector con los valores del parametro 
        """
        file.write(f'param {name_param} := {param};\n')

    def writeArray(self, file, name_param, array):
        """
        Encargada de agregar los valores asociado a cada una de las demandas de los clientes a la fila correspondiente
        del parametro. 
        @param self: objeto con las variables necesarias para el funcionamiento del parser
        @param file: archivo donde se almacena la conversión
        @param name_param: nombre del parametro
        @param array: array con los valores del paramtro que seran agregados al file
        """
        file.write(f'param {name_param} := ')
        for i, e in enumerate(array):
            file.write(f'{i + 1} {e}    ')
        file.write(';\n\n')

    def writeMatrix(self, file, name_param, matrix):
        """
        Encargada de agregar en una matriz los costos de los clientes asociado a cada uno de los centros.
        @param self: objeto con las variables necesarias para el funcionamiento del parser
        @param file: archivo donde se almacena la conversion del txt
        @param name_param: nombre del parametro
        @param matrix: matriz donde se almacenarán los valores 
        """
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
        """
        Encargada de inicializar las variables contenidas dentro del objeto self desde el archivo filename (.txt) con la instancia del problema
        @param self: objeto que contiene las variables necesarias para el problema 
        @param filename: nombre del archivo .txt con la instancia
        """
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

        # Se inicializa el vector X (1,n) con 0
        self.X = [0] * self.n

    def readFirstLine(self, file):
        """
        Función encargada de leer la primera linea del archivo de instancia .txt asociado a los centros (n) y los clientes (m) y luego retornarlas.
        @param self: objeto que contiene las variables necesarias para el problema 
        @param file: archivo .txt donde se encuenta la instancia del problema 
        @returns n,m con los valores en enteros de la cantidad de centros y la cantidad de clientes
        """
        first_line = file.readline()
        data = first_line.strip().split(' ')
        n, m = data
        return int(n), int(m)

    def readWarehousesInfo(self, file, n):
        """
        Encargada de leer la informacion de la instancia asociada a los centros, con respecto a su capacidad y costo de instalación asociados.
        @param self: objeto con las variables necesarias para el problema
        @param file: archivo .txt donde se encuentra la instancia del problema
        @param n: cantidad de centros de la instancia
        @returns capacity, cost: que representa la capacidad de los centros y el costo de instalacion de los mismos
        """
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
        """
        Encargada de leer la informacion asociada a los clientes desde la instancia (.txt) y retornar las demandas y costos
        @param self: objeto con las variables necesarias para el funcionamiento del problema
        @param file: archivo de la instancia del problema
        @param n: cantidad de centros
        @param m: cantidad de clientes
        @returns demands, client_costs: asociado a la demanda de los clientes y los costos de transporte de los mismos respectivamente.
        """
        demands = [0] * m
        client_costs = []

        for i in range(m):
            current_demand, demand_cost = self.readClientInfo(file, n)
            demands[i] = current_demand
            client_costs.append(demand_cost)

        return demands, client_costs

    def readClientInfo(self, file, n):
        """
        Encargada de leer la informacion de un cliente de manera especifica y retornar su demanda y costos asociados.
        @param self: objeto con las variables necesarias para el funcionamiento del problema
        @param file: archivo de la instancia
        @param n: cantidad de centros
        @returns demand, demand_cost: asociadas a la demanda de un cliente y el costo de transporte del mismo respectivamente
        """
        demand = float(file.readline().strip())
        demand_cost = []

        for line in file:
            data = list(map(lambda x: float(x), line.strip().split(' ')))
            demand_cost = demand_cost + data

            if len(demand_cost) == n:
                break

        return demand, demand_cost

