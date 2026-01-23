import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

cin = QuantumRegister(1, "cin")
a = QuantumRegister(4, "a")
b = QuantumRegister(4, "b")
cout = QuantumRegister(1, "cout")
ans = ClassicalRegister(5, "ans")
qc = QuantumCircuit(cin, a, b, cout, ans)

qc.reset(cin)
qc.reset(a)
qc.reset(b)
qc.reset(cout)

# a = 0001, b = 1111
qc.x(a[0])
for idx in range(4):
    qc.x(b[idx])


def majority(qcircuit, qa, qb, qcbit):
    qcircuit.cx(qcbit, qb)
    qcircuit.cx(qcbit, qa)
    qcircuit.ccx(qa, qb, qcbit)


def unmaj(qcircuit, qa, qb, qcbit):
    qcircuit.ccx(qa, qb, qcbit)
    qcircuit.cx(qcbit, qa)
    qcircuit.cx(qa, qb)


majority(qc, cin[0], b[0], a[0])
for idx in range(3):
    majority(qc, a[idx], b[idx + 1], a[idx + 1])
qc.cx(a[3], cout[0])
for idx in reversed(range(3)):
    unmaj(qc, a[idx], b[idx + 1], a[idx + 1])
unmaj(qc, cin[0], b[0], a[0])

for idx in range(4):
    qc.measure(b[idx], ans[idx])
qc.measure(cout[0], ans[4])
