sim.set_num_qubits(2);
std::vector<int> creg(2);
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(0, {}, {});
// Unsupported operation: barrier
sim.gate_z(1, {}, {0});
// Unsupported operation: barrier
sim.gate_s(0, {}, {});
sim.gate_z(1, {}, {0});
// Unsupported operation: barrier
sim.gate_s(0, {}, {});
sim.gate_z(0, {}, {});
sim.hadamard(0, {}, {});
// Unsupported operation: barrier
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
