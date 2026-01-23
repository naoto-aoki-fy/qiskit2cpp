sim.set_num_qubits(4);
std::vector<int> creg(4);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(0, {}, {});
sim.hadamard(1, {}, {});
sim.hadamard(2, {}, {});
sim.hadamard(3, {}, {});
// Unsupported operation: barrier
sim.hadamard(0, {}, {});
creg[0] = sim.measure(0);
if (creg[0] == 1) {
    sim.gate_rz(1.5707963267948966, 1, {}, {});
}
sim.hadamard(1, {}, {});
creg[1] = sim.measure(1);
if (creg[0] == 1) {
    sim.gate_rz(0.7853981633974483, 2, {}, {});
}
if (creg[1] == 1) {
    sim.gate_rz(1.5707963267948966, 2, {}, {});
}
sim.hadamard(2, {}, {});
creg[2] = sim.measure(2);
if (creg[0] == 1) {
    sim.gate_rz(0.39269908169872414, 3, {}, {});
}
if (creg[1] == 1) {
    sim.gate_rz(0.7853981633974483, 3, {}, {});
}
if (creg[2] == 1) {
    sim.gate_rz(1.5707963267948966, 3, {}, {});
}
sim.hadamard(3, {}, {});
creg[3] = sim.measure(3);
