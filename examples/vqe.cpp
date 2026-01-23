sim.set_num_qubits(4);
std::vector<int> creg(4);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_ry(0.1, 0, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.2, 1, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.3, 2, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.4, 3, std::vector<int>{}, std::vector<int>{});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(3, std::vector<int>{}, std::vector<int>{2});
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
creg[2] = sim.measure(2);
creg[3] = sim.measure(3);
