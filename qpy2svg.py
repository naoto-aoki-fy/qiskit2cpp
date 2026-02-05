"""Render a circuit source (Python or QPY) to SVG."""

import argparse
import runpy
from pathlib import Path

from qiskit import qpy


def load_python_circuit(path: str):
    namespace = runpy.run_path(path)
    qc = namespace.get("qc")
    if qc is None:
        raise ValueError("Circuit file must define a variable named 'qc'.")
    return qc


def load_qpy_circuit(path: str):
    with open(path, "rb") as qpy_file:
        circuits = qpy.load(qpy_file)
    if not circuits:
        raise ValueError("QPY file does not contain any circuits.")
    return circuits[0]


def load_circuit(path: str):
    if Path(path).suffix.lower() == ".qpy":
        return load_qpy_circuit(path)
    return load_python_circuit(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a Qiskit QuantumCircuit (Python or QPY) to SVG"
    )
    parser.add_argument("circuit_file", help="Input Python file or QPY file")
    parser.add_argument("svg_file", help="Output SVG path")
    args = parser.parse_args()

    qc = load_circuit(args.circuit_file)
    fig = qc.draw("mpl")
    fig.savefig(args.svg_file, format="svg", bbox_inches="tight")


if __name__ == "__main__":
    main()
