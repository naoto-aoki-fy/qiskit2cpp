sim.set_num_qubits(4);
// Unsupported operation: delay
sim.gate_x(0, {}, {});
// Unsupported operation: delay
sim.gate_y(0, {}, {});
// Unsupported operation: delay
sim.gate_x(0, {}, {});
// Unsupported operation: delay
sim.gate_y(0, {}, {});
// Unsupported operation: delay
sim.gate_x(3, {}, {2});
sim.gate_x(2, {}, {1});
sim.gate_u3(0.0, 0.0, 0.0, 0.0, 3, {}, {});
