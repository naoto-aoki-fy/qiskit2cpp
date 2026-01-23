import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

input_qubit = QuantumRegister(1, "input")
ancilla = QuantumRegister(2, "anc")
flags = ClassicalRegister(2, "flags")
output = ClassicalRegister(1, "out")
qc = QuantumCircuit(input_qubit, ancilla, flags, output)

qc.reset(input_qubit)
qc.h(input_qubit)

qc.reset(ancilla)
qc.h(ancilla)
qc.ccx(ancilla[0], ancilla[1], input_qubit[0])
qc.s(input_qubit[0])
qc.ccx(ancilla[0], ancilla[1], input_qubit[0])
qc.z(input_qubit[0])
qc.h(ancilla)

qc.measure(ancilla[0], flags[0])
qc.measure(ancilla[1], flags[1])

qc.rz(math.pi - math.acos(3 / 5), input_qubit[0])
qc.h(input_qubit[0])
qc.measure(input_qubit[0], output[0])
