import numpy as np
import matplotlib.pyplot as plt
import os

# data saved from scope (Save Now!)
# skip 5 header rows then take only every 100 lines

# files="W_=600fF_-160deg_Cd270p_00000.dat", "W_=600fF_-160deg_Cd270p_00001.dat"

patterns=["30f", "100f", "300f", "600f", "1000f"]
prefiles=[f for f in os.listdir(".") if (f.endswith('.dat') and 1+f.find("-160") )]

for motif in patterns:
    print "using pattern : "+motif
    files = [f for f in prefiles if 1+f.find(motif)]
    datas=[np.loadtxt(f_in, delimiter=',') for f_in in files]
    for data in datas:
        plt.plot(data[:,0],data[:,1]);
    plt.legend(files,loc='center left', prop={'size':6});
    plt.show();
    plt.savefig("pic_"+motif+".png")
#    raw_input("press return")
    plt.close()
