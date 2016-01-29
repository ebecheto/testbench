import numpy as np
import matplotlib.pyplot as plt
import itertools

# data saved from scope (Save Now!)
# skip 5 header rows then take only every 100 lines

filename="F1qin=100fF_-160deg_Cd270p_00000.txt"
with open(filename) as f_in:
    x = np.loadtxt(itertools.islice(f_in, 5, None, 100), delimiter=',')

plt.plot(x[:,0],x[:,1])
plt.show() 
