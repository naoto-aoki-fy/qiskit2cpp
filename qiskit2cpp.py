#!/usr/bin/env python3
"""Convert a Qiskit QuantumCircuit into qcs::simulator C++ calls."""

from __future__ import annotations

import argparse
import runpy
import sys
from dataclasses import dataclass, field
from typing import Iterable, List, Sequence

from qiskit.circuit import ClassicalRegister, Clbit, QuantumCircuit, Qubit
from qiskit.circuit.controlflow import ForLoopOp, IfElseOp, WhileLoopOp
from qiskit.circuit.controlledgate import ControlledGate


@dataclass
class EmitState:
    qubit_indices: dict[Qubit, int]
    clbit_indices: dict[Clbit, int]
    needs_pack_bits: bool = False
    lines: List[str] = field(default_factory=list)

    def indent(self, level: int) -> str:
        return "    " * level

    def emit(self, line: str, level: int = 0) -> None:
        self.lines.append(f"{self.indent(level)}{line}")


def format_param(param: object) -> str:
    try:
        return f"{float(param)}"
    except (TypeError, ValueError):
        return str(param)


def resolve_ctrl_state(ctrl_state: int | None, num_ctrl: int) -> tuple[list[int], list[int]]:
    neg: list[int] = []
    pos: list[int] = []
    if ctrl_state is None:
        return neg, pos
    for idx in range(num_ctrl):
        if ((ctrl_state >> idx) & 1) == 0:
            neg.append(idx)
        else:
            pos.append(idx)
    return neg, pos


def condition_to_cpp(condition: object, state: EmitState) -> str:
    if not isinstance(condition, tuple) or len(condition) != 2:
        return "/* unsupported condition */ true"
    bits, value = condition
    value_str = str(value)
    if isinstance(bits, Clbit):
        idx = state.clbit_indices[bits]
        return f"creg[{idx}] == {value_str}"
    if isinstance(bits, ClassicalRegister):
        indices = [state.clbit_indices[clbit] for clbit in bits]
    elif isinstance(bits, Iterable):
        indices = [state.clbit_indices[clbit] for clbit in bits]
    else:
        return "/* unsupported condition */ true"
    if len(indices) == 1:
        return f"creg[{indices[0]}] == {value_str}"
    state.needs_pack_bits = True
    indices_list = ", ".join(str(idx) for idx in indices)
    return f"pack_bits(creg, std::vector<int>{{{indices_list}}}) == {value_str}"


def neg_pos_controls(
    qargs: Sequence[Qubit],
    ctrl_state: int | None,
    num_ctrl: int,
    state: EmitState,
) -> tuple[list[int], list[int]]:
    neg_offsets, pos_offsets = resolve_ctrl_state(ctrl_state, num_ctrl)
    neg: list[int] = []
    pos: list[int] = []
    for offset in neg_offsets:
        neg.append(state.qubit_indices[qargs[offset]])
    for offset in pos_offsets:
        pos.append(state.qubit_indices[qargs[offset]])
    if ctrl_state is None:
        for qubit in qargs[:num_ctrl]:
            pos.append(state.qubit_indices[qubit])
    return neg, pos


def emit_gate_call(
    state: EmitState,
    gate_name: str,
    params: Sequence[object],
    targets: Sequence[int],
    negctrl: list[int],
    ctrl: list[int],
    level: int,
) -> None:
    def format_index_list(indices: Sequence[int]) -> str:
        inner = ", ".join(str(idx) for idx in indices)
        return f"{{{inner}}}"

    neg_expr = format_index_list(negctrl)
    pos_expr = format_index_list(ctrl)
    if gate_name in {"swap", "iswap"}:
        state.emit(
            f"sim.{gate_name}({format_index_list(targets)}, {neg_expr}, {pos_expr});",
            level,
        )
        return
    if len(targets) != 1:
        state.emit(f"// Unsupported operation: {gate_name}", level)
        return
    target = targets[0]
    param_list = ", ".join(format_param(param) for param in params)
    if param_list:
        param_list = f"{param_list}, "
    state.emit(
        f"sim.{gate_name}({param_list}{target}, {neg_expr}, {pos_expr});",
        level,
    )


def emit_instruction(
    state: EmitState,
    instruction,
    qargs: Sequence[Qubit],
    cargs: Sequence[Clbit],
    level: int,
) -> None:
    op = instruction
    name = getattr(op, "name", "")
    if name == "measure":
        for qubit, clbit in zip(qargs, cargs):
            q_index = state.qubit_indices[qubit]
            c_index = state.clbit_indices[clbit]
            state.emit(f"creg[{c_index}] = sim.measure({q_index});", level)
        return
    if isinstance(op, IfElseOp):
        cond_expr = condition_to_cpp(op.condition, state)
        state.emit(f"if ({cond_expr}) {{", level)
        emit_circuit(op.blocks[0], state, level + 1)
        if len(op.blocks) > 1:
            state.emit("} else {", level)
            emit_circuit(op.blocks[1], state, level + 1)
        state.emit("}", level)
        return
    if isinstance(op, WhileLoopOp):
        cond_expr = condition_to_cpp(op.condition, state)
        state.emit(f"while ({cond_expr}) {{", level)
        emit_circuit(op.blocks[0], state, level + 1)
        state.emit("}", level)
        return
    if isinstance(op, ForLoopOp):
        loop_parameter = getattr(op, "loop_parameter", None)
        loop_var = getattr(loop_parameter, "name", None) or "loop_num"
        indexset = getattr(op, "indexset", None)
        if isinstance(indexset, range):
            start = indexset.start
            stop = indexset.stop
            step = indexset.step
            compare = "<" if step > 0 else ">"
            state.emit(
                f"for (int {loop_var} = {start}; {loop_var} {compare} {stop}; {loop_var} += {step}) {{",
                level,
            )
        elif isinstance(indexset, (list, tuple)):
            values = ", ".join(str(value) for value in indexset)
            state.emit(
                f"for (auto {loop_var} : std::vector<int>{{{values}}}) {{",
                level,
            )
        else:
            state.emit(f"// Unsupported loop index set: {indexset}", level)
            state.emit("for (int loop_num = 0; loop_num < 0; ++loop_num) {", level)
        emit_circuit(op.blocks[0], state, level + 1)
        state.emit("}", level)
        return
    num_ctrl = getattr(op, "num_ctrl_qubits", 0)
    base_name = name
    if isinstance(op, ControlledGate):
        base_name = op.base_gate.name
        num_ctrl = op.num_ctrl_qubits
    ctrl_state = getattr(op, "ctrl_state", None)
    targets = qargs[num_ctrl:]
    target_indices = [state.qubit_indices[q] for q in targets]
    negctrl, ctrl = neg_pos_controls(qargs, ctrl_state, num_ctrl, state)
    params = getattr(op, "params", [])
    gate_map = {
        "h": "hadamard",
        "x": "gate_x",
        "y": "gate_y",
        "z": "gate_z",
        "s": "gate_s",
        "sdg": "gate_sdg",
        "t": "gate_t",
        "tdg": "gate_tdg",
        "sx": "gate_sx",
        "rx": "gate_rx",
        "ry": "gate_ry",
        "rz": "gate_rz",
        "u1": "gate_u1",
        "u2": "gate_u2",
        "u3": "gate_u3",
        "u": "gate_u3",
        "p": "gate_u1",
        "swap": "swap",
        "iswap": "iswap",
    }
    if base_name == "u1":
        params = [0.0, 0.0, params[0], 0.0]
    elif base_name == "p":
        params = [0.0, 0.0, params[0], 0.0]
    elif base_name == "u2":
        params = [params[0], params[1], 0.0]
    elif base_name in {"u3", "u"}:
        params = [params[0], params[1], params[2], 0.0]
    elif base_name in {"swap", "iswap"}:
        params = []
    mapped = gate_map.get(base_name)
    if mapped is None:
        state.emit(f"// Unsupported operation: {base_name}", level)
        return
    emit_gate_call(state, mapped, params, target_indices, negctrl, ctrl, level)


def emit_circuit(circuit: QuantumCircuit, state: EmitState, level: int) -> None:
    for instruction in circuit.data:
        op = instruction.operation
        emit_instruction(state, op, instruction.qubits, instruction.clbits, level)


def generate_cpp(qc: QuantumCircuit) -> str:
    qubit_indices = {qubit: idx for idx, qubit in enumerate(qc.qubits)}
    clbit_indices = {clbit: idx for idx, clbit in enumerate(qc.clbits)}
    state = EmitState(qubit_indices=qubit_indices, clbit_indices=clbit_indices)
    state.emit(f"sim.set_num_qubits({len(qc.qubits)});")
    if qc.clbits:
        state.emit(f"std::vector<int> creg({len(qc.clbits)});")
    emit_circuit(qc, state, 0)
    if state.needs_pack_bits:
        pack_lines = [
            "auto pack_bits = [](const std::vector<int>& creg, const std::vector<int>& bits) {",
            "    int value = 0;",
            "    for (size_t i = 0; i < bits.size(); ++i) {",
            "        value |= (creg[bits[i]] & 1) << i;",
            "    }",
            "    return value;",
            "};",
        ]
        state.lines = [state.lines[0], *pack_lines, *state.lines[1:]]
    return "\n".join(state.lines)


def load_quantum_circuit(path: str) -> QuantumCircuit:
    namespace = runpy.run_path(path)
    if "qc" not in namespace:
        raise ValueError("Python file must define a 'qc' variable containing a QuantumCircuit.")
    qc = namespace["qc"]
    if not isinstance(qc, QuantumCircuit):
        raise TypeError("'qc' must be an instance of qiskit.QuantumCircuit.")
    return qc


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to Python file defining qc.")
    args = parser.parse_args(argv)
    try:
        qc = load_quantum_circuit(args.path)
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    cpp = generate_cpp(qc)
    print(cpp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
