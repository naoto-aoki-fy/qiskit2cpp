from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import HGate, XGate

q = QuantumRegister(14)
c = ClassicalRegister(14)
qc = QuantumCircuit(q, c)

qc.x(q[0])
qc.cx(q[0], q[3])
qc.ccx(q[0], q[1], q[2])
qc.mcx(q[1:6], q[0])

qc.append(XGate().control(2, ctrl_state=0b10), [q[0], q[1], q[4]])

qc.h(q[0])
qc.ch(q[0], q[1])
qc.append(HGate().control(13), q)

qc.p(1.0, q[0])
qc.u(1.0, 2.0, 3.0, q[0])

qc.measure(q[2], c[1])
qc.measure(q[3], c[0])

