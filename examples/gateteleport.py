import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(3, "q")
a = QuantumRegister(3, "a")
c = ClassicalRegister(3, "c")
qc = QuantumCircuit(q, a, c)

for idx in range(3):
    qc.rz(math.pi / 4, a[idx])

for idx in range(3):
    qc.cx(q[idx], a[idx])

for idx in range(3):
    qc.measure(a[idx], c[idx])

with qc.if_test((c[0], 1)):
    for idx in range(3):
        qc.z(q[idx])
