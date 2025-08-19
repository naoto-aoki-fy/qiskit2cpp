# qiskit's QuantumCircuit to C++ converter

This tool converts a [Qiskit](https://qiskit.org/) ``QuantumCircuit`` into a set
of C++ simulator calls.  Define your circuit in a separate Python file that
exposes a variable named ``qc`` and pass that file to the converter.

## Example

### `example_circuit.py`

```python
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import HGate, XGate

q = QuantumRegister(14)
c = ClassicalRegister(14)
qc = QuantumCircuit(q, c)

qc.x(q[0])
qc.cx(q[0], q[3])
qc.ccx(q[0], q[1], q[2])
qc.mcx(q[1:6], q[0])

qc.append(XGate().control(2, ctrl_state=0b10), [q[0], q[1], q[4]])

qc.h(q[0])
qc.ch(q[0], q[1])
qc.append(HGate().control(13), q)

qc.p(1.0, q[0])
qc.u(1.0, 2.0, 3.0, q[0])

qc.measure(q[2], c[1])
qc.measure(q[3], c[0])
```

Run the converter:

```bash
python qc2cpp.py example_circuit.py
```

Output:

```c++
sim.set_num_qubits(14);
sim.set_num_clbits(14);
sim.gate_x({0}, {}, {});
sim.gate_x({3}, {0}, {});
sim.gate_x({2}, {0, 1}, {});
sim.gate_x({0}, {1, 2, 3, 4, 5}, {});
sim.gate_x({4}, {0, 1}, {0});
sim.gate_h({0}, {}, {});
sim.gate_h({1}, {0}, {});
sim.gate_h({13}, {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, {});
sim.gate_p(1.0, {0}, {}, {});
sim.gate_u(1.0, 2.0, 3.0, {0}, {}, {});
sim.measure({2}, {1});
sim.measure({3}, {0});
```

The third argument of each gate lists the control qubit indices that must be 0.

### `example_control_flow.py`

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.x(0)
with qc.if_test((c[0], 1)):
    qc.x(0)
with qc.while_loop((c[0], 0)):
    qc.x(0)
with qc.for_loop([1, 3, 4, 9]) as i:
    qc.rx(i, 0)
with qc.for_loop((1, 3, 4, 9)) as j:
    qc.ry(j, 0)
with qc.for_loop(range(0, 10, 2)) as k:
    qc.rz(k, 0)
qc.measure(0, 0)
```

```c++
sim.set_num_qubits(1);
sim.set_num_clbits(1);
sim.gate_x({0}, {}, {});
if (sim.read(0) == 1) {
    sim.gate_x({0}, {}, {});
}
while (sim.read(0) == 0) {
    sim.gate_x({0}, {}, {});
}
for (int _loop_i_0 : {1, 3, 4, 9}) {
    sim.gate_rx(_loop_i_0, {0}, {}, {});
}
for (int _loop_i_1 : {1, 3, 4, 9}) {
    sim.gate_ry(_loop_i_1, {0}, {}, {});
}
for (int _loop_i_2 = 0; _loop_i_2 < 10; _loop_i_2 += 2) {
    sim.gate_rz(_loop_i_2, {0}, {}, {});
}
sim.measure({0}, {0});
```