sim.set_num_qubits(2);
std::vector<int> creg(3);
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(1, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: reset
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
sim.gate_u1(0.0, 0.0, 1.1780972450961724, 0.0, 1, std::vector<int>{}, std::vector<int>{0});
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
creg[0] = sim.measure(0);
// Unsupported operation: reset
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
sim.gate_u1(0.0, 0.0, 2.356194490192345, 0.0, 1, std::vector<int>{}, std::vector<int>{0});
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
creg[1] = sim.measure(0);
// Unsupported operation: reset
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
sim.gate_u1(0.0, 0.0, 4.71238898038469, 0.0, 1, std::vector<int>{}, std::vector<int>{0});
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
creg[2] = sim.measure(0);
