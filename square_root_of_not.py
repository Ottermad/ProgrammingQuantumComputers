"""Demonstrates the square root of NOT gate."""
from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


circuit = QuantumCircuit(2, 2)

# Square root of not on first qbit
circuit.h(0)
circuit.rz(pi / 2, 0)
circuit.h(0)

# Square root of not on first qbit again
circuit.h(0)
circuit.rz(pi / 2, 0)
circuit.h(0)

# Apply not gate / x gate on second qbit
circuit.x(1)

circuit.measure(range(2), range(2))

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
