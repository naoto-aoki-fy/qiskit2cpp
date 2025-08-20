from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

with qc.for_loop([1, 3, 4, 9]) as i:
    qc.rx(i, 0)

    with qc.for_loop((1, 3, 4, 9)) as j:
        qc.ry(j, 0)

        with qc.for_loop(range(0, 10, 2)) as k:
            qc.rz(k, 0)

qc.measure(0, 0)
with qc.while_loop((c[0], 0)):
    qc.x(0)
    qc.measure(0, 0)

