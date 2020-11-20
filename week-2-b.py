# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Clearing the room with a single switch
# *The room Dr. Ryoko needs to cross has a floor made of 3 x 3 tiles. Each tile represents a single qubit.<br/>
# Some of the qubits change from the ground state to the excited state and vice versa. <br/> You notice that there is a pattern - the floor can only be in either one of the four patterns as shown in each of the examples below. <br/>
# To help Dr. Ryoko cross the room safely, you need to find out which board can be cleared with a single switch operation. <br/>*
# %% [markdown]
# # Week2-B: Four-Lights Out
# In this problem, we are dealing with multiple binary data at the same time. 
# We have to determine if each of the given four Lights Out boards are solvable under the given constraints, so let's devise a quantum circuit to solve them all at the same time.
# 
# As an example, let's consider how to find a board that can be cleared with just a single switch operation from the 4 boards given below. The initial state of the 4 boards is given in the following two-dimensional array, where "0" and "1" represent "off" and "on" respectively similar to the previous learning problem:
# 
# lightsout4_ex=\[\[Board 0\],\[Board 1\],\[Board 2\],\[Board 3\]\]

# %%
from IPython.display import Image, display
Image('4lightsout_ex.png')

# %% [markdown]
# ## Answer Strategy
# If only one board is given, this is a decision problem.
# Using the algorithm from the first Lights Out puzzle (2A), you can solve this problem by counting the "1"s in the output.
#  
# If we are given multiple boards, there will be several approaches.
# 1. Iterate the same "one board algorithm" for each board.
# 2. Hold information for multiple boards at the same time and solve the problems in a single run (execute the algorithm once). 
# - For the rest of this document, we discuss how to use the latter approach to solve this type of problem.
# 
# First, how do we keep data for all the boards at the same time?
# 1. Naive data structures:　　9 Qubits/board * 4 boards > 32 qubits (Upper limit of ibm_qasm_simulator).
# 2. Prepare the  superposition state:   $\vert Board 0\rangle + \vert Board 1\rangle + \vert Board 2\rangle + \vert Board 3\rangle$.
#     - The circuit configuration used for state generation is non-trivial.
# 3. *qRAM* is known as one solution. 
#     - **Pros**: Intuitive implementation. 
#     - **Cons**: Computationally expensive. 
# 
# Of course you can devise and adopt other smart ways to do this.
# 
# Here, we will focus on *qRAM* and describe its configuration and implementation.

# %%
from qiskit import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute
provider = IBMQ.load_account()

# %% [markdown]
# ## qRAM: Quantum Random Access Memory
# 
# In classical computers, RAM (Random Access Memory) is a type of volatile memory that has memory addresses $j$ and stores binary data corresponding to each address $D_j$.
# 
# In the case of [qRAM](https://arxiv.org/abs/0708.1879) in a quantum computer, address qubits $a$ have the $N$-addresses as superposition and the corresponding binary data is stored in data qubits $d$ as a state vector.
# \\[
# \sum_{j}\frac{1}{\sqrt{N}}\vert j \rangle_{a}\vert 0 \rangle_{d}\xrightarrow{qRAM}\sum_{j}\frac{1}{\sqrt{N}}\vert j \rangle_{a}\vert D_{j} \rangle_{d}
# \\]　　
# We call the right-hand side state "qRAM" and the corresponding gate operation "qRAM operation".
# 
# Although qRAM operation requires $\mathcal{O}(N\log N)$ gates, it can be used to create superposition states of binary data intuitively.  
# 
# qRAM has previously been applied to various quantum machine learning algorithms such as the HHL algorithm. For this problem, let's apply qRAM to Grover's algorithm.
# %% [markdown]
# ## Example: Find the data from qRAM
# Prepare a qRAM of $n$-addresses in which the numbers $k_0, k_1, .. , k_{n-1}$ are stored in this order.  
# Find the address in which the number $m$ is stored using Grover's algorithm.  
# - $n = 4$
# - $k = [1,2,5,7]$
# - $m = 7$
# 
# ### qRAM operation.
# Here we show a circuit example of qRAM.

# %%
address = QuantumRegister(2)
data = QuantumRegister(3)
c = ClassicalRegister(5)
qc = QuantumCircuit(address,data,c)

# address preparation
qc.h([address[0],address[1]])
qc.barrier()
# address 0 -> data = 1
qc.x([address[0],address[1]])
qc.ccx(address[0],address[1],data[2])
qc.x([address[0],address[1]])
qc.barrier()
# address 1 -> data = 2
qc.x(address[0])
qc.ccx(address[0],address[1],data[1])
qc.x(address[0])
qc.barrier()
# address 2 -> data = 5
qc.x(address[1])
qc.ccx(address[0],address[1],data[2])
qc.ccx(address[0],address[1],data[0])
qc.x(address[1])
qc.barrier()
# address 3 -> data = 7
qc.ccx(address[0],address[1],data[2])
qc.ccx(address[0],address[1],data[1])
qc.ccx(address[0],address[1],data[0])
qc.barrier()


#Check the qRAM　status
qc.measure(address[0:2], c[0:2])
qc.measure(data[0:3], c[2:5])
 
# Reverse the output string.
qc = qc.reverse_bits()

#backend = provider.get_backend('ibmq_qasm_simulator')
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=backend, shots=8000, seed_simulator=12345, backend_options={"fusion_enable":True})
#job = execute(qc, backend=backend, shots=8192)
result = job.result()
count =result.get_counts()
print(count)

qc.draw(output='mpl')

# %% [markdown]
# ### qRAM Data Search
# To perform Grover's algorithm, we invert the sign of the **address qubit** containing $m$. We also need to initialize the **data qubit** by another qRAM operation before the Diffusion operation,
# 
# \begin{align*}
# \vert j \rangle_{a}\vert D_{j} \rangle_{d} \vert - \rangle_{f}
# \xrightarrow{oracle}  
# \left \{
#  \begin{array}{l}
# -\vert j \rangle_{a}\vert D_{j} \rangle_{d} \vert - \rangle_{f},  D_{j} = m\\
# \vert j \rangle_{a}\vert D_{j} \rangle_{d} \vert - \rangle_{f},  D_{j}  \neq m
#  \end{array}
#  \right.
#  \xrightarrow{qRAM}
# \left \{
#  \begin{array}{l}
# -\vert j \rangle_{a}\vert 0 \rangle_{d}\vert - \rangle_{f},  D_{j} = m \\
# \vert j \rangle_{a}\vert 0 \rangle_{d}\vert - \rangle_{f},　D_{j}\neq m
#  \end{array}
#  \right.
#  \end{align*}
#  
# where $f$ denotes the flag qubit.  
# 
# In this case, we can configure an oracle operation using the [C3X gate](https://qiskit.org/documentation/stubs/qiskit.circuit.library.C3XGate.html#qiskit.circuit.library.C3XGate) . 
# 
# Here, we show the whole circuit for our [qRAM example](#qRAM-Example:-Find-the-data-from-qRAM).

# %%
Image('circuit_ex.png')

# %% [markdown]
# ### Considerations for qRAM implementation
# In the above description we have introduced a naive *qRAM operation* circuit.
# Depending on the data structure, we can simplify the circuit by using **gate synthesis** (equivalence transformation) techniques.
# Also, some simplified gates, e.g. [RCCX](https://qiskit.org/documentation/stubs/qiskit.circuit.library.RCCXGate.html#qiskit.circuit.library.RCCXGate), may help improve your *CNOT*-saving implementation.
# 
# An example of gate synthesis is shown below.

# %%
Image('gatesynthesis_ex.png')

# %% [markdown]
# ## Learning Exercise II-B
# Let's solve a 4-Lights Out problem with qRAM.  
# 
# When the initial board state lightsout4=\[\[Board 0\],\[Board 1\],\[Board 2\],\[Board 3\]\] is described by the following data, 
# determine the _binary_ number of the solvable boards in $3$ switch operations.  (ex. Board 0 → 00, 1 → 01, 2 → 10, 3 → 11)
# 
# Answer by creating a quantum circuit to solve the puzzle shown in the figure below. In the quantum circuit to be submitted, measure only the `solution` (2bit) that solves the puzzle.
# 
# To submit your solution, create a function which takes "lightsout4" as an input and return `QuantumCircuit`.  Function's name does not matter. Make sure it works even if you input another dataset to "lightsout4".
# 
#  **In addition, please implement the quantum circuit within 28 qubits.**
# 
# Please note that you can get the answer with the same endian as the one used in the description. You can also use the following function.
# ```python
# qc = qc.reverse_bits()
# ```

# %%
Image('4lightsout_pr.png')


# %%
lightsout4=[[1, 1, 1, 0, 0, 0, 1, 0, 0],[1, 0, 1, 0, 0, 0, 1, 1, 0],[1, 0, 1, 1, 1, 1, 0, 0, 1],[1, 0, 0, 0, 0, 0, 1, 0, 0]]

# %% [markdown]
# ### Hints
# - Change the oracle of [qRAM data search](#qRAM-Data-search) to an appropriate one.
# - Data storing/writing in *QRAM operation* can be performed in any order. We can reduce the number of gates by taking into account the _hamming distance_ of the address and input data.

# %%
# Kudos: https://github.com/riuriuriuriu/IBMQuantumchallenge/blob/master/2020Nov/week-2/ex_2b_ja.ipynb
import numpy as np
import itertools
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, BasicAer, execute

def week2b_ans_func(lightout4):
    ##### Build your cirucuit here
    ####  In addition, please make it a function that can solve the problem even with different inputs (lightout4). We do validation with different inputs.
    debug = False
    nboard = len(lightout4)
    naddress = int(np.log2(nboard + 1))
    nlight = len(lightout4[0])
    size = int(np.sqrt(nlight))
    
    r_address = QuantumRegister(naddress, 'address')
    r_ispush = QuantumRegister(nlight, 'is_push')
    r_isoff = QuantumRegister(nlight, 'is_off')
    r_oracle = QuantumRegister(1, 'oracle')
    # r_flag = QuantumRegister(1, 'flag')
    r_ancilla = QuantumRegister(7,'ancilla')
    c_measure = ClassicalRegister(naddress, 'measure')
    c_measure2 = ClassicalRegister(nlight, 'measure2')
    c_measure3 = ClassicalRegister(nlight, 'measure3')
    c_measure4 = ClassicalRegister(6, 'measure4')
    c_measure5 = ClassicalRegister(1, 'measure5')
    if(debug):
        qc = QuantumCircuit(r_address, r_ispush, r_isoff, r_oracle, r_flag, r_ancilla, c_measure,c_measure2,c_measure3,c_measure4, c_measure5)
    else:
        qc = QuantumCircuit(r_address, r_ispush, r_isoff, r_oracle, r_ancilla, c_measure)
    
    push = [[] for _ in range(nlight)]
    for i in range(nlight):
        push[i].append(i)
        if(i % size):
            push[i].append(i-1)
        if((i+1) % size):
            push[i].append(i+1)
        if(i-size >= 0):
            push[i].append(i - size)
        if(i+size < nlight):
            push[i].append(i + size)  
    
    N = 1 << nlight
    theta = np.arcsin(2 * np.sqrt(N-1)/ N)
    Grover_nit = int(np.arccos(1 / np.sqrt(N))/ theta)
    Grover_nit = 2

    
    qc.h(r_address)
    qc.x(r_oracle)
    qc.h(r_oracle)
    qc.barrier()
    
    #### qRAM #####################################################################################

    qc.h(r_ispush)
    qc.barrier()

    for it in range(Grover_nit):
        
        if it == 0:
            for i_board in range(nboard):
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
                for i, light in enumerate(lightout4[i_board]):
                    if(not light):
                        qc.mcx(r_address,r_isoff[i], r_ancilla, mode = 'basic')
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
            qc.barrier()
        
        
        for i, q_ispush in enumerate(r_ispush):
            for j in push[i]:
                qc.mcx([q_ispush], r_isoff[j], r_ancilla, mode = 'basic')
        qc.barrier()
        
        qc.mcx([*r_isoff],*r_oracle, r_ancilla ,mode = 'basic')
        qc.barrier()

        for i, q_ispush in enumerate(r_ispush):
            for j in push[i]:
                qc.mcx([q_ispush], r_isoff[j], r_ancilla, mode = 'basic')
        qc.barrier()
        '''
        if it == Grover_nit - 1:
            for i_board in reversed(range(nboard)):
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
                for i, light in enumerate(lightout4[i_board]):
                    if(not light):
                        qc.mcx(r_address,r_isoff[i], r_ancilla, mode = 'basic')
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
            qc.barrier()
        '''
        qc.h(r_ispush)
        qc.x(r_ispush)
        qc.h(r_ispush[-1])
        qc.mcx([*r_ispush[:nlight-1]], r_ispush[-1], r_ancilla, mode = 'basic')
        qc.h(r_ispush[-1])
        qc.x(r_ispush)
        qc.h(r_ispush)
        qc.barrier() 

    for q_ispush in r_ispush:
        ctr = [q_ispush]
        for i_ancilla in range(4):
            qc.mcx(ctr, r_ancilla[i_ancilla])
            qc.x(r_ancilla[i_ancilla])
            ctr.append(r_ancilla[i_ancilla])
        qc.x(r_ancilla[0:4])
        qc.barrier()
    
    ##### Oracle ##################################################################################  
    # 3 push
    qc.x(r_ancilla[2])
    qc.x(r_ancilla[3]) 
    qc.mcx([*r_ancilla[0:4]], r_oracle)
    #qc.x(r_ancilla[2])
    #qc.x(r_ancilla[3])
    qc.barrier()
    
    # 2 push
    qc.x(r_ancilla[0])
    #qc.x(r_ancilla[2])
    #qc.x(r_ancilla[3])
    qc.mcx([*r_ancilla[0:4]], r_oracle)
    qc.x(r_ancilla[0])
    #qc.x(r_ancilla[2])
    #qc.x(r_ancilla[3])
    qc.barrier()
         
    # 1 push
    qc.x(r_ancilla[1])
    #qc.x(r_ancilla[2])
    #qc.x(r_ancilla[3])
    qc.mcx([*r_ancilla[0:4]], r_oracle)
    qc.x(r_ancilla[1])
    qc.x(r_ancilla[2])
    qc.x(r_ancilla[3])

    qc.barrier()

    #### qRAM #####################################################################################
    for q_ispush in reversed(r_ispush):
        ctr = [q_ispush, *r_ancilla[0:3]]
        qc.x(r_ancilla[0:4])
        for i_ancilla in reversed(range(4)):
            qc.x(r_ancilla[i_ancilla])
            qc.mcx(ctr, r_ancilla[i_ancilla])
            ctr.pop(-1)
        qc.barrier()

    for it in range(Grover_nit):
        
        qc.h(r_ispush)
        qc.x(r_ispush)
        qc.h(r_ispush[-1])
        qc.mcx([*r_ispush[:nlight-1]], r_ispush[-1], r_ancilla, mode = 'basic')
        qc.h(r_ispush[-1])
        qc.x(r_ispush)
        qc.h(r_ispush)
        qc.barrier() 
        
        '''
        if it == 0:
            for i_board in (range(nboard)):
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
                for i, light in enumerate(lightout4[i_board]):
                    if(not light):
                        qc.mcx(r_address,r_isoff[i], r_ancilla, mode = 'basic')
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
        qc.barrier()
        '''
        
        for i, q_ispush in enumerate(r_ispush):
            for j in push[i]:
                qc.mcx([q_ispush], r_isoff[j], r_ancilla, mode = 'basic')
        qc.barrier()
        
        qc.mcx([*r_isoff],*r_oracle, r_ancilla, mode = 'basic')
        qc.barrier()

        for i, q_ispush in enumerate(r_ispush):
            for j in push[i]:
                qc.mcx([q_ispush], r_isoff[j], r_ancilla, mode = 'basic')
        qc.barrier()

        if it == Grover_nit - 1:
            for i_board in reversed(range(nboard)):
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
                for i, light in enumerate(lightout4[i_board]):
                    if(not light):
                        qc.mcx(r_address,r_isoff[i], r_ancilla, mode = 'basic')
                for i_address in range(naddress):
                    if( not (i_board >> i_address & 1)):
                        qc.x(r_address[i_address])
            qc.barrier()
        
    qc.x(r_oracle)
    qc.h(r_ispush)
    qc.barrier()
    
    #### defusion #################################################################################
    if(not debug):
        qc.h(r_address)
        qc.x(r_address)
        qc.h(r_address[-1])
        qc.mcx(r_address[0:-1], r_address[-1], r_ancilla, mode = 'basic')
        qc.h(r_address[-1])
        qc.x(r_address)
        qc.h(r_address)
        qc.barrier()
    
    #### measure ##################################################################################
    qc.measure(r_address, c_measure)
    if(debug):
        qc.measure(r_isoff, c_measure2)
        qc.measure(r_ispush, c_measure3)
        qc.measure(r_ancilla, c_measure4)
        qc.measure(r_flag, c_measure5)
        
    ###############################################################################################
    return qc

# qc = week2b_ans_func(lightsout4)
# qc.draw()


# %%
# Submission code
from qc_grader import prepare_ex2b, grade_ex2b, submit_ex2b

# Execute your circuit with following prepare_ex2b() function.
# The prepare_ex2b() function works like the execute() function with only QuantumCircuit as an argument.
job  =  prepare_ex2b(week2b_ans_func)

result = job.result()
count = result.get_counts()
original_problem_set_counts = count[0]

original_problem_set_counts
# The bit string with the highest number of observations is treated as the solution.


# %%
# Check your answer by executing following code.
# The quantum cost of the QuantumCircuit is obtained as the score. The quantum cost is related to rank only in the third week.
grade_ex2b(job)


# %%
# Submit your results by executing following code. You can submit as many times as you like during the period. 
submit_ex2b(job)


