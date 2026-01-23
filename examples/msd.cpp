sim.set_num_qubits(7);
std::vector<int> creg(5);
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
// Unsupported operation: reset
sim.gate_ry(0.7853981633974483, 0, {}, {});
sim.gate_ry(0.7853981633974483, 1, {}, {});
sim.gate_ry(0.7853981633974483, 2, {}, {});
sim.gate_ry(0.7853981633974483, 3, {}, {});
sim.gate_ry(0.7853981633974483, 4, {}, {});
sim.gate_x(5, {}, {0});
sim.gate_x(6, {}, {1});
sim.gate_z(2, {}, {5});
sim.gate_z(3, {}, {6});
creg[0] = sim.measure(0);
creg[1] = sim.measure(1);
creg[2] = sim.measure(2);
creg[3] = sim.measure(3);
creg[4] = sim.measure(4);
