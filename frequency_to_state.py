"""Get QFT of a simple register."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

register = QuantumRegister(4)
circuit = QuantumCircuit(register)

circuit.x(register[0])
circuit.x(register[1])
circuit.barrier(register)

circuit.append(QFT(num_qubits=register.size).to_instruction(), register)


circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
