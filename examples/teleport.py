import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(3, "q")
c = ClassicalRegister(3, "c")
qc = QuantumCircuit(q, c)

qc.reset(q)
qc.u(0.3, 0.2, 0.1, q[0])
qc.h(q[1])
qc.cx(q[1], q[2])
qc.barrier(q)
qc.cx(q[0], q[1])
qc.h(q[0])

qc.measure(q[0], c[0])
qc.measure(q[1], c[1])

with qc.if_test((c[0], 1)):
    qc.z(q[2])
with qc.if_test((c[1], 1)):
    qc.x(q[2])

qc.measure(q[2], c[2])
