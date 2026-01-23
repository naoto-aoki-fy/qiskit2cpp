sim.set_num_qubits(2);
std::vector<int> creg(2);
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: barrier
sim.gate_z(1, std::vector<int>{}, std::vector<int>{0});
// Unsupported operation: barrier
sim.gate_s(0, std::vector<int>{}, std::vector<int>{});
sim.gate_z(1, std::vector<int>{}, std::vector<int>{0});
// Unsupported operation: barrier
sim.gate_s(0, std::vector<int>{}, std::vector<int>{});
sim.gate_z(0, std::vector<int>{}, std::vector<int>{});
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: barrier
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
