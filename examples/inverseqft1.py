import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(4, "q")
c = ClassicalRegister(4, "c")
qc = QuantumCircuit(q, c)

qc.reset(q)
qc.h(q)
qc.barrier(q)

qc.h(q[0])
qc.measure(q[0], c[0])
with qc.if_test((c, 1)):
    qc.rz(math.pi / 2, q[1])

qc.h(q[1])
qc.measure(q[1], c[1])
with qc.if_test((c, 1)):
    qc.rz(math.pi / 4, q[2])
with qc.if_test((c, 2)):
    qc.rz(math.pi / 2, q[2])
with qc.if_test((c, 3)):
    qc.rz(math.pi / 2 + math.pi / 4, q[2])

qc.h(q[2])
qc.measure(q[2], c[2])
with qc.if_test((c, 1)):
    qc.rz(math.pi / 8, q[3])
with qc.if_test((c, 2)):
    qc.rz(math.pi / 4, q[3])
with qc.if_test((c, 3)):
    qc.rz(math.pi / 4 + math.pi / 8, q[3])
with qc.if_test((c, 4)):
    qc.rz(math.pi / 2, q[3])
with qc.if_test((c, 5)):
    qc.rz(math.pi / 2 + math.pi / 8, q[3])
with qc.if_test((c, 6)):
    qc.rz(math.pi / 2 + math.pi / 4, q[3])
with qc.if_test((c, 7)):
    qc.rz(math.pi / 2 + math.pi / 4 + math.pi / 8, q[3])

qc.h(q[3])
qc.measure(q[3], c[3])
