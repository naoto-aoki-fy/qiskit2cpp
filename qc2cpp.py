"""Convert a Qiskit ``QuantumCircuit`` into C++ simulator calls.

The quantum circuit is defined in a separate Python file that must define a
variable named ``qc``.  Usage::

    python qc2cpp.py path/to/circuit_file.py

The generated C++ code is printed to standard output.
"""

import argparse
import runpy
from typing import Dict, Iterable, Tuple

from qiskit.circuit import ClassicalRegister
from qiskit.circuit.controlflow import ForLoopOp, IfElseOp, WhileLoopOp

def pack_xbits(xbits_list: Iterable) -> Tuple[Dict, list]:
    """Pack quantum or classical bits into sequential numbers."""

    xbit2num_dict: Dict = {}
    num2xbit_list = []

    for xbit_num, xbit in enumerate(xbits_list):
        xbit2num_dict[xbit] = xbit_num
        num2xbit_list.append(xbit)

    return xbit2num_dict, num2xbit_list

def get_base_gate_name(operation) -> str:
    """Return the base gate name of an operation by inspecting its type."""
    base_gate = operation
    while hasattr(base_gate, "base_gate"):
        base_gate = base_gate.base_gate
    return base_gate.name


def condition_to_cpp(condition, clbit2num_dict) -> str:
    bits, value = condition
    bits_list = bits if isinstance(bits, ClassicalRegister) else [bits]
    bit_nums = [clbit2num_dict[b] for b in bits_list]
    if len(bit_nums) == 1:
        bit_expr = f"sim.read({bit_nums[0]})"
    else:
        bit_expr = f"sim.read({{{', '.join(str(bn) for bn in bit_nums)}}})"
    return f"{bit_expr} == {value}"


def emit(instructions, qubit2num_dict, clbit2num_dict, indent: str = ""):
    for gate in instructions:
        op = gate.operation
        qubit_num_list = tuple(qubit2num_dict[q] for q in gate.qubits)
        clbit_num_list = tuple(clbit2num_dict[c] for c in gate.clbits)

        if op.name == "measure":
            print(
                indent
                + f"sim.measure({{{','.join(str(n) for n in qubit_num_list)}}}, "
                + f"{{{','.join(str(n) for n in clbit_num_list)}}});"
            )
        elif isinstance(op, IfElseOp):
            cond = condition_to_cpp(op.condition, clbit2num_dict)
            print(f"{indent}if ({cond}) {{")
            emit(op.blocks[0].data, qubit2num_dict, clbit2num_dict, indent + "    ")
            if len(op.blocks) > 1 and op.blocks[1] is not None:
                print(f"{indent}}} else {{")
                emit(op.blocks[1].data, qubit2num_dict, clbit2num_dict, indent + "    ")
            print(f"{indent}}}")
        elif isinstance(op, WhileLoopOp):
            cond = condition_to_cpp(op.condition, clbit2num_dict)
            print(f"{indent}while ({cond}) {{")
            emit(op.blocks[0].data, qubit2num_dict, clbit2num_dict, indent + "    ")
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
                cond = (
                    f"{loop_var} < {stop}" if step > 0 else f"{loop_var} > {stop}"
                )
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
                print(f"{indent}for (int {loop_var} : {{{values}}}) {{")
            else:
                count = len(sequence)
                print(
                    f"{indent}for (int {loop_var} = 0; {loop_var} < {count}; ++{loop_var}) {{",
                )

            emit(op.blocks[0].data, qubit2num_dict, clbit2num_dict, indent + "    ")
            print(f"{indent}}}")
        else:
            base_gate_name = get_base_gate_name(op)
            ctrl_qubit_num_list = qubit_num_list[:-1]
            target_qubit_num = qubit_num_list[-1]

            ctrl_state = getattr(op, "ctrl_state", None)
            neg_ctrl_qubit_num_list = []
            if ctrl_state is not None:
                for i, ctrl_qubit_num in enumerate(ctrl_qubit_num_list):
                    if not (ctrl_state >> i) & 1:
                        neg_ctrl_qubit_num_list.append(ctrl_qubit_num)

            args = [str(param) for param in gate.params]
            args.append(f"{{{target_qubit_num}}}")
            args.append(
                f"{{{', '.join(str(num) for num in ctrl_qubit_num_list)}}}"
            )
            args.append(
                f"{{{', '.join(str(num) for num in neg_ctrl_qubit_num_list)}}}"
            )
            args_str = ", ".join(args)

            print(f"{indent}sim.gate_{base_gate_name}({args_str});")


def circuit_to_cpp(qc) -> None:
    """Print a C++ representation of ``qc`` to ``stdout``."""

    # ``QuantumCircuit`` tracks registers for nested control-flow blocks, so
    # this collection covers all qubits and clbits used anywhere in ``qc``.
    qubit2num_dict, num2qubit_list = pack_xbits(qc.qubits)
    clbit2num_dict, num2clbit_list = pack_xbits(qc.clbits)

    num_qubits = len(num2qubit_list)
    print(f"sim.set_num_qubits({num_qubits});")
    num_clbits = len(num2clbit_list)
    print(f"sim.set_num_clbits({num_clbits});")

    emit(qc.data, qubit2num_dict, clbit2num_dict)


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
