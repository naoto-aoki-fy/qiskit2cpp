sim.set_num_qubits(5);
std::vector<int> creg(5);
// Unsupported operation: reset
sim.hadamard(0, {}, {});
sim.gate_rz(0.7853981633974483, 0, {}, {});
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(1, {}, {});
sim.gate_x(2, {}, {1});
sim.gate_x(1, {}, {0});
sim.hadamard(0, {}, {});
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
if (creg[0] == 1) {
    sim.gate_z(2, {}, {});
}
if (creg[1] == 1) {
    sim.gate_x(2, {}, {});
}
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(3, {}, {});
sim.gate_x(4, {}, {3});
sim.gate_x(3, {}, {2});
sim.hadamard(2, {}, {});
creg[2] = sim.measure(2);
creg[3] = sim.measure(3);
if (creg[2] == 1) {
    sim.gate_z(4, {}, {});
}
if (creg[3] == 1) {
    sim.gate_x(4, {}, {});
}
sim.hadamard(4, {}, {});
creg[4] = sim.measure(4);
