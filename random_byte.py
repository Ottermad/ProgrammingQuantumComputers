"""Generates a random byte."""
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator


circuit = QuantumCircuit(8, 8)
circuit.h(range(8))
circuit.measure(range(8), range(8))

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

plot_histogram(counts)
