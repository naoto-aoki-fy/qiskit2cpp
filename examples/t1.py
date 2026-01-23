from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(2, "q")
c = ClassicalRegister(2, "c")
qc = QuantumCircuit(q, c)

qc.reset(q)
qc.x(q[0])
qc.x(q[1])
qc.delay(1, q[0])
qc.delay(1, q[1])
qc.measure(q, c)
