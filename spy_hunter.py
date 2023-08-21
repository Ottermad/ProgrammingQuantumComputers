"""Using qbits to detect a spy."""
from numpy import average
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

simulator = AerSimulator()


def value_of_measurement(circuit):
    """Get result as int."""
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(compiled_circuit)

    return int(list(counts.keys())[0])


def random_bit():
    """Randomly generates a bit."""
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    return value_of_measurement(circuit)


def spy_hunter(is_spy):
    """Send a bit and check for spies."""
    # Alice prepares a qbit randomly in one of 0, 1, -, +
    initial_value = random_bit()

    spy_hunter_circuit = QuantumCircuit(1, 1)

    if initial_value == 1:
        spy_hunter_circuit.x(0)

    alice_apply_hadamard = random_bit()

    if alice_apply_hadamard:
        spy_hunter_circuit.h(0)

    if is_spy:
        spy_hunter_circuit.measure(0, 0)
        stolen_data = value_of_measurement(spy_hunter_circuit)
        spy_hunter_circuit = QuantumCircuit(1, 1)
        if stolen_data == 1:
            spy_hunter_circuit.x(0)

    bob_apply_hadamard = random_bit()

    if bob_apply_hadamard:
        spy_hunter_circuit.h(0)

    spy_hunter_circuit.measure(0, 0)

    bobs_result = value_of_measurement(spy_hunter_circuit)

    both_did_op = alice_apply_hadamard and bob_apply_hadamard
    results_match = initial_value != bobs_result

    if both_did_op and (not results_match):
        return True

    return False


caught_on = []
for i in range(0, 10):
    attempt_number = 0

    while True:
        attempt_number += 1
        caught = spy_hunter(True)
        if caught:
            break
    caught_on.append(attempt_number)

print("Max attempts needed", max(caught_on))
print("Mean attempts needed", average(caught_on))
