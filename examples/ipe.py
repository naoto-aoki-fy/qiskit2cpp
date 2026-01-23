import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(1, "q")
r = QuantumRegister(1, "r")
c = ClassicalRegister(3, "c")
qc = QuantumCircuit(q, r, c)

theta = 3 * math.pi / 8
qc.reset(q)
qc.reset(r)
qc.h(r)

for idx in range(3):
    qc.reset(q[0])
    qc.h(q[0])
    qc.cp(theta * (2**idx), q[0], r[0])
    qc.h(q[0])
    qc.measure(q[0], c[idx])
