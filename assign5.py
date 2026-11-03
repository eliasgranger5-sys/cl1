from qiskit import QuantumCircuit
import numpy as np

def build_qft_5_qubit():
    qc = QuantumCircuit(5)
    
    # Iteratively apply H and controlled-phase gates
    for i in range(5):
        qc.h(i)
        for j in range(i + 1, 5):
            # The phase rotation relies on the distance between the qubits
            angle = np.pi / (2 ** (j - i))
            qc.cp(angle, j, i)
        qc.barrier()
        
    # Swap the qubits to match the required QFT output ordering
    qc.swap(0, 4)
    qc.swap(1, 3)
    
    return qc

qft_circuit = build_qft_5_qubit()
print("5-Qubit QFT Depth:", qft_circuit.depth())
print(qft_circuit.draw(output='text', scale=0.7))