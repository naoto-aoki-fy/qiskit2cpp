# qiskit's QuantumCircuit to C++ converter

This tool converts a [Qiskit](https://qiskit.org/) ``QuantumCircuit`` into a set
of C++ simulator calls.  Define your circuit in a separate Python file that
exposes a variable named ``qc`` and pass that file to the converter.

## Example

`example_circuit.py`

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

