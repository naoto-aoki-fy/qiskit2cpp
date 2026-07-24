# qiskit2c

This tool converts a [Qiskit](https://qiskit.org/) ``QuantumCircuit`` into a set
of C simulator calls. Input can be either:

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
python qpy2c.py examples/example_circuit.py
```

Or first generate QPY then convert:

```bash
python examples/example_circuit.py /tmp/example_circuit.qpy
python qpy2c.py /tmp/example_circuit.qpy
```

Output:

```c
#include <stddef.h>
#include <qcs.h>

static const bit_num_t num_qubits = 14;
static const bit_num_t num_clbits = 14;

#define QCS_CHECK(call) do { int qcs_status = (call); if (qcs_status != 0) return qcs_status; } while (0)

int circuit_init(qcs_simulator* sim) {
    QCS_CHECK(qcs_simulator_set_num_qubits(sim, num_qubits));
    QCS_CHECK(qcs_simulator_set_num_clbits(sim, num_clbits));
    return 0;
}

int circuit_run(qcs_simulator* sim) {
    QCS_CHECK(qcs_simulator_gate_x(sim, (bit_num_t[]){0}, 1, NULL, 0, NULL, 0));
    QCS_CHECK(qcs_simulator_gate_x(sim, (bit_num_t[]){3}, 1, NULL, 0, (bit_num_t[]){0}, 1));
    QCS_CHECK(qcs_simulator_gate_x(sim, (bit_num_t[]){2}, 1, NULL, 0, (bit_num_t[]){0, 1}, 2));
    QCS_CHECK(qcs_simulator_gate_x(sim, (bit_num_t[]){0}, 1, NULL, 0, (bit_num_t[]){1, 2, 3, 4, 5}, 5));
    QCS_CHECK(qcs_simulator_gate_x(sim, (bit_num_t[]){4}, 1, (bit_num_t[]){0, 1}, 2, NULL, 0));
    QCS_CHECK(qcs_simulator_gate_h(sim, (bit_num_t[]){0}, 1, NULL, 0, NULL, 0));
    QCS_CHECK(qcs_simulator_gate_h(sim, (bit_num_t[]){1}, 1, NULL, 0, (bit_num_t[]){0}, 1));
    QCS_CHECK(qcs_simulator_gate_h(sim, (bit_num_t[]){13}, 1, NULL, 0, (bit_num_t[]){0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 13));
    QCS_CHECK(qcs_simulator_gate_p(sim, 1.0, (bit_num_t[]){0}, 1, NULL, 0, NULL, 0));
    QCS_CHECK(qcs_simulator_gate_u3(sim, 1.0, 2.0, 3.0, (bit_num_t[]){0}, 1, NULL, 0, NULL, 0));
    bit_t measure_result_1; QCS_CHECK(qcs_simulator_measure_to_clbit(sim, 2, 1, &measure_result_1));
    bit_t measure_result_2; QCS_CHECK(qcs_simulator_measure_to_clbit(sim, 3, 0, &measure_result_2));

    return 0;
}
```

## Acknowledgments

This repository is based on results obtained from a project, JPNP20017, commissioned by the New Energy and Industrial Technology Development Organization (NEDO).
