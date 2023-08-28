"""Illustrate conditional increment operation."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


register1 = QuantumRegister(3)
register2 = QuantumRegister(3)
circuit = QuantumCircuit(register1, register2)

#  Create inital sate
circuit.x(register1[0])
circuit.h(register1[2])


circuit.x(register2[0])
circuit.h(register2[1])
circuit.p(pi/4, register2[1])


# Do addition
def increment_register(circuit, register):
    for i in range(0, len(register))[::-1]:
        gate = XGate()
        if i != 0:
            gate = gate.control(i)

        circuit.append(gate, register[:i] + [register[i]], [])

def controlled_increment_register(circuit, register, control_bit):
    for i in range(0, len(register))[::-1]:
        gate = XGate().control(i+1)

        circuit.append(gate, [control_bit] + register[:i] + [register[i]], [])



def decrement_register(circuit, register):
    for i in range(0, len(register)):
        gate = XGate()
        if i != 0:
            gate = gate.control(i)

        circuit.append(gate, register[:i] + [register[i]], [])


for i in range(3):
    increment_register(circuit, register1)

controlled_increment_register(circuit, register2, register1[2])

for i in range(3):
    decrement_register(circuit, register1)

circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
