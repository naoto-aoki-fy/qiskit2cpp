import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

magic = QuantumRegister(5, "magic")
aux = QuantumRegister(2, "aux")
meas = ClassicalRegister(5, "m")
qc = QuantumCircuit(magic, aux, meas)

for idx in range(5):
    qc.reset(magic[idx])
qc.reset(aux)

for idx in range(5):
    qc.ry(math.pi / 4, magic[idx])

qc.cx(magic[0], aux[0])
qc.cx(magic[1], aux[1])
qc.cz(aux[0], magic[2])
qc.cz(aux[1], magic[3])

for idx in range(5):
    qc.measure(magic[idx], meas[idx])
