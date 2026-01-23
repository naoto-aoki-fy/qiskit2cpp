sim.set_num_qubits(2);
std::vector<int> creg(2);
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_x(0, {}, {});
sim.gate_x(1, {}, {});
// Unsupported operation: delay
// Unsupported operation: delay
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
