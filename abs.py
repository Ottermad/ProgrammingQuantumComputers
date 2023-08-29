"""Uses scratch bits to implement sbs."""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


register = QuantumRegister(3)
classical_register = ClassicalRegister(3)
scratch = QuantumRegister(1)
circuit = QuantumCircuit(register, scratch, classical_register)


circuit.x(register)

circuit.cx(register[-1], scratch)
for n in range(0, register.size):
    circuit.cx(scratch, register[n])


def controlled_increment_register(circuit, register, control_bit):
    for i in range(0, len(register))[::-1]:
        gate = XGate().control(i+1)

        circuit.append(gate, [control_bit] + register[:i] + [register[i]], [])


controlled_increment_register(circuit, register, scratch[0])

circuit.measure(register, classical_register)

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
