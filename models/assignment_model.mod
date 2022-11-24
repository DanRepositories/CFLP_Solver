option solver gurobi;
option solver_msg 0;
option show_presolve_messages 0;
option display_round 5;
option solution_round 5;

param n;	# Cantidad de centros
param m;	# Cantidad de clientes

param J{1 .. n};
param I{1 .. m};

# Demanda de los clientes
param D{1 .. m};

# Capacidad de los centros de distribucion
param Q{1 .. n};

# Costos de abastecimiento
param C{1 .. m, 1 .. n};

# Centros de distribucion abiertos
param X{1 .. n};

# Variables de decision
var y {1 .. m, 1 .. n} binary;


# Funcion objetivo
minimize Total_Cost: (sum {i in 1..m} (sum {j in 1..n} y[i,j] * C[i,j]));

s.t.
clients {i in 1..m}: sum {j in 1..n} y[i,j] = 1;
capacities {j in 1..n}: sum {i in 1..m} y[i,j] * D[i] <= Q[j] * X[j];



