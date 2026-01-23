sim.set_num_qubits(17);
std::vector<int> creg(17);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(9, std::vector<int>{}, std::vector<int>{});
sim.hadamard(10, std::vector<int>{}, std::vector<int>{});
sim.hadamard(11, std::vector<int>{}, std::vector<int>{});
sim.hadamard(12, std::vector<int>{}, std::vector<int>{});
sim.hadamard(13, std::vector<int>{}, std::vector<int>{});
sim.hadamard(14, std::vector<int>{}, std::vector<int>{});
sim.hadamard(15, std::vector<int>{}, std::vector<int>{});
sim.hadamard(16, std::vector<int>{}, std::vector<int>{});
sim.gate_x(9, std::vector<int>{}, std::vector<int>{0});
sim.gate_x(9, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(10, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(10, std::vector<int>{}, std::vector<int>{2});
creg[0] = sim.measure(9);
creg[1] = sim.measure(10);
creg[2] = sim.measure(11);
creg[3] = sim.measure(12);
creg[4] = sim.measure(13);
creg[5] = sim.measure(14);
creg[6] = sim.measure(15);
creg[7] = sim.measure(16);
creg[8] = sim.measure(0);
creg[9] = sim.measure(1);
creg[10] = sim.measure(2);
creg[11] = sim.measure(3);
creg[12] = sim.measure(4);
creg[13] = sim.measure(5);
creg[14] = sim.measure(6);
creg[15] = sim.measure(7);
creg[16] = sim.measure(8);
