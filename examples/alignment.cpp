sim.set_num_qubits(3);
// Unsupported operation: barrier
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0});
// Unsupported operation: delay
sim.gate_u3(0.7853981633974483, 0.0, 1.5707963267948966, 0.0, 2, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: delay
// Unsupported operation: barrier
