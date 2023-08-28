"""Uses scratch bits to implement abs then uncompute."""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


def add_register_b_to_a(circuit, register_a, register_b):
    for bit in register_b:
        for i in range(0, len(register_a))[::-1]:
            gate = XGate()
            gate = gate.control(i+1)
    
            circuit.append(gate, [bit] + register_a[:i] + [register_a[i]], [])


register_a = QuantumRegister(3)
register_b = QuantumRegister(3)

classical_register = ClassicalRegister(3)
circuit = QuantumCircuit(register_a, register_b, classical_register)


circuit.x(register_a[0])
circuit.h(register_a[1])
circuit.x(register_b[0])

add_register_b_to_a(circuit, register_a, register_b)


circuit.measure(register_a, classical_register)

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
