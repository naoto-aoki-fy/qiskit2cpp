sim.set_num_qubits(2);
std::vector<int> creg(3);
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(1, {}, {});
// Unsupported operation: reset
sim.hadamard(0, {}, {});
sim.gate_u1(0.0, 0.0, 1.1780972450961724, 0.0, 1, {}, {0});
sim.hadamard(0, {}, {});
creg[0] = sim.measure(0);
// Unsupported operation: reset
sim.hadamard(0, {}, {});
sim.gate_u1(0.0, 0.0, 2.356194490192345, 0.0, 1, {}, {0});
sim.hadamard(0, {}, {});
creg[1] = sim.measure(0);
// Unsupported operation: reset
sim.hadamard(0, {}, {});
sim.gate_u1(0.0, 0.0, 4.71238898038469, 0.0, 1, {}, {0});
sim.hadamard(0, {}, {});
creg[2] = sim.measure(0);
