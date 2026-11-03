from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_16bit_rng():
    qc = QuantumCircuit(16, 16)
    
    for i in range(16):
        qc.h(i)
        
    qc.measure(range(16), range(16))
    
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    
    result = job.result().get_counts()
    return list(result.keys())[0]

print("16-bit Quantum Random Number:", generate_16bit_rng())