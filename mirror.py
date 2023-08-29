"""Apply mirror subroutine to flip phase."""
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library.standard_gates import PhaseGate
from qiskit_aer import AerSimulator

register = QuantumRegister(4)
circuit = QuantumCircuit(register)

# Prep
for bit in register:
    circuit.h(bit)

# Flip
number_to_flip = 9


def apply_nots():
    binary_string = format(number_to_flip, '0' + str(register.size) + 'b')
    for i, x in enumerate(reversed(binary_string)):
        if x == '0':
            circuit.x(i)


apply_nots()
circuit.append(PhaseGate(pi).control(register.size-1), register)
apply_nots()

circuit.barrier(register)

# Mirror
for bit in register:
    circuit.h(bit)
    circuit.x(bit)

circuit.append(PhaseGate(pi).control(register.size-1), register)

for bit in register:
    circuit.x(bit)
    circuit.h(bit)

circuit.draw('mpl', filename='debug.png')
circuit.measure_all()

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
