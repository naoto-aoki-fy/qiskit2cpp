from qiskit import ClassicalRegister, QuantumCircuit
from qiskit.circuit import Gate

qc = QuantumCircuit(1, 1)
pre = Gate("pre", 1, [])
post = Gate("post", 1, [])

qc.reset(0)
qc.append(pre, [0])
qc.barrier(0)
qc.h(0)
qc.barrier(0)
qc.append(post, [0])
qc.measure(0, 0)
