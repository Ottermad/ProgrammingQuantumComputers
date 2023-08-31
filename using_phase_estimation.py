import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import PhaseEstimation
from qiskit_aer import AerSimulator

input_register = QuantumRegister(1)
output_register = QuantumRegister(4)
classical_output = ClassicalRegister(output_register.size)

circuit = QuantumCircuit(input_register, output_register, classical_output)

circuit.ry(-3*math.pi/4, input_register)

hadamardCircuit = QuantumCircuit(1)
hadamardCircuit.h(0)

circuit.append(PhaseEstimation(num_evaluation_qubits=output_register.size, unitary=hadamardCircuit).to_instruction(), list(reversed([*output_register]))+[ *input_register])

circuit.decompose(reps=2).draw('mpl', filename='debug.png')

circuit.measure(output_register, classical_output)

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
