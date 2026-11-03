from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

q_data = QuantumRegister(3, 'data')
q_ancilla = QuantumRegister(2, 'ancilla')
c_syndrome = ClassicalRegister(2, 'syndrome')
c_out = ClassicalRegister(3, 'output')

qc = QuantumCircuit(q_data, q_ancilla, c_syndrome, c_out)

qc.cx(q_data[0], q_data[1])
qc.cx(q_data[0], q_data[2])
qc.barrier()

qc.x(q_data[1])
qc.barrier()

qc.cx(q_data[0], q_ancilla[0])
qc.cx(q_data[1], q_ancilla[0])

qc.cx(q_data[1], q_ancilla[1])
qc.cx(q_data[2], q_ancilla[1])

qc.measure(q_ancilla, c_syndrome)
qc.barrier()

with qc.if_test((c_syndrome, 1)): 
    qc.x(q_data[0])
with qc.if_test((c_syndrome, 3)): 
    qc.x(q_data[1])
with qc.if_test((c_syndrome, 2)): 
    qc.x(q_data[2])

qc.measure(q_data, c_out)

sim = AerSimulator()
result = sim.run(qc, shots=1000).result().get_counts()
print("Error Correction Results (Data | Syndrome):", result)