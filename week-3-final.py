# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython.display import Image, display
Image("ryoko.png", width="70")

# %% [markdown]
# # The Final Stage
# %% [markdown]
# *Dr. Ryoko is stuck in the quantum multiverse due to noise clusters interfering with her device. <br/>
# Please DM Dr. Ryoko and ask her about the **noise clusters** and you will find out more. <br/>
# Dr. Ryoko is trying to clear noise clusters with her laser beams, but has only 3 shots left.<br/>
# To make matters worse, there seems to be one area (board) that cannot be cleared within 3 shots. <br/>
# Help Dr. Ryoko identify that one area (board) with noise clusters that **cannot be cleared within 3 shots**. Good luck!<br/>*
# 
# [<< Click here to communicate with Dr. Ryoko through the web cam >>](https://youtu.be/Bkk5-j6rpoM)
# 
# *You can do this by learning how to solve a famous classic puzzle called “Asteroids puzzle”.*
# %% [markdown]
# # Week3: False Asteroids
# Asteroids is a famous puzzle with the following setup and rules:
# - The asteroids are placed on a grid.
# - The objective is to destroy all the asteroids by shooting laser beams: either vertically or horizontally.
# - Determine how to destroy all the asteroids by shooting no more than the specified number of beams.
# 
# The following image is an example of an Asteroids puzzle. In this example, the board size is 4 × 4 and we have six asteroids.

# %%
Image('asteroids_example.png')

# %% [markdown]
# As shown below, we can destroy all the asteroids by shooting 3 lasers vertically. Each thick blue line represents a laser beam. 

# %%
Image('asteroids_beam_example.png')

# %% [markdown]
# There are also false Asteroid problems. An Asteroid problem is false if the asteroids cannot be cleared within the specified number of beams. The following example is a false Asteroid problem with 3 laser beams.

# %%
Image('false_asteroids_example.png')

# %% [markdown]
# ----------
# # Final Exercise
# There are 16 areas (boards) that Dr. Ryoko needs to clear, each of which has 6 noise clusters that correspond to an asteroid in "Asteroids puzzle". However, there happens to be one area that cannot be cleared within three laser shots! Use Grover's algorithm you learned in Weeks 1 & 2 to find that one area (board)!
# %% [markdown]
# A board with asteroids is represented with a list of tuples. Each tuple represents the coordinate of an asteroid in the format `[row index, column index]`. Therefore, a board according to the following image can be represented as:
# 
# ```
# [['0', '0'], ['1', '1'], ['2', '2'], ['3', '0'], ['3', '1'], ['3', '2']]
# ```
# 

# %%
Image('asteroids_example.png')

# %% [markdown]
# There are 16 areas (boards) with the following configurations.
# Find the area that cannot be cleared with 3 laser shots by using Grover's algorithm to help Dr. Ryoko!

# %%
problem_set =     [[['0', '2'], ['1', '0'], ['1', '2'], ['1', '3'], ['2', '0'], ['3', '3']],
    [['0', '0'], ['0', '1'], ['1', '2'], ['2', '2'], ['3', '0'], ['3', '3']],
    [['0', '0'], ['1', '1'], ['1', '3'], ['2', '0'], ['3', '2'], ['3', '3']],
    [['0', '0'], ['0', '1'], ['1', '1'], ['1', '3'], ['3', '2'], ['3', '3']],
    [['0', '2'], ['1', '0'], ['1', '3'], ['2', '0'], ['3', '2'], ['3', '3']],
    [['1', '1'], ['1', '2'], ['2', '0'], ['2', '1'], ['3', '1'], ['3', '3']],
    [['0', '2'], ['0', '3'], ['1', '2'], ['2', '0'], ['2', '1'], ['3', '3']],
    [['0', '0'], ['0', '3'], ['1', '2'], ['2', '2'], ['2', '3'], ['3', '0']],
    [['0', '3'], ['1', '1'], ['1', '2'], ['2', '0'], ['2', '1'], ['3', '3']],
    [['0', '0'], ['0', '1'], ['1', '3'], ['2', '1'], ['2', '3'], ['3', '0']],
    [['0', '1'], ['0', '3'], ['1', '2'], ['1', '3'], ['2', '0'], ['3', '2']],
    [['0', '0'], ['1', '3'], ['2', '0'], ['2', '1'], ['2', '3'], ['3', '1']],
    [['0', '1'], ['0', '2'], ['1', '0'], ['1', '2'], ['2', '2'], ['2', '3']],
    [['0', '3'], ['1', '0'], ['1', '3'], ['2', '1'], ['2', '2'], ['3', '0']],
    [['0', '2'], ['0', '3'], ['1', '2'], ['2', '3'], ['3', '0'], ['3', '1']],
    [['0', '1'], ['1', '0'], ['1', '2'], ['2', '2'], ['3', '0'], ['3', '1']]]

# %% [markdown]
# Answer by creating a quantum circuit to solve the puzzle shown with the problem set above. In the quantum circuit to be submitted, measure **only the `solution` (4bit)** that solves the puzzle. <br/>
# To submit your solution, create a function that takes `problem_set` as an input and then returns a  `QuantumCircuit`.  You can name the function as you like. Make sure it works even with another dataset of "problem_set". We will validate your circuit with different inputs.<br/>
# Make a circuit that gets the correct answer at a low cost. The lower the cost, the better.
# 
# ## <span style="color: red; ">IMPORTANT: Final exercise submission rules</span>
# 
# **For solving this problem:**<br/>
# - **Please implement the quantum circuit within <span style="color: red; ">28 qubits.</span>**<br/>
# - Use **Grover's algorithm** you learned in Week1 & 2 with **<span style="color: red; ">iteration ＝ 1.</span>**
# - The initial state for Grover's algorithm must be equal probability distributions. For example, if you want use only 3 computational bases for 2 qubits instead of 4 as the initial state. Then, the state will be $\sqrt\frac{1}{3} (|00\rangle + |01\rangle + |11\rangle)$
# 
# - Please note that you can get the answer with the same endian as the one used in Week2 explanation. You should map the index of the problem into four classical registers *`c[0:4]`* in binary. `c[0]` is the highest bit and `c[3]` is the lowest bit. For example, when mapping 12, the furthest left bit of the `1100` will be mapped to `c[0]`.
# - Make sure you **create an oracle** that **doesn't require any knowledge of what the answers are**. (For example, you are not allowed to create an oracle by using a classical optimization solver to get your answers for it.)  
# - With the exception of the Unroller, which is required for decomposing your circuit to calculate quantum costs, you are not allowed to use any existing transpiler passes nor original transpilers for making simplifications in this competition.
# - Please **do not run jobs in succession** even if you are concerned that your job is not running properly. This can create a long queue and clog the backend. You can check whether your job is running properly at:<br/>
# https://quantum-computing.ibm.com/results  
# - Your score for this exercise will be same as the cost of your QuantumCircuit. The lower the cost, the better.
# - Judges will check top 10 solutions manually to see if their solutions adhere to the rules. **Please note that your ranking is subject to change after the challenge period as a result of the judging process.**
# - Top 10 participants will be recognized and asked to submit a write up on how they solved the exercise.

# %%
def week3_ans_func(problem_set):
    ##### build your quantum circuit here
    ##### In addition, please make it a function that can solve the problem even with different inputs (problem_set). We do validation with different inputs. 
    
    #### Code for Grover's algorithm with iterations = 1 will be as follows. 
    #### for i in range(1):
    ####   oracle()
    ####   diffusion()
    
    return qc


# %%
# Submission code
from qc_grader import grade_ex3, prepare_ex3, submit_ex3

# Execute your circuit with following prepare_ex3() function.
# The prepare_ex3() function works like the execute() function with only QuantumCircuit as an argument.
job = prepare_ex3(week3_ans_func)

result = job.result()
counts = result.get_counts()
original_problem_set_counts = counts[0]

original_problem_set_counts
# The bit string with the highest number of observations is treated as the solution.


# %%
# Check your answer by executing following code.
# The quantum cost of the QuantumCircuit is obtained as the score. The lower the cost, the better.
grade_ex3(job)


# %%
# Submit your results by executing following code. You can submit as many times as you like during the period. 
submit_ex3(job)


