"""Demonstrate the swap test."""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


circuit = QuantumCircuit(3, 3)

circuit.x(0)
circuit.x(1)

circuit.h(2)
circuit.cswap(2, 0, 1)
circuit.h(2)
circuit.x(2)

circuit.measure(range(3), range(3))

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
