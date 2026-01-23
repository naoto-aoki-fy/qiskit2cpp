from qiskit import QuantumCircuit

qc = QuantumCircuit(4)

qc.delay(1, 0)
qc.x(0)
qc.delay(1, 0)
qc.y(0)
qc.delay(1, 0)
qc.x(0)
qc.delay(1, 0)
qc.y(0)
qc.delay(1, 0)

qc.cx(2, 3)
qc.cx(1, 2)
qc.u(0.0, 0.0, 0.0, 3)
