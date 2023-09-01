"""Illustrate phase logic operations."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


register1 = QuantumRegister(3)
circuit = QuantumCircuit(register1, register2)


def phase_not(circuit, index): 
    circuit.x(index)
    circuit.phase(pi, index)
    circuit.x(index)


def phase_or(circuit, index1, index2): 
    circuit.phase(pi, index1)
    circuit.cz(index1, index2)
    circuit.phase(pi, index2)


def phase_and(circuit, index1, index2): 
    circuit.cz(index1, index2)

circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
