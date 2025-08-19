from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.x(0)
with qc.if_test((c[0], 1)):
    qc.x(0)
with qc.while_loop((c[0], 0)):
    qc.x(0)
with qc.for_loop(range(2)):
    qc.h(0)
qc.measure(0, 0)
