"""Demonstrate quantum teleportation."""
from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


circuit = QuantumCircuit(3, 3)

#  Create entangled pair
circuit.h(1)
circuit.cx(1, 2)

circuit.barrier(range(3))


#  Create payload
circuit.h(0)
circuit.p(pi / 4, 0)
circuit.h(0)
circuit.barrier(range(3))

#  Send payload
circuit.cx(0, 1)
circuit.h(0)

circuit.measure(range(2), range(2))

circuit.barrier(range(3))

circuit.x(2).c_if(1, 1)
circuit.p(pi, 2).c_if(0, 1)

#  Verify - Bob's quit should always be 0
circuit.h(2)
circuit.p(-pi / 4, 2)
circuit.h(2)

circuit.measure(2, 2)

# circuit.draw('mpl', filename='debug.png')


simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)

