sim.set_num_qubits(3);
std::vector<int> creg(3);
// Unsupported operation: reset
sim.hadamard(0, {}, {});
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(1, {}, {});
sim.hadamard(2, {}, {});
sim.gate_x(0, {}, {1, 2});
sim.gate_s(0, {}, {});
sim.gate_x(0, {}, {1, 2});
sim.gate_z(0, {}, {});
sim.hadamard(1, {}, {});
sim.hadamard(2, {}, {});
creg[0] = sim.measure(1);
creg[1] = sim.measure(2);
sim.gate_rz(2.214297435588181, 0, {}, {});
sim.hadamard(0, {}, {});
creg[2] = sim.measure(0);
