sim.set_num_qubits(4);
// Unsupported operation: delay
sim.gate_x(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: delay
sim.gate_y(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: delay
sim.gate_x(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: delay
sim.gate_y(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: delay
sim.gate_x(3, std::vector<int>{}, std::vector<int>{2});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{1});
sim.gate_u3(0.0, 0.0, 0.0, 0.0, 3, std::vector<int>{}, std::vector<int>{});
