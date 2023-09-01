"""Illustrate solving kittens and tigers problem."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


boxes = QuantumRegister(2)
note = QuantumRegister(1)
anc = QuantumRegister(1)

circuit = QuantumCircuit(boxes, note, anc)

circuit.h(boxes)

# A OR B
circuit.x(boxes)
circuit.ccx(*boxes, note)
circuit.x(boxes)
circuit.x(note)
circuit.barrier()

# The other box contains a tiger
circuit.x(boxes[0])
circuit.barrier()

# Phase logic XNOR
circuit.x(anc)
circuit.h(anc)
circuit.cx(note, anc)
circuit.cx(boxes[0], anc)
circuit.x(anc)
circuit.h(anc)
circuit.x(anc)
circuit.barrier()

# Uncompute
circuit.x(boxes[0])
circuit.x(boxes)
circuit.x(note)
circuit.ccx(*boxes, note)
circuit.x(boxes)
circuit.barrier()

# Mirror
circuit.h(boxes)
circuit.x(boxes)
circuit.cz(*boxes)
circuit.x(boxes)
circuit.h(boxes)


circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
