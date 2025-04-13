from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import QuantumCircuit
import time

# Azure Quantum Workspace credentials
workspace = Workspace(
    subscription_id="",
    resource_group="AzureQuantum",
    name="",
    location="northeurope"
)

# Connect to Azure Quantum
provider = AzureQuantumProvider(workspace)

# Select backend
backend = provider.get_backend("ionq.qpu.aria-1")

# Function to build a delay-encoded quantum circuit
def build_mass_delay_circuit(num_qubits, delay_depth):
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))  # Superposition
    for _ in range(delay_depth):
        for i in range(num_qubits):
            qc.id(i)  # Identity gates simulate computational delay
    qc.measure_all()
    return qc

# Function to run the latency-based experiment
def run_latency_experiment(mass_factor, delay_scale=500, shots=1024):
    print(f"\n▶️ Submitting job with mass_factor = {mass_factor}...")
    delay_depth = int(mass_factor * delay_scale)
    qc = build_mass_delay_circuit(num_qubits=3, delay_depth=delay_depth)

    start_time = time.time()
    job = backend.run(qc, shots=shots)
    result = job.result()
    end_time = time.time()

    exec_time = end_time - start_time
    counts = result.get_counts()

    print(f"✅ Done: Time = {exec_time:.2f}s, Sample = {counts}")
    return mass_factor, exec_time, counts

# Main test execution
if __name__ == "__main__":
    for mass in [0.5, 1.0, 1.5]:
        run_latency_experiment(mass_factor=mass)
