"""Illustrate solving kittens and tigers problem."""
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library.standard_gates import ZGate
from qiskit_aer import AerSimulator


def bit_or(q1, q2, out):
    circuit.x(q1)
    circuit.x(q2)
    circuit.ccx(q1, q2, out)
    circuit.x(q1)
    circuit.x(q2)
    circuit.x(out)


def inv_bit_or(q1, q2, out):
    circuit.x(q1)
    circuit.x(q2)
    circuit.x(out)
    circuit.ccx(q1, q2, out)
    circuit.x(q1)
    circuit.x(q2)


def phase_and(qubits):
    circuit.append(ZGate().control(qubits.size - 1), qubits)


reg = QuantumRegister(3)
anc = QuantumRegister(4)

circuit = QuantumCircuit(reg, anc)

circuit.h(reg)

# Clause 1
bit_or(reg[0], reg[1], anc[0])
circuit.barrier()

# Clause 2
circuit.x(reg[0])
bit_or(reg[0], reg[1], anc[1])
circuit.x(reg[0])
circuit.barrier()

# Clause 3
circuit.x(reg[1])
circuit.x(reg[2])
bit_or(reg[1], reg[2], anc[2])
circuit.x(reg[1])
circuit.x(reg[2])
circuit.barrier()

# Clause 4
bit_or(reg[0], reg[2], anc[3])
circuit.barrier()

# Flip
phase_and(anc)
circuit.barrier()

# Inversions
inv_bit_or(reg[0], reg[2], anc[3])
circuit.barrier()

circuit.x(reg[1])
circuit.x(reg[2])
inv_bit_or(reg[1], reg[2], anc[2])
circuit.x(reg[1])
circuit.x(reg[2])
circuit.barrier()

inv_bit_or(reg[0], reg[1], anc[0])
circuit.barrier()

circuit.x(reg[0])
inv_bit_or(reg[0], reg[1], anc[1])
circuit.x(reg[0])
circuit.barrier()

# AA
for bit in reg:
    circuit.h(bit)
    circuit.x(bit)

circuit.append(ZGate().control(reg.size-1), reg)

for bit in reg:
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
