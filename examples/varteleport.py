import math
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

input_qubit = QuantumRegister(1, "input")
q = QuantumRegister(4, "q")
meas = ClassicalRegister(4, "m")
output = ClassicalRegister(1, "out")
qc = QuantumCircuit(input_qubit, q, meas, output)

qc.reset(input_qubit)
qc.h(input_qubit)
qc.rz(math.pi / 4, input_qubit)

pair_indices = [(0, 1), (2, 3)]
current = input_qubit[0]
for pair_idx, (a, b) in enumerate(pair_indices):
    qc.reset(q[a])
    qc.reset(q[b])
    qc.h(q[a])
    qc.cx(q[a], q[b])

    qc.cx(current, q[a])
    qc.h(current)
    qc.measure(current, meas[2 * pair_idx])
    qc.measure(q[a], meas[2 * pair_idx + 1])

    with qc.if_test((meas[2 * pair_idx], 1)):
        qc.z(q[b])
    with qc.if_test((meas[2 * pair_idx + 1], 1)):
        qc.x(q[b])

    current = q[b]

qc.h(current)
qc.measure(current, output[0])
