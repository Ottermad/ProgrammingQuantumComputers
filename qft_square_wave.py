"""Get QFT of a simple register."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

register = QuantumRegister(8)
circuit = QuantumCircuit(register)

circuit.h(register)
circuit.p(pi, register[4])
circuit.barrier(register)

circuit.append(QFT(num_qubits=register.size, inverse=True).to_instruction(), register)


circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
