"""Uses scratch bits to implement abs then uncompute."""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator

   
def controlled_increment_register(circuit, register, control_bit):
    for i in range(0, len(register))[::-1]:
        gate = XGate().control(i+1)

        circuit.append(gate, [control_bit] + register[:i] + [register[i]], [])

def add_register_b_to_a(circuit, register_a, register_b):
    for bit in register_b:
        for i in range(0, len(register_a))[::-1]:
            gate = XGate()
            gate = gate.control(i+1)
    
            circuit.append(gate, [bit] + register_a[:i] + [register_a[i]], [])


register_a = QuantumRegister(3)
classical_register = ClassicalRegister(3)
scratch = QuantumRegister(1)
circuit = QuantumCircuit(register_a, scratch, classical_register)


circuit.x(register_a)

# Compute abs
def q_abs():
    circuit.cx(register_a[-1], scratch)
    for n in range(0, register_a.size):
        circuit.cx(scratch, register_a[n])
     
    controlled_increment_register(circuit, register_a, scratch[0])

def q_inv_abs():
    
    controlled_increment_register(circuit, register_a, scratch[0])
    for n in range(register_a.size, -1, -1):
        circuit.cx(scratch, register_a[n])
# b += abs(a)


circuit.measure(register_a, classical_register)

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
