"""Illustrate increment operation."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


register1 = QuantumRegister(4)
register2 = QuantumRegister(4)
circuit = QuantumCircuit(register1, register2)

#  Create inital sate
circuit.x(register1[0])
circuit.x(register2[2])


# Do addition
def increment_register(circuit, register):
    for i in range(0, len(register))[::-1]:
        gate = XGate()
        if i != 0:
            gate = gate.control(i)

        circuit.append(gate, register[:i] + [register[i]], [])


def decrement_register(circuit, register):
    for i in range(0, len(register)):
        gate = XGate()
        if i != 0:
            gate = gate.control(i)

        circuit.append(gate, register[:i] + [register[i]], [])

increment_register(circuit, register1)
decrement_register(circuit, register2)

circuit.measure_all()

circuit.draw('mpl', filename='increment.png')

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
