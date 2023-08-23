"""Remote control randomness."""
from math import pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def output(circuit):
    circuit.measure(range(circuit.num_qubits), range(circuit.num_qubits))

    simulator = AerSimulator()

    compiled_circuit = transpile(circuit, simulator)

    job = simulator.run(compiled_circuit, shots=1000)

    result = job.result()
    counts = result.get_counts(compiled_circuit)

    print(counts)
    
def create(number_of_qbits):
    return QuantumCircuit(number_of_qbits, number_of_qbits)
    

circuit = create(2)

circuit.h(0)

circuit.h(1)
circuit.p(pi/4, 1)
circuit.h(1)

circuit.cnot(0, 1)

output(circuit)


