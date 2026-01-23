sim.set_num_qubits(10);
std::vector<int> creg(5);
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
sim.gate_x(1, std::vector<int>{}, std::vector<int>{});
sim.gate_x(5, std::vector<int>{}, std::vector<int>{});
sim.gate_x(6, std::vector<int>{}, std::vector<int>{});
sim.gate_x(7, std::vector<int>{}, std::vector<int>{});
sim.gate_x(8, std::vector<int>{}, std::vector<int>{});
sim.gate_x(5, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(0, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0, 5});
sim.gate_x(6, std::vector<int>{}, std::vector<int>{2});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{2});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{1, 6});
sim.gate_x(7, std::vector<int>{}, std::vector<int>{3});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{3});
sim.gate_x(3, std::vector<int>{}, std::vector<int>{2, 7});
sim.gate_x(8, std::vector<int>{}, std::vector<int>{4});
sim.gate_x(3, std::vector<int>{}, std::vector<int>{4});
sim.gate_x(4, std::vector<int>{}, std::vector<int>{3, 8});
sim.gate_x(9, std::vector<int>{}, std::vector<int>{4});
sim.gate_x(4, std::vector<int>{}, std::vector<int>{3, 8});
sim.gate_x(3, std::vector<int>{}, std::vector<int>{4});
sim.gate_x(8, std::vector<int>{}, std::vector<int>{3});
sim.gate_x(3, std::vector<int>{}, std::vector<int>{2, 7});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{3});
sim.gate_x(7, std::vector<int>{}, std::vector<int>{2});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{1, 6});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{2});
sim.gate_x(6, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0, 5});
sim.gate_x(0, std::vector<int>{}, std::vector<int>{1});
sim.gate_x(5, std::vector<int>{}, std::vector<int>{0});
creg[0] = sim.measure(5);
creg[1] = sim.measure(6);
creg[2] = sim.measure(7);
creg[3] = sim.measure(8);
creg[4] = sim.measure(9);
