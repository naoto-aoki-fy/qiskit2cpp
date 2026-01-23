sim.set_num_qubits(3);
std::vector<int> creg(3);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_u3(0.3, 0.2, 0.1, 0.0, 0, std::vector<int>{}, std::vector<int>{});
sim.hadamard(1, std::vector<int>{}, std::vector<int>{});
sim.gate_x(2, std::vector<int>{}, std::vector<int>{1});
// Unsupported operation: barrier
sim.gate_x(1, std::vector<int>{}, std::vector<int>{0});
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
if (creg[0] == 1) {
    sim.gate_z(2, std::vector<int>{}, std::vector<int>{});
}
if (creg[1] == 1) {
    sim.gate_x(2, std::vector<int>{}, std::vector<int>{});
}
creg[2] = sim.measure(2);
