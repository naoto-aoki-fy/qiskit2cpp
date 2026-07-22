"""Convert a Qiskit ``QuantumCircuit`` into C simulator calls.

Input can be either:
- a Python file that defines a variable named ``qc``
- a QPY file containing at least one circuit
- a QASM file loadable via ``qiskit.qasm3`` or ``qiskit.qasm2``

Usage::

    python qpy2c.py path/to/circuit_file.py
    python qpy2c.py path/to/circuit.qpy
    python qpy2c.py path/to/circuit.qasm

The generated C code is printed to standard output.
"""

import argparse
import runpy
from pathlib import Path

from qiskit import qasm2, qasm3, qpy
from qiskit.circuit import (
    QuantumCircuit,
    AnnotatedOperation,
    Barrier,
    ClassicalRegister,
    ControlledGate,
    Gate,
    Measure,
)
from qiskit.circuit.annotated_operation import ControlModifier
from qiskit.circuit.controlflow import ForLoopOp, IfElseOp, WhileLoopOp
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.circuit.library.standard_gates.u import CUGate, UGate

STANDARD_GATE_TYPE_NAME_PAIRS = [
    (type(gate), gate_name) for gate_name, gate in get_standard_gate_name_mapping().items()
]


def get_base_gate_name(operation) -> str:
    """Return the base gate name of an operation by inspecting its type."""
    if isinstance(operation, CUGate):
        return "u4"
    if isinstance(operation, UGate):
        return "u3"

    base_gate = operation
    while hasattr(base_gate, "base_gate"):
        base_gate = base_gate.base_gate

    for gate_type, gate_name in STANDARD_GATE_TYPE_NAME_PAIRS:
        if isinstance(base_gate, gate_type):
            return gate_name

    if isinstance(base_gate, Gate):
        raise ValueError(f"Unsupported gate type for base name resolution: {type(base_gate)}")

    raise ValueError(
        f"Operation does not resolve to a Gate instance: {type(base_gate)}"
    )


def condition_to_c(condition, qc) -> str:
    bits, value = condition
    bits_list = bits if isinstance(bits, ClassicalRegister) else [bits]
    bit_nums = [qc.find_bit(bit).index for bit in bits_list]
    if len(bit_nums) == 1:
        bit_expr = f"qcs_simulator_read(sim, {bit_nums[0]})"
    else:
        terms = [
            f"(qcs_simulator_read(sim, {bit_num}) << {offset})"
            for offset, bit_num in enumerate(bit_nums)
        ]
        bit_expr = "(" + " | ".join(terms) + ")"
    return f"{bit_expr} == {value}"


def c_int_array(values) -> str:
    """Return a C argument pair for an int array pointer and element count."""
    if not values:
        return "NULL, 0"
    return f"(int[]){{{', '.join(str(value) for value in values)}}}, {len(values)}"


def get_num_ctrl_qubits(op) -> int:
    if isinstance(op, ControlledGate):
        return op.num_ctrl_qubits

    if isinstance(op, AnnotatedOperation):
        return sum(
            modifier.num_ctrl_qubits
            for modifier in op.modifiers
            if isinstance(modifier, ControlModifier)
        )

    return 0


def emit(instructions, qc, indent: str = ""):
    for gate in instructions:
        op = gate.operation
        qubit_num_list = tuple(qc.find_bit(qubit).index for qubit in gate.qubits)
        clbit_num_list = tuple(qc.find_bit(clbit).index for clbit in gate.clbits)

        if isinstance(op, Measure):
            for qubit_num, clbit_num in zip(qubit_num_list, clbit_num_list):
                print(
                    indent
                    + f"qcs_simulator_measure_to_clbit(sim, {qubit_num}, {clbit_num});"
                )
        elif isinstance(op, IfElseOp):
            cond = condition_to_c(op.condition, qc)
            print(f"{indent}if ({cond}) {{")
            emit(op.blocks[0].data, qc, indent + "    ")
            if len(op.blocks) > 1 and op.blocks[1] is not None:
                print(f"{indent}}} else {{")
                emit(op.blocks[1].data, qc, indent + "    ")
            print(f"{indent}}}")
        elif isinstance(op, WhileLoopOp):
            cond = condition_to_c(op.condition, qc)
            print(f"{indent}while ({cond}) {{")
            emit(op.blocks[0].data, qc, indent + "    ")
            print(f"{indent}}}")
        elif isinstance(op, ForLoopOp):
            sequence = op.params[0]
            loop_parameter = op.params[1]
            loop_var = (
                loop_parameter.name if loop_parameter is not None else "loop_num"
            )

            if isinstance(sequence, range):
                start = sequence.start
                stop = sequence.stop
                step = sequence.step
                cond = f"{loop_var} < {stop}" if step > 0 else f"{loop_var} > {stop}"
                increment = (
                    f"{loop_var} += {step}"
                    if step not in (1, -1)
                    else (f"++{loop_var}" if step == 1 else f"--{loop_var}")
                )
                print(
                    f"{indent}for (int {loop_var} = {start}; {cond}; {increment}) {{",
                )
            elif isinstance(sequence, (list, tuple)):
                values = ", ".join(str(x) for x in sequence)
                sequence_var = f"{loop_var}_values"
                print(f"{indent}int {sequence_var}[] = {{{values}}};")
                print(
                    f"{indent}for (unsigned int {loop_var}_index = 0; "
                    + f"{loop_var}_index < {len(sequence)}; ++{loop_var}_index) {{"
                )
                print(f"{indent}    int {loop_var} = {sequence_var}[{loop_var}_index];")
            else:
                count = len(sequence)
                print(
                    f"{indent}for (int {loop_var} = 0; {loop_var} < {count}; ++{loop_var}) {{",
                )

            emit(op.blocks[0].data, qc, indent + "    ")
            print(f"{indent}}}")
        elif isinstance(op, Barrier):
            qubits_str = ", ".join(str(n) for n in qubit_num_list)
            clbits_str = ", ".join(str(n) for n in clbit_num_list)
            print(f"{indent}// barrier qargs={{{qubits_str}}}, cargs={{{clbits_str}}}")
        else:
            base_gate_name = get_base_gate_name(op)
            num_ctrl_qubits = get_num_ctrl_qubits(op)
            both_ctrl_qubit_num_list = qubit_num_list[:num_ctrl_qubits]
            target_qubit_num_list = qubit_num_list[num_ctrl_qubits:]

            ctrl_state = getattr(op, "ctrl_state", None)
            neg_ctrl_qubit_num_list = []
            ctrl_qubit_num_list = []
            if ctrl_state is not None:
                for i, ctrl_qubit_num in enumerate(both_ctrl_qubit_num_list):
                    if (ctrl_state >> i) & 1:
                        ctrl_qubit_num_list.append(ctrl_qubit_num)
                    else:
                        neg_ctrl_qubit_num_list.append(ctrl_qubit_num)
            else:
                ctrl_qubit_num_list = list(both_ctrl_qubit_num_list)

            args = ["sim", *[str(param) for param in gate.params]]
            args.append(c_int_array(target_qubit_num_list))
            args.append(c_int_array(neg_ctrl_qubit_num_list))
            args.append(c_int_array(ctrl_qubit_num_list))
            args_str = ", ".join(args)

            print(f"{indent}qcs_simulator_gate_{base_gate_name}({args_str});")


def circuit_to_c(qc) -> None:
    """Print a C representation of ``qc`` to ``stdout``."""

    num_qubits = qc.num_qubits
    num_clbits = qc.num_clbits
    print("#include <stddef.h>")
    print("#include <qcs.h>")
    print()
    print(f"static const unsigned int num_qubits = {num_qubits};")
    print(f"static const unsigned int num_clbits = {num_clbits};")
    print()
    print("void circuit_init(qcs_simulator* sim) {")
    print("    qcs_simulator_set_num_qubits(sim, num_qubits);")
    print("    qcs_simulator_set_num_clbits(sim, num_clbits);")
    print("}")
    print()
    print("void circuit_run(qcs_simulator* sim) {")
    emit(qc.data, qc, "    ")
    print()
    print("}")


def load_python_circuit(path: str):
    namespace = runpy.run_path(path)
    qc = namespace.get("qc")
    if qc is not None:
        return qc
    qc = namespace.get("circuit")
    if qc is not None:
        return qc
    for name, value in namespace.items():
        if not name.startswith("_") and isinstance(value, QuantumCircuit):
            return value
    raise ValueError("Circuit file must define a variable named 'qc'.")


def load_qpy_circuit(path: str):
    with open(path, "rb") as qpy_file:
        circuits = qpy.load(qpy_file)
    if not circuits:
        raise ValueError("QPY file does not contain any circuits.")
    return circuits[0]


def _rewrite_qasm_for_retry(qasm_text: str) -> str:
    return (
        qasm_text.replace("OPENQASM 2.0;", "OPENQASM 3.0;")
        .replace('include "qelib1.inc";', 'include "stdgates.inc";')
    )


def load_qasm_circuit(path: str):
    qasm_text = Path(path).read_text(encoding="utf-8")

    for loader in (qasm3.loads, qasm2.loads):
        try:
            return loader(qasm_text)
        except Exception:
            pass

    rewritten_qasm = _rewrite_qasm_for_retry(qasm_text)
    if rewritten_qasm != qasm_text:
        for loader in (qasm3.loads, qasm2.loads):
            try:
                return loader(rewritten_qasm)
            except Exception:
                pass

    raise ValueError(
        "Failed to load QASM via qiskit.qasm3/qiskit.qasm2, including retry with "
        "OPENQASM/stdgates replacements."
    )


def load_circuit(path: str):
    suffix = Path(path).suffix.lower()
    if suffix == ".qpy":
        return load_qpy_circuit(path)
    if suffix in {".qasm", ".qasm2", ".qasm3"}:
        return load_qasm_circuit(path)
    return load_python_circuit(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Qiskit QuantumCircuit (Python, QPY, or QASM) to C"
    )
    parser.add_argument("circuit_file", help="Input Python, QPY, or QASM file")
    args = parser.parse_args()

    qc = load_circuit(args.circuit_file)
    circuit_to_c(qc)


if __name__ == "__main__":
    main()
