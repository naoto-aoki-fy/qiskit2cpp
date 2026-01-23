import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(4, "q")
c = ClassicalRegister(4, "c")
qc = QuantumCircuit(q, c)

qc.reset(q)

angles = [0.1, 0.2, 0.3, 0.4]
for idx, angle in enumerate(angles):
    qc.ry(angle, q[idx])

qc.cx(q[0], q[1])
qc.cx(q[1], q[2])
qc.cx(q[2], q[3])

for idx in range(4):
    qc.measure(q[idx], c[idx])
