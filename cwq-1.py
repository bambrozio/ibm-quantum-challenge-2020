# Coding with Qiskit.
## Jin-Sung Kim, PhD.
# Research Staff Member, IBM Quantum.
# YouTube playlist: https://www.youtube.com/playlist?list=PLOFEBzvs-VvrhKYASly1BXo1AdPyoCsor

#%%
# Youtube video 2: https://www.youtube.com/watch?v=iMCphGJWVSE&list=PLOFEBzvs-VvrhKYASly1BXo1AdPyoCsor&index=2
# Writing My First Quantum Algorithm — Programming on Quantum Computers — Coding with Qiskit S2E2
import qiskit.quantum_info as qi 
from qiskit.circuit.library import FourierChecking
from qiskit.visualization import plot_histogram
# %%
f = [1, -1, -1, -1]
g = [1, 1, -1, -1]
# %%
circ = FourierChecking(f=f, g=g)
circ.draw()
# %%
zero = qi.Statevector.from_label('00')
sv = zero.evolve(circ)
probs = sv.probabilities_dict()
plot_histogram(probs)

# %%
# Youtube video 3: https://www.youtube.com/watch?v=0RPFWZj7Jm0&list=PLOFEBzvs-VvrhKYASly1BXo1AdPyoCsor&index=3
# Grovers Algorithm — Programming on Quantum Computers — Coding with Qiskit S2E3
my_list = [1, 3, 5, 2, 4, 9, 5, 8, 0, 7, 6]
# %%
def the_oracle(my_input):
    winner = 7
    if my_input is winner:
        response = True
    else:
        response = False
    return response
# %%
# Classical computing: O(N).
for index, trial_number in enumerate(my_list):
    if the_oracle(trial_number) is True:
        print(f"Winner found at index {index}")
        print(f"{index+1} calls to the Oracle used.")
# %%
from qiskit import *
import matplotlib.pyplot as pltimport 
import numpy as np
# %%
# Quantum computing O(sqrd(N))
# define the oracle circuit:
oracle = QuantumCircuit(2, name='oracle')
oracle.cz(0,1)
oracle.to_gate()
oracle.draw()
# %%
backend = Aer.get_backend('statevector_simulator')
grover_circ = QuantumCircuit(2,2)
grover_circ.h([0,1])
grover_circ.append(oracle, [0,1])
grover_circ.draw()
# %%
job = execute(grover_circ, backend)
result = job.result()
# %%
sv = result.get_statevector()
np.around(sv, 2)
# %%
reflection = QuantumCircuit(2, name='reflection')
reflection.h([0,1])
reflection.z([0,1])
reflection.cz(0,1)
reflection.h([0,1])
reflection.to_gate()
# %%
reflection.draw()
# %%
backend = Aer.get_backend('qasm_simulator')
grover_circ = QuantumCircuit(2, 2)
grover_circ.h([0,1])
grover_circ.append(oracle, [0,1])
grover_circ.append(reflection, [0,1])
grover_circ.measure([0,1], [0,1])
# %%
grover_circ.draw()
# %%
job = execute(grover_circ, backend, shots=1)
result = job.result()
result.get_counts()

# %%
# Youtube video 4: https://www.youtube.com/watch?v=Z-A6G0WVI9w&list=PLOFEBzvs-VvrhKYASly1BXo1AdPyoCsor&index=4
# The Variational Quantum Eigensolver — Programming on Quantum Computers — Coding with Qiskit S2E4
# Chemistry simulation
import numpy as np 
import pylab 
import copy
from qiskit import BasicAer 
from qiskit.aqua import aqua_globals, QuantumInstance
from qiskit.aqua.algorithms import NumPyMinimumEigensolver, VQE 
from qiskit.aqua.components.optimizers import SLSQP 
from qiskit.chemistry.components.initial_states import HartreeFock
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.drivers import PySCFDriver 
from qiskit.chemistry.core import Hamiltonian, QubitMappingType
# %%
molecule = 'H .0 .0 -{0}; Li .0 .0 {0}'
distances = np.arange(0.5, 4.25, 0.25)
vqe_energies = []
hf_energies = []
exact_energies = []
# %%
for i, d in enumerate(distances):
    print('step', i)

    # set up experiment:
    driver = PySCFDriver(molecule.format(d/2), basis='sto3g')
    qmolecule = driver.run()
    operator = Hamiltonian(qubit_mapping=QubitMappingType.PARITY,
                           two_qubit_reduction=True, 
                           freeze_core=True,
                           orbital_reduction=[-3, -2])
    qubit_op, aux_ops = operator.run(qmolecule)

    # exact classical result
    exact_result = NumPyMinimumEigensolver(qubit_op, aux_operators=aux_ops)
    exact_result = operator.process_algorithm_result(exact_result)

    # VQE
    optimzer = SLSQP(maxiter=1000)
    initial_state = HartreeFock(operator.molecule_info['num_orbitals'],
                                 operator.molecule_info['num_particles'],
                                 qubit_mapping=operator._qubit_mapping,
                                 two_qubit_reduction=operator._two_qubit_reduction)
    var_form = UCCSD(num_orbitals=operator.molecule_info['num_orbitals'],
                     num_particles=operator.molecule_info['num_particles'],
                     initial_state=initial_state,
                     qubit_mapping=operator._qubit_mapping,
                     two_qubit_reduction=operator._two_qubit_reduction)
    algo = VQE(qubit_op, var_form, optimzer, aux_operators=aux_ops)

    vqe_result = algo.run(QuantumInstance(BasicAer.get_backend('statevector_simulator'))
    vqe_result = operator.process_algorithm_result(vqe_result)

    exact_energies.append(exact_result.energy)
    vqe_energies.append(vqe_result.energy)
    hf_energies.append(vqe_result.hartree_fock_energy)

# TODO: Fix the error. Requested help at: #qiskitters: https://qiskit.slack.com/archives/C9YTUV077/p1604862094095100
# for i, d in enumerate(distances):...
#   File "<ipython-input-29-b9786e9f45d1>", line 31
#     vqe_result = operator.process_algorithm_result(vqe_result)
#     ^
# SyntaxError: invalid syntax
    
# %%
pylab.plot(distances, hf_energies, label='Hartree-Fock')
pylab.plot(distances, vqe_energies, 'o', label='VQE')
pylab.plot(distances, exact_energies, 'r', label='Exact')

pylab.xlabel('Interatomic distance')
pylab.ylabel('Energy')
pylab.title('LiH Ground State Energy')
pylab.legend(loc='upper right')
# %%
