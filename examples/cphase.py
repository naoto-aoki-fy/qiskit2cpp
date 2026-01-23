import math
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)

theta = math.pi / 2
qc.u(0.0, 0.0, theta / 2, 0)
qc.cx(0, 1)
qc.u(0.0, 0.0, -theta / 2, 1)
qc.cx(0, 1)
qc.u(0.0, 0.0, theta / 2, 1)
