import argparse

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, qpy
from qiskit.circuit.library import HGate, XGate

NUM_QUBITS = 33

q = QuantumRegister(NUM_QUBITS, "q")
c = ClassicalRegister(NUM_QUBITS, "c")
qc = QuantumCircuit(q, c)

# Apply a Hadamard gate to every qubit.
qc.h(q)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Write this example circuit as QPY"
    )
    parser.add_argument("qpy_file", help="Output QPY path")
    args = parser.parse_args()

    with open(args.qpy_file, "wb") as f:
        qpy.dump(qc, f)
