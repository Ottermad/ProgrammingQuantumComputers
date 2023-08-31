import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

input_register = QuantumRegister(1)
output_register = QuantumRegister(4)
classical_output = ClassicalRegister(output_register.size)

circuit = QuantumCircuit(input_register, output_register, classical_output)

circuit.ry(-3 * math.pi / 4, input_register)

hadamardCircuit = QuantumCircuit(1)
hadamardCircuit.h(0)


def phase_estimation(output_register, eigenstate, unitary_circuit):
    circuit.h(output_register)

    controlled_u = unitary_circuit.to_gate().control(1)

    for index, bit in enumerate(output_register):
        for i in range(0, 2**index):
            circuit.append(controlled_u, [bit, *eigenstate])

    circuit.append(
        QFT(num_qubits=output_register.size).to_instruction(), output_register)

phase_estimation(output_register, input_register, hadamardCircuit)

circuit.decompose().draw('mpl', filename='debug.png')

circuit.measure(output_register, classical_output)

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()
counts = result.get_counts(compiled_circuit)

print(counts)
