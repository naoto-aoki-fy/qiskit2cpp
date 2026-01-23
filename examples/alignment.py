import math
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)

qc.barrier(0, 1, 2)
qc.cx(0, 1)
qc.delay(1, 2)
qc.u(math.pi / 4, 0.0, math.pi / 2, 2)
qc.delay(2, 2)
qc.barrier(0, 1, 2)
