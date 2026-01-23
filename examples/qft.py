import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(4, "q")
c = ClassicalRegister(4, "c")
qc = QuantumCircuit(q, c)

qc.reset(q)
qc.x(q[0])
qc.x(q[2])
qc.barrier(q)

qc.h(q[0])
qc.cp(math.pi / 2, q[1], q[0])
qc.h(q[1])
qc.cp(math.pi / 4, q[2], q[0])
qc.cp(math.pi / 2, q[2], q[1])
qc.h(q[2])
qc.cp(math.pi / 8, q[3], q[0])
qc.cp(math.pi / 4, q[3], q[1])
qc.cp(math.pi / 2, q[3], q[2])
qc.h(q[3])

for idx in range(4):
    qc.measure(q[idx], c[idx])
