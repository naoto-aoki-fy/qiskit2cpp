import argparse

from qiskit import qpy
from qiskit.circuit.random import random_circuit

qc = random_circuit(num_qubits=5, depth=10, measure=True, seed=7)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a random circuit example and write it as QPY"
    )
    parser.add_argument("qpy_file", help="Output QPY path")
    args = parser.parse_args()

    with open(args.qpy_file, "wb") as f:
        qpy.dump(qc, f)
