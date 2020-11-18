# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Previously on the IBM Quantum Challenge
# *Ryoko has been stuck in the quantum realm. Please DM Ryoko and ask her about the **quantum realm** and you will find out more.  <br/>
# She is in a square room with excited qubits blocking her passage. <br/>
# How can you help Dr. Ryoko get out of the room?<br/>
# You can do this by learning how to solve a famous classic puzzle called "lights out." Good luck!*
# 
# [<< Click here to communicate with Dr. Ryoko through the web cam >>](https://youtu.be/kLizHnvTguE)

# %%
from IPython.display import Image, display
Image('ryoko_pillars.png')

# %% [markdown]
# # Week2-A: Lights Out Puzzle
# 
# **Lights out** is a famous puzzle game. The player is given a rectangular grid of lights which can be switched on and off. When you flip a switch inside one of those squares, it will toggle the on/off state of this and adjacent squares (up, down, left and right). Your goal is to turn all the lights off from a random starting light pattern.
# 
# ## Example Puzzle
# 
# An example of the puzzle with 3 x 3 grid is shown in the figure below. The light squares are labelled from 0 to 8. We can represent the starting pattern using a list of numbers, where `1` represents lights switched on and `0` represnts ligths switched off. The list `lights` below represents the starting pattern in this example (squares 3, 5, 6, 7 are on and the rest are off):
# 
# ```python
# lights = [0, 0, 0, 1, 0, 1, 1, 1, 0]
# ```
# 
# The example puzzle can be solved by flipping the switches in square 0, 3 and 4 as illustrated step by step in the figure. If you play with it a little bit, you will soon notice **two important properties of this puzzle game**:
# 
# 1. You don't need to flip a switch more than once.
# 2. The order of flipping doesn't matter.
# 
# Therefore, we can represent the puzzle solution as a list of numbers similar to the starting pattern. However, the meaning of `0` and `1` are different here:  `1` represents flipping a switch and `0` represents *not* flipping a switch. 
# 
# ```python
# solution = [1, 0, 0, 1, 1, 0, 0, 0, 0]
# ```

# %%
Image('lights_out_rule.png')

# %% [markdown]
# # Learning Exercise II-A
# 
# Let's try to solve a "Lights Out" puzzle using **Grover's algorithm**! The information you learned last week will be helpful in solving this puzzle.
# 
# Answer by creating a quantum circuit to solve the puzzle shown in the figure below. In the quantum circuit to be submitted, measure **only the `solution` (9bit)** that solves the puzzle. 
# To submit your solution, create a function which takes `lights` as an input and then returns a  `QuantumCircuit`.  You can name the function as you like. Make sure it works even with another dataset of "lights". We will validate your circuit with different inputs.
# 
# **In addition, please implement the quantum circuit within 28 qubits.**
# 
# There are several ways to solve it without using Grover's algorithm, but we ask you to **use Grover's algorithm** for this exercise. It should help you in solving other challenges.
# 
# Please note that you can get the answer with the same endian as the one used in the description. You can also use the following function.
# ```python
# qc = qc.reverse_bits()
# ```

# %%
Image('lights_out_prob.png')

# %% [markdown]
# ## Hint
# You’ll need a more complex oracle than the “Week1-B oracle” to solve this problem. 
# The added auxiliary qubits will help you design the oracle part, but they need to be 
# handled with care.  At the end of the oracle part, all auxiliary qubits must be returned 
# to their initial state (this operation is sometimes called Uncomputation). 
# [Week 3 of last year’s IBM Quantum Challenge](https://github.com/quantum-challenge/2019/blob/master/problems/week3/week3_en.ipynb) 
# will support your understanding of this concept. 
# 
# If you are not sure about the optimal number of iterations for Grover's algorithm, solve 
# [this quiz](https://github.com/qiskit-community/IBMQuantumChallenge2020/tree/main/quizzes/quiz_1) and talk to Dr. Ryoko(@ryoko) in the [Qiskit slack](qiskit.slack.com) via direct message. You can get important formulas of the theoretical aspects of week 1-B.

# %%
# The starting pattern is represented by this list of numbers.
# Please use it as an input for your solution.
lights = [0, 1, 1, 1, 0, 0, 1, 1, 1]

#%%
##############################################################
from qiskit import IBMQ, BasicAer, Aer, QuantumCircuit, execute
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np

# #%%
# # Create a oracle circuit to flip the qubits we are looking for (CZ gate does that).
# # To do the amplifitude, we will use the oracle + reflection = Grover's diffusion operator
# oracle = QuantumCircuit(2, name='oracle')
# oracle.cz(0,1)
# oracle.to_gate()
# oracle.draw(output="mpl")

# #%%
# # check if the oracle is doing what we expect (S) for superposition:
# backend = Aer.get_backend('statevector_simulator')
# grover_circ = QuantumCircuit(2, 2)
# grover_circ.h([0,1]) # Superposition S
# grover_circ.append(oracle, [0,1]) # to execute simutaneously
# grover_circ.draw(output="mpl")

# #%%
# # exec in a simulator:
# job = execute(grover_circ, backend)
# result = job.result()

# #%%
# sv = result.get_statevector()
# # we have 00, 01, 10, 11
# # 11 is the winner, because our oracle applied the cz at (0,1)
# # [ 0.5+0.j,  0.5+0.j,  0.5+0.j, -0.5+0.j] Fliped the last one.
# np.around(sv, 2)

# #%% reflection amplifitude amplification
# reflection = QuantumCircuit(2, name='reflection')
# reflection.h([0,1])
# reflection.z([0,1])
# reflection.cz(0,1)
# reflection.h([0,1])
# reflection.to_gate()

# #%% 
# reflection.draw(output="mpl")

#%% 
# put all together:
oracle = QuantumCircuit(2, name='oracle')
oracle.cz(0,1)
oracle.to_gate()

reflection = QuantumCircuit(2, name='reflection')
reflection.h([0,1])
reflection.z([0,1])
reflection.cz(0,1)
reflection.h([0,1])
reflection.to_gate()

backend = BasicAer.get_backend('statevector_simulator')
grover_circ = QuantumCircuit(2,2)
grover_circ.h([0,1]) # Superposition S
grover_circ.append(oracle, [0,1]) # to execute simutaneously
grover_circ.append(reflection, [0,1]) # to execute simutaneously
grover_circ.measure([0,1], [0,1])

#%% 
grover_circ.draw(output="mpl")

#%% 
# exec in a simulator:
job = execute(grover_circ, backend, shots=1)
result = job.result()
result.get_counts()

#%%
sv = result.get_statevector()
# we have 00, 01, 10, 11
# 11 is the winner, because our oracle applied the cz at (0,1)
# [0.+0.j, 0.+0.j, 0.+0.j, 1.-0.j] Fliped and amplified the last one.
np.around(sv, 2)

#%%

#%%
##############################################################

def week2a_ans_func(lights):
    ##### build your quantum circuit here

    
    #####  In addition, please make it a function that can solve the problem even with different inputs (lights). We do validation with different inputs.
    
    return qc


# %%
# Submission code
from qc_grader import prepare_ex2a, grade_ex2a, submit_ex2a

# Execute your circuit with following prepare_ex2a() function.
# The prepare_ex2a () function works like the execute() function with only QuantumCircuit as an argument.
job = prepare_ex2a(week2a_ans_func)

result = job.result()
count = result.get_counts()
original_problem_set_counts = count[0]

original_problem_set_counts
# The bit string with the highest number of observations is treated as the solution.


# %%
# Check your answer by executing following code.
# The quantum cost of the QuantumCircuit is obtained as the score. The quantum cost is related to rank only in the third week.
grade_ex2a(job)


# %%
# Submit your results by executing following code. You can submit as many times as you like during the period. 
submit_ex2a(job)


