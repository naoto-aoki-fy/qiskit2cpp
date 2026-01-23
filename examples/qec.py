import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(3, "q")
a = QuantumRegister(2, "a")
c = ClassicalRegister(3, "c")
syn = ClassicalRegister(2, "syn")
qc = QuantumCircuit(q, a, c, syn)

qc.reset(q)
qc.reset(a)
qc.x(q[0])
qc.barrier(q)

qc.cx(q[0], a[0])
qc.cx(q[1], a[0])
qc.cx(q[1], a[1])
qc.cx(q[2], a[1])

qc.measure(a[0], syn[0])
qc.measure(a[1], syn[1])

with qc.if_test((syn, 1)):
    qc.x(q[0])
with qc.if_test((syn, 2)):
    qc.x(q[2])
with qc.if_test((syn, 3)):
    qc.x(q[1])

for idx in range(3):
    qc.measure(q[idx], c[idx])
