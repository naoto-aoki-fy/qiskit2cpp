sim.set_num_qubits(6);
std::vector<int> creg(3);
sim.gate_rz(0.7853981633974483, 3, {}, {});
sim.gate_rz(0.7853981633974483, 4, {}, {});
sim.gate_rz(0.7853981633974483, 5, {}, {});
sim.gate_x(3, {}, {0});
sim.gate_x(4, {}, {1});
sim.gate_x(5, {}, {2});
creg[0] = sim.measure(3);
creg[1] = sim.measure(4);
creg[2] = sim.measure(5);
if (creg[0] == 1) {
    sim.gate_z(0, {}, {});
    sim.gate_z(1, {}, {});
    sim.gate_z(2, {}, {});
}
