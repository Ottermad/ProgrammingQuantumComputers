""""Illustrate increment operation."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import AerSimulator


qx = QuantumRegister(4)
qy = QuantumRegister(4)
circuit = QuantumCircuit(qx, qy)

circuit.h(qx)
circuit.h(qy)

circuit.p(pi/2, qx[2:])

circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
