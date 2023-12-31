"""Use QFT to distinguish between signals."""
from math import pi
import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT, CU1Gate
from qiskit_aer import AerSimulator

register = QuantumRegister(4)
circuit = QuantumCircuit(register)


def signal_a():
    circuit.p(pi,register[0])


def signal_b():
    circuit.p(pi/2, register[0])
    circuit.p(pi, register[1])


def signal_c():
    circuit.p(math.radians(45), register[0])
    circuit.p(math.radians(90), register[1])
    circuit.p(math.radians(180), register[2])


for qbit in register:
    circuit.h(qbit)
signal_a()
circuit.barrier(register)


circuit.append(QFT(num_qubits=register.size, inverse=True).to_instruction(), register)


circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
