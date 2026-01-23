"""Convert a Qiskit QuantumCircuit into qcs::simulator C++ calls.

Usage:
  python qc2qcs_cpp.py path/to/circuit_file.py
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from typing import Any, Iterable, List, Tuple

from qiskit.circuit import ClassicalRegister, Clbit, QuantumCircuit
from qiskit.circuit.controlflow import ForLoopOp, IfElseOp, WhileLoopOp


INDENT_WIDTH = 4


def pack_bits(bits: Iterable[Any]) -> Tuple[dict[Any, int], List[Any]]:
    ordered = list(bits)
    return {bit: idx for idx, bit in enumerate(ordered)}, ordered


def get_base_gate_name(operation: Any) -> str:
    base = operation
    while getattr(base, "base_gate", None) is not None:
        base = base.base_gate
    return getattr(base, "name", str(base))


def condition_to_cpp(condition: Any, clbit2num: dict[Any, int]) -> str:
    bits, value = condition
    if isinstance(bits, ClassicalRegister):
        bits_list = list(bits)
    elif isinstance(bits, Clbit):
        bits_list = [bits]
    else:
        bits_list = list(bits)
    indices = [clbit2num[bit] for bit in bits_list]
    if len(indices) == 1:
        return f"creg[{indices[0]}] == {value}"
    packed_terms = [f"((creg[{idx}] & 1) << {pos})" for pos, idx in enumerate(indices)]
    packed_expr = " | ".join(packed_terms)
    return f"({packed_expr}) == {value}"


def format_vector_int(values: Iterable[int]) -> str:
    values_list = list(values)
    if not values_list:
        return "{}"
    joined = ",".join(str(v) for v in values_list)
    return f"{{{joined}}}"


def split_controls(
    controls: List[Any],
    ctrl_state: Any,
    qubit2num: dict[Any, int],
) -> Tuple[List[int], List[int]]:
    if ctrl_state is None:
        return [qubit2num[q] for q in controls], []
    positive: List[int] = []
    negative: List[int] = []
    for index, qubit in enumerate(controls):
        if (int(ctrl_state) >> index) & 1:
            positive.append(qubit2num[qubit])
        else:
            negative.append(qubit2num[qubit])
    return positive, negative


def get_exponent(operation: Any) -> Any:
    if hasattr(operation, "exponent"):
        exponent = operation.exponent
        if exponent is not None and exponent != 1:
            return exponent
    return None


def get_u_params(params: List[Any]) -> List[str]:
    # Qiskit gates may provide fewer parameters; missing values default to 0.0.
    filled = [str(param) for param in params]
    while len(filled) < 4:
        filled.append("0.0")
    return filled[:4]


def unpack_instruction(inst: Any) -> Tuple[Any, List[Any], List[Any]]:
    if hasattr(inst, "operation"):
        return inst.operation, list(inst.qubits), list(inst.clbits)
    op, qargs, cargs = inst
    return op, list(qargs), list(cargs)


def emit(
    instructions: Iterable[Any],
    qubit2num: dict[Any, int],
    clbit2num: dict[Any, int],
    indent: int,
    lines: List[str],
) -> None:
    indent_str = " " * (indent * INDENT_WIDTH)
    for inst in instructions:
        op, qargs, cargs = unpack_instruction(inst)
        if isinstance(op, IfElseOp):
            condition = condition_to_cpp(op.condition, clbit2num)
            lines.append(f"{indent_str}if ({condition}) {{")
            emit(op.blocks[0].data, qubit2num, clbit2num, indent + 1, lines)
            lines.append(f"{indent_str}}}")
            if len(op.blocks) > 1:
                lines.append(f"{indent_str}else {{")
                emit(op.blocks[1].data, qubit2num, clbit2num, indent + 1, lines)
                lines.append(f"{indent_str}}}")
            continue
        if isinstance(op, WhileLoopOp):
            condition = condition_to_cpp(op.condition, clbit2num)
            lines.append(f"{indent_str}while ({condition}) {{")
            emit(op.blocks[0].data, qubit2num, clbit2num, indent + 1, lines)
            lines.append(f"{indent_str}}}")
            continue
        if isinstance(op, ForLoopOp):
            sequence = op.params[0]
            loop_parameter = op.params[1]
            loop_var = getattr(loop_parameter, "name", None) or "loop_num"
            if isinstance(sequence, range):
                start = sequence.start
                stop = sequence.stop
                step = sequence.step
                comparator = "<" if step >= 0 else ">"
                step_expr = f"{loop_var} += {step}"
                lines.append(
                    f"{indent_str}for (int {loop_var} = {start}; {loop_var} {comparator} {stop}; {step_expr}) {{"
                )
            elif isinstance(sequence, (list, tuple)):
                values = ", ".join(str(val) for val in sequence)
                lines.append(f"{indent_str}for (int {loop_var} : {{{values}}}) {{")
            else:
                try:
                    count = len(sequence)
                except TypeError:
                    count = 0
                lines.append(
                    f"{indent_str}for (int {loop_var} = 0; {loop_var} < {count}; ++{loop_var}) {{"
                )
            emit(op.blocks[0].data, qubit2num, clbit2num, indent + 1, lines)
            lines.append(f"{indent_str}}}")
            continue

        name = getattr(op, "name", "")
        if name == "measure":
            for qubit, clbit in zip(qargs, cargs):
                q_index = qubit2num[qubit]
                c_index = clbit2num[clbit]
                lines.append(f"{indent_str}creg[{c_index}] = sim.measure({q_index});")
            continue

        base_name = get_base_gate_name(op)
        exponent = get_exponent(op)
        num_ctrl = getattr(op, "num_ctrl_qubits", 0)
        controls = qargs[:num_ctrl]
        targets = qargs[num_ctrl:]
        ctrl_state = getattr(op, "ctrl_state", None)
        ctrl_list, negctrl_list = split_controls(controls, ctrl_state, qubit2num)
        ctrl_vec = format_vector_int(ctrl_list)
        negctrl_vec = format_vector_int(negctrl_list)

        if base_name == "global_phase":
            theta = str(op.params[0]) if op.params else "0.0"
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.global_phase_pow({exponent}, {theta}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(f"{indent_str}sim.global_phase({theta}, {negctrl_vec}, {ctrl_vec});")
            continue
        if base_name == "reset":
            target = qubit2num[targets[0]] if targets else qubit2num[qargs[0]]
            lines.append(f"{indent_str}sim.reset({target});")
            continue

        if base_name in {"swap", "iswap"}:
            target_indices = [qubit2num[q] for q in targets]
            target_vec = format_vector_int(target_indices)
            if exponent is not None:
                method = "swap_pow" if base_name == "swap" else "iswap_pow"
                lines.append(
                    f"{indent_str}sim.{method}({exponent}, {target_vec}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                method = base_name
                lines.append(
                    f"{indent_str}sim.{method}({target_vec}, {negctrl_vec}, {ctrl_vec});"
                )
            continue

        if not targets:
            qubit_indices = [qubit2num[q] for q in qargs]
            clbit_indices = [clbit2num[c] for c in cargs]
            lines.append(
                f"{indent_str}// UNSUPPORTED: {name} on qubits {qubit_indices} clbits {clbit_indices}"
            )
            continue

        target = qubit2num[targets[-1]]
        if base_name == "x":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_x_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_x({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "y":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_y_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_y({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "z":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_z_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_z({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "h":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.hadamard_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.hadamard({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "s":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_s_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_s({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "sdg":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_sdg_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_sdg({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "t":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_t_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_t({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "tdg":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_tdg_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_tdg({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name == "sx":
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_sx_pow({exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_sx({target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name in {"rx", "ry", "rz"}:
            theta = str(op.params[0]) if op.params else "0.0"
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.gate_{base_name}_pow({theta}, {exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.gate_{base_name}({theta}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue
        if base_name in {"u1", "u2", "u3", "u", "u4"}:
            theta, phi, lambd, gamma = get_u_params(list(op.params))
            method = "gate_u4" if base_name in {"u", "u4"} else f"gate_{base_name}"
            if exponent is not None:
                lines.append(
                    f"{indent_str}sim.{method}_pow({theta}, {phi}, {lambd}, {gamma}, {exponent}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            else:
                lines.append(
                    f"{indent_str}sim.{method}({theta}, {phi}, {lambd}, {gamma}, {target}, {negctrl_vec}, {ctrl_vec});"
                )
            continue

        qubit_indices = [qubit2num[q] for q in qargs]
        clbit_indices = [clbit2num[c] for c in cargs]
        lines.append(
            f"{indent_str}// UNSUPPORTED: {name} on qubits {qubit_indices} clbits {clbit_indices}"
        )


def circuit_to_cpp(qc: QuantumCircuit) -> List[str]:
    qubit2num, _ = pack_bits(qc.qubits)
    clbit2num, _ = pack_bits(qc.clbits)
    num_qubits = len(qc.qubits)
    num_clbits = len(qc.clbits)
    needs_creg = False
    for inst in qc.data:
        op, _, _ = unpack_instruction(inst)
        if getattr(op, "name", "") == "measure":
            needs_creg = True
            break
        if getattr(op, "condition", None) is not None:
            needs_creg = True
            break
    lines = [f"sim.set_num_qubits({num_qubits});"]
    if num_clbits > 0 and needs_creg:
        lines.append(f"std::vector<int> creg({num_clbits}, 0);")
    emit(qc.data, qubit2num, clbit2num, 0, lines)
    return lines


def load_circuit(path: str) -> QuantumCircuit:
    spec = importlib.util.spec_from_file_location("user_circuit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load circuit file: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if not hasattr(module, "qc"):
        raise RuntimeError("Circuit file must define 'qc'.")
    qc = module.qc
    if not isinstance(qc, QuantumCircuit):
        raise RuntimeError("'qc' must be a qiskit.circuit.QuantumCircuit instance.")
    return qc


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Qiskit QuantumCircuit to qcs::simulator C++ calls.")
    parser.add_argument("path", help="Path to Python file defining `qc`.")
    args = parser.parse_args()
    qc = load_circuit(args.path)
    lines = circuit_to_cpp(qc)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
