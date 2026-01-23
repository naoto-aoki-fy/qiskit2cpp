sim.set_num_qubits(4);
std::vector<int> creg(4);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_x(0, std::vector<int>{}, std::vector<int>{});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: barrier
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
sim.gate_u1(0.0, 0.0, 1.5707963267948966, 0.0, 0, std::vector<int>{}, std::vector<int>{1});
sim.hadamard(1, std::vector<int>{}, std::vector<int>{});
sim.gate_u1(0.0, 0.0, 0.7853981633974483, 0.0, 0, std::vector<int>{}, std::vector<int>{2});
sim.gate_u1(0.0, 0.0, 1.5707963267948966, 0.0, 1, std::vector<int>{}, std::vector<int>{2});
sim.hadamard(2, std::vector<int>{}, std::vector<int>{});
sim.gate_u1(0.0, 0.0, 0.39269908169872414, 0.0, 0, std::vector<int>{}, std::vector<int>{3});
sim.gate_u1(0.0, 0.0, 0.7853981633974483, 0.0, 1, std::vector<int>{}, std::vector<int>{3});
sim.gate_u1(0.0, 0.0, 1.5707963267948966, 0.0, 2, std::vector<int>{}, std::vector<int>{3});
sim.hadamard(3, std::vector<int>{}, std::vector<int>{});
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
creg[2] = sim.measure(2);
creg[3] = sim.measure(3);
