# qiskit2c

This tool converts a [Qiskit](https://qiskit.org/) ``QuantumCircuit`` into a set
of C simulator calls for the C interface exposed by
[`rqs-svg`](https://github.com/naoto-aoki-fy/rqs-svg). Input can be either:

- a Python file that exposes a variable named ``qc``
- a QPY file containing at least one circuit
- a QASM file loadable via ``qiskit.qasm3`` or ``qiskit.qasm2``

## Example

### `examples/example_circuit.py`

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

qc.append(XGate().control(2, ctrl_state=0b00), [q[0], q[1], q[4]])

qc.h(q[0])
qc.ch(q[0], q[1])
qc.append(HGate().control(13), q)

qc.p(1.0, q[0])
qc.u(1.0, 2.0, 3.0, q[0])

qc.measure(q[2], c[1])
qc.measure(q[3], c[0])
```

Run the converter directly from Python input:

```bash
python qiskit2c.py examples/example_circuit.py
```

Or first generate QPY then convert:

```bash
python examples/example_circuit.py /tmp/example_circuit.qpy
python qiskit2c.py /tmp/example_circuit.qpy
```

Output:

```c
#include <stddef.h>
#include <qcs.h>

static const unsigned int num_qubits = 14;
static const unsigned int num_clbits = 14;

static unsigned long long read_clbits(qcs_simulator* sim, const int* clbits, size_t num_bits) {
    unsigned long long value = 0;
    for (size_t i = 0; i < num_bits; ++i) {
        if (qcs_read(sim, clbits[i])) {
            value |= 1ULL << i;
        }
    }
    return value;
}

void circuit_init(qcs_simulator* sim) {
    qcs_set_num_qubits(sim, num_qubits);
    qcs_set_num_clbits(sim, num_clbits);
}

void circuit_run(qcs_simulator* sim) {
    qcs_gate_x(sim, (int[]){0}, 1, NULL, 0, NULL, 0);
    qcs_gate_x(sim, (int[]){3}, 1, NULL, 0, (int[]){0}, 1);
    qcs_gate_x(sim, (int[]){2}, 1, NULL, 0, (int[]){0, 1}, 2);
    qcs_gate_x(sim, (int[]){0}, 1, NULL, 0, (int[]){1, 2, 3, 4, 5}, 5);
    qcs_gate_x(sim, (int[]){4}, 1, (int[]){0, 1}, 2, NULL, 0);
    qcs_gate_h(sim, (int[]){0}, 1, NULL, 0, NULL, 0);
    qcs_gate_h(sim, (int[]){1}, 1, NULL, 0, (int[]){0}, 1);
    qcs_gate_h(sim, (int[]){13}, 1, NULL, 0, (int[]){0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 13);
    qcs_gate_p(sim, 1.0, (int[]){0}, 1, NULL, 0, NULL, 0);
    qcs_gate_u3(sim, 1.0, 2.0, 3.0, (int[]){0}, 1, NULL, 0, NULL, 0);
    qcs_measure(sim, 2, 1);
    qcs_measure(sim, 3, 0);

}
```

## Acknowledgments

This repository is based on results obtained from a project, JPNP20017, commissioned by the New Energy and Industrial Technology Development Organization (NEDO).
