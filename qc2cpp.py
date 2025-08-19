"""Convert a Qiskit ``QuantumCircuit`` into C++ simulator calls.

The quantum circuit is defined in a separate Python file that must define a
variable named ``qc``.  Usage::

    python qc2cpp.py path/to/circuit_file.py

The generated C++ code is printed to standard output.
"""

import argparse
import runpy
from typing import Iterable, Tuple, Dict


def pack_registers(registers_list: Iterable) -> Tuple[Dict, list]:
    """Pack quantum or classical registers into sequential numbers."""

    xbit2num_dict: Dict = {}
    num2xbit_list = []

    xbit_num = 0
    for register in registers_list:
        for xbit in register:
            xbit2num_dict[xbit] = xbit_num
            assert len(num2xbit_list) == xbit_num
            num2xbit_list.append(xbit)
            xbit_num += 1

    return xbit2num_dict, num2xbit_list


def get_base_gate_name(operation) -> str:
    """Return the base gate name of an operation by inspecting its type."""
    base_gate = operation
    while hasattr(base_gate, "base_gate"):
        base_gate = base_gate.base_gate
    return base_gate.name


def circuit_to_cpp(qc) -> None:
    """Print a C++ representation of ``qc`` to ``stdout``."""

    quantum_registers_set = set()
    classical_registers_set = set()

    for gate in qc.data:
        for qubit in gate.qubits:
            quantum_registers_set.add(qubit._register)
        for clbit in gate.clbits:
            classical_registers_set.add(clbit._register)

    quantum_registers_list = tuple(quantum_registers_set)
    classical_registers_list = tuple(classical_registers_set)

    qubit2num_dict, num2qubit_list = pack_registers(quantum_registers_list)
    clbit2num_dict, num2clbit_list = pack_registers(classical_registers_list)

    num_qubits = len(num2qubit_list)
    print(f"set_num_qubits({num_qubits});")
    num_clbits = len(num2clbit_list)
    print(f"set_num_clbits({num_clbits});")

    for gate in qc.data:
        qubit_num_list = tuple(qubit2num_dict[qubit] for qubit in gate.qubits)
        clbit_num_list = tuple(clbit2num_dict[clbit] for clbit in gate.clbits)
        if gate.operation.name == "measure":
            print(
                f"sim.measure({{{','.join(str(qubit_num) for qubit_num in qubit_num_list)}}}, "
                f"{{{','.join(str(clbit_num) for clbit_num in clbit_num_list)}}});"
            )
        else:
            base_gate_name = get_base_gate_name(gate.operation)
            ctrl_qubit_num_list = qubit_num_list[:-1]
            target_qubit_num = qubit_num_list[-1]

            ctrl_state = getattr(gate.operation, "ctrl_state", None)
            neg_ctrl_qubit_num_list = []
            if ctrl_state is not None:
                for i, ctrl_qubit_num in enumerate(ctrl_qubit_num_list):
                    if not (ctrl_state >> i) & 1:
                        neg_ctrl_qubit_num_list.append(ctrl_qubit_num)

            args = [str(param) for param in gate.params]
            args.append(f"{{{target_qubit_num}}}")
            args.append(f"{{{', '.join(str(ctrl_qubit_num) for ctrl_qubit_num in ctrl_qubit_num_list)}}}")
            args.append(f"{{{', '.join(str(num) for num in neg_ctrl_qubit_num_list)}}}")
            args_str = ", ".join(args)

            print(f"sim.gate_{base_gate_name}({args_str});")


def load_circuit(path: str):
    """Load a QuantumCircuit from ``path`` which defines ``qc``."""

    namespace = runpy.run_path(path)
    qc = namespace.get("qc")
    if qc is None:
        raise ValueError("Circuit file must define a variable named 'qc'.")
    return qc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Qiskit QuantumCircuit defined in another file to C++"
    )
    parser.add_argument("circuit_file", help="Python file that defines a variable 'qc'")
    args = parser.parse_args()

    qc = load_circuit(args.circuit_file)
    circuit_to_cpp(qc)


if __name__ == "__main__":
    main()

