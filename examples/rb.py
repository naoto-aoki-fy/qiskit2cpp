from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

q = QuantumRegister(2, "q")
c = ClassicalRegister(2, "c")
qc = QuantumCircuit(q, c)

qc.reset(q)
qc.h(q[0])
qc.barrier(q)
qc.cz(q[0], q[1])
qc.barrier(q)
qc.s(q[0])
qc.cz(q[0], q[1])
qc.barrier(q)
qc.s(q[0])
qc.z(q[0])
qc.h(q[0])
qc.barrier(q)

qc.measure(q, c)
