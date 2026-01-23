sim.set_num_qubits(7);
std::vector<int> creg(5);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_ry(0.7853981633974483, 0, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.7853981633974483, 1, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.7853981633974483, 2, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.7853981633974483, 3, std::vector<int>{}, std::vector<int>{});
sim.gate_ry(0.7853981633974483, 4, std::vector<int>{}, std::vector<int>{});
sim.gate_x(5, std::vector<int>{}, std::vector<int>{0});
sim.gate_x(6, std::vector<int>{}, std::vector<int>{1});
sim.gate_z(2, std::vector<int>{}, std::vector<int>{5});
sim.gate_z(3, std::vector<int>{}, std::vector<int>{6});
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
creg[2] = sim.measure(2);
creg[3] = sim.measure(3);
creg[4] = sim.measure(4);
