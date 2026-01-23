sim.set_num_qubits(2);
sim.gate_u3(0.0, 0.0, 0.7853981633974483, 0.0, 0, std::vector<int>{}, std::vector<int>{});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0});
sim.gate_u3(0.0, 0.0, -0.7853981633974483, 0.0, 1, std::vector<int>{}, std::vector<int>{});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0});
sim.gate_u3(0.0, 0.0, 0.7853981633974483, 0.0, 1, std::vector<int>{}, std::vector<int>{});
