sim.set_num_qubits(5);
auto pack_bits = [](const std::vector<int>& creg, const std::vector<int>& bits) {
    int value = 0;
    for (size_t i = 0; i < bits.size(); ++i) {
        value |= (creg[bits[i]] & 1) << i;
    }
    return value;
};
std::vector<int> creg(5);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_x(0, {}, {});
// Unsupported operation: barrier
sim.gate_x(3, {}, {0});
sim.gate_x(3, {}, {1});
sim.gate_x(4, {}, {1});
sim.gate_x(4, {}, {2});
creg[3] = sim.measure(3);
creg[4] = sim.measure(4);
if (pack_bits(creg, std::vector<int>{3, 4}) == 1) {
    sim.gate_x(0, {}, {});
}
if (pack_bits(creg, std::vector<int>{3, 4}) == 2) {
    sim.gate_x(2, {}, {});
}
if (pack_bits(creg, std::vector<int>{3, 4}) == 3) {
    sim.gate_x(1, {}, {});
}
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
creg[2] = sim.measure(2);
