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
# You’ll need a more complex oracle than the “Week1-B oracle” to solve this problem. The added auxiliary qubits will help you design the oracle part, but they need to be handled with care.  At the end of the oracle part, all auxiliary qubits must be returned to their initial state (this operation is sometimes called Uncomputation). [Week 3 of last year’s IBM Quantum Challenge](https://github.com/quantum-challenge/2019/blob/master/problems/week3/week3_en.ipynb) will support your understanding of this concept. 
# 
# If you are not sure about the optimal number of iterations for Grover's algorithm, solve [this quiz](https://github.com/qiskit-community/IBMQuantumChallenge2020/tree/main/quizzes/quiz_1) and talk to Dr. Ryoko(@ryoko) in the [Qiskit slack](qiskit.slack.com) via direct message. You can get important formulas of the theoretical aspects of week 1-B.

# %%
# Kudos to: https://github.com/riuriuriuriu/IBMQuantumchallenge/blob/739a7a349696de1084529e707880829b6d97db66/2020Nov/week-2/lights_out.py
# 
# The starting pattern is represented by this list of numbers.
# Please use it as an input for your solution.
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, BasicAer, execute
import numpy as np
lights = [0, 1, 1, 1, 0, 0, 1, 1, 1]

def week2a_ans_func(lights):
    nlight = len(lights)
    size = int(np.sqrt(nlight))
    r_ispush = QuantumRegister(nlight, "is_push")
    r_isoff = QuantumRegister(nlight, "is_off")
    r_oracle = QuantumRegister(1, "oracle")
    cr_measure = ClassicalRegister(nlight, "m")
    qc = QuantumCircuit(r_ispush, r_isoff, r_oracle, cr_measure)

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
            push[i].append(i+size)

    # nit
    N = 1 << nlight
    theta = np.arcsin(2 * np.sqrt(N-1) / N)
    nit = int(np.arccos(1 / np.sqrt(N)) / theta)

    # Grover
    qc.x(r_oracle)
    qc.h(r_ispush)
    qc.barrier()

    for _ in range(nit):

        ### Oracle ###
        for i, light in enumerate(lights):
            if(not light):
                qc.x(r_isoff[i])
        qc.barrier()

        for i, q_ispush in enumerate(r_ispush):
            for j in push[i]:
                qc.cx([q_ispush], r_isoff[j])
        qc.barrier()
        qc.h(r_oracle)
        qc.mcx([*r_isoff], *r_oracle)
        qc.h(r_oracle)
        qc.barrier()
        for i, q_ispush in enumerate(reversed(r_ispush)):
            for j in reversed(push[nlight - i - 1]):
                qc.cx([q_ispush], r_isoff[j])
        qc.barrier()

        for i, light in enumerate(lights):
            if(not light):
                qc.x(r_isoff[i])
        qc.barrier()
        ##############

        qc.h(r_ispush)
        qc.x(r_ispush)
        qc.h(r_ispush[-1])
        qc.mcx([*r_ispush[:nlight-1]], r_ispush[-1])
        qc.h(r_ispush[-1])
        qc.x(r_ispush)
        qc.h(r_ispush)
        qc.barrier()
    qc.measure(r_ispush[::-1], cr_measure)

    return qc

qc = week2a_ans_func(lights)
# qc.draw(output='mpl')
qc.draw()

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


# %%



