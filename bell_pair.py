"""Creates a Bell Pair."""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


circuit = QuantumCircuit(2, 2)

circuit.h(0)
circuit.cx(0, 1)

circuit.measure(range(2), range(2))

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
