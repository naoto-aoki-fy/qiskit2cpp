sim.set_num_qubits(4);
auto pack_bits = [](const std::vector<int>& creg, const std::vector<int>& bits) {
    int value = 0;
    for (size_t i = 0; i < bits.size(); ++i) {
        value |= (creg[bits[i]] & 1) << i;
    }
    return value;
};
std::vector<int> creg(4);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
sim.hadamard(1, std::vector<int>{}, std::vector<int>{});
sim.hadamard(2, std::vector<int>{}, std::vector<int>{});
sim.hadamard(3, std::vector<int>{}, std::vector<int>{});
// Unsupported operation: barrier
sim.hadamard(0, std::vector<int>{}, std::vector<int>{});
creg[0] = sim.measure(0);
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 1) {
    sim.gate_rz(1.5707963267948966, 1, std::vector<int>{}, std::vector<int>{});
}
sim.hadamard(1, std::vector<int>{}, std::vector<int>{});
creg[1] = sim.measure(1);
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 1) {
    sim.gate_rz(0.7853981633974483, 2, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 2) {
    sim.gate_rz(1.5707963267948966, 2, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 3) {
    sim.gate_rz(2.356194490192345, 2, std::vector<int>{}, std::vector<int>{});
}
sim.hadamard(2, std::vector<int>{}, std::vector<int>{});
creg[2] = sim.measure(2);
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 1) {
    sim.gate_rz(0.39269908169872414, 3, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 2) {
    sim.gate_rz(0.7853981633974483, 3, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 3) {
    sim.gate_rz(1.1780972450961724, 3, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 4) {
    sim.gate_rz(1.5707963267948966, 3, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 5) {
    sim.gate_rz(1.9634954084936207, 3, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 6) {
    sim.gate_rz(2.356194490192345, 3, std::vector<int>{}, std::vector<int>{});
}
if (pack_bits(creg, std::vector<int>{0, 1, 2, 3}) == 7) {
    sim.gate_rz(2.748893571891069, 3, std::vector<int>{}, std::vector<int>{});
}
sim.hadamard(3, std::vector<int>{}, std::vector<int>{});
creg[3] = sim.measure(3);
