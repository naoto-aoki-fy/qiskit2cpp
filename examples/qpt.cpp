sim.set_num_qubits(1);
std::vector<int> creg(1);
// Unsupported operation: reset
// Unsupported operation: pre
// Unsupported operation: barrier
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: barrier
// Unsupported operation: post
creg[0] = sim.measure(0);
