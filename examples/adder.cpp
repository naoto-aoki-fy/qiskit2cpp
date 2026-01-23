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
sim.gate_x(1, {}, {});
sim.gate_x(5, {}, {});
sim.gate_x(6, {}, {});
sim.gate_x(7, {}, {});
sim.gate_x(8, {}, {});
sim.gate_x(5, {}, {1});
sim.gate_x(0, {}, {1});
sim.gate_x(1, {}, {0, 5});
sim.gate_x(6, {}, {2});
sim.gate_x(1, {}, {2});
sim.gate_x(2, {}, {1, 6});
sim.gate_x(7, {}, {3});
sim.gate_x(2, {}, {3});
sim.gate_x(3, {}, {2, 7});
sim.gate_x(8, {}, {4});
sim.gate_x(3, {}, {4});
sim.gate_x(4, {}, {3, 8});
sim.gate_x(9, {}, {4});
sim.gate_x(4, {}, {3, 8});
sim.gate_x(3, {}, {4});
sim.gate_x(8, {}, {3});
sim.gate_x(3, {}, {2, 7});
sim.gate_x(2, {}, {3});
sim.gate_x(7, {}, {2});
sim.gate_x(2, {}, {1, 6});
sim.gate_x(1, {}, {2});
sim.gate_x(6, {}, {1});
sim.gate_x(1, {}, {0, 5});
sim.gate_x(0, {}, {1});
sim.gate_x(5, {}, {0});
creg[0] = sim.measure(5);
creg[1] = sim.measure(6);
creg[2] = sim.measure(7);
creg[3] = sim.measure(8);
creg[4] = sim.measure(9);
