from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

# Qubits: Alice's message, Alice's shared half, Bob's shared half
qr = QuantumRegister(3, name="q")
crz = ClassicalRegister(1, name="crz") # Alice's Z measurement
crx = ClassicalRegister(1, name="crx") # Alice's X measurement
result_cr = ClassicalRegister(1, name="result")

qc = QuantumCircuit(qr, crz, crx, result_cr)

# 1. Prepare a state to teleport (e.g., Ry rotation)
qc.ry(np.pi/3, 0)
qc.barrier()

# 2. Create shared Bell pair between Alice (q1) and Bob (q2)
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# 3. Alice performs Bell-basis measurement on her qubits (q0, q1)
qc.cx(0, 1)
qc.h(0)
qc.measure(0, crz)
qc.measure(1, crx)
qc.barrier()

# 4. Bob applies conditional Pauli gates based on Alice's classical bits
with qc.if_test((crx, 1)):
    qc.x(2)
with qc.if_test((crz, 1)):
    qc.z(2)

# Verify by disentangling the original Ry rotation on Bob's qubit
qc.ry(-np.pi/3, 2)
qc.measure(2, result_cr)

sim = AerSimulator()
res = sim.run(qc, shots=1024).result().get_counts()
print("Teleportation Result (should be highly biased to 0):", res)