"""Demonstrate the swap test."""
from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def output(circuit):
    circuit.measure(range(circuit.num_qubits), range(circuit.num_qubits))

    simulator = AerSimulator()

    compiled_circuit = transpile(circuit, simulator)

    job = simulator.run(compiled_circuit, shots=1000)

    result = job.result()
    counts = result.get_counts(compiled_circuit)

    print(counts)
    
def create(number_of_qbits):
    return QuantumCircuit(number_of_qbits, number_of_qbits)
    

circuit = create(2)

theta = pi/2

circuit.p(theta/2, 1)
circuit.cnot(0, 1)
circuit.p(-theta/2, 1)
circuit.cnot(0, 1)
circuit.p(theta/2, 0)


output(circuit)


