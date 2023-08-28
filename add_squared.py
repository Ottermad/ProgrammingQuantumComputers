from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import AerSimulator


a = QuantumRegister(4)
b = QuantumRegister(2)
classical_a = ClassicalRegister(4)
circuit = QuantumCircuit(a, b, classical_a)


for n in range(3, -1, -1):
    circuit.append(XGate().control(n+1), [b[0], *a[0:n], a[n]], [])

for i in range(0, 2):
    for n in range(3, 0, -1):
        circuit.append(XGate().control(n+1), [*b, *a[1:n], a[n]], [])
        
for n in range(3, 1, -1):
    circuit.append(XGate().control(n-1), [b[1], *a[2:n], a[n]], [])

circuit.measure(a, classical_a)

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
