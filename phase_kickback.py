"""Creates a phase kickback."""
from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


circuit = QuantumCircuit(3, 3)

circuit.x(2) # Set qubit 3 to 1

circuit.h(0)
circuit.h(1)

circuit.cp(pi/4, 0, 2)

circuit.cp(pi/2, 1, 2)

circuit.measure(range(3), range(3))

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
