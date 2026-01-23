from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

# Simplified surface code cycle for d=3
n = 9
ancilla_count = 8

data = QuantumRegister(n, "data")
ancilla = QuantumRegister(ancilla_count, "ancilla")
layer = ClassicalRegister(ancilla_count, "layer")
results = ClassicalRegister(n, "data_out")
qc = QuantumCircuit(data, ancilla, layer, results)

qc.reset(data)
qc.reset(ancilla)

for idx in range(ancilla_count):
    qc.h(ancilla[idx])

qc.cx(data[0], ancilla[0])
qc.cx(data[1], ancilla[0])
qc.cx(data[1], ancilla[1])
qc.cx(data[2], ancilla[1])

for idx in range(ancilla_count):
    qc.measure(ancilla[idx], layer[idx])

for idx in range(n):
    qc.measure(data[idx], results[idx])
