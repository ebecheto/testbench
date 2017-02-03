# python arange4.py B06_avgs.log
# arange conso
# for file in B*_avgs.log;do python ../arange4.py >> conso.txt ;done
from numpy import arange, concatenate # from utiles import *
import sys
ampls=arange(0.05, 0.4, 0.025)
ampls=concatenate((ampls, arange(0.4, 1.2+0.05, 0.2)))


#nb=range(1,17)

#filename='CH_01.log' if len(sys.argv) < 2 else sys.argv[1]
#filename='_CH_01.log' if len(sys.argv) < 2 else sys.argv[1]
filename = "B02_avgs.log"  if len(sys.argv) < 2 else sys.argv[1]


with open(filename, 'r') as f:
    # do things with your file
    data = f.read()

data=data.split('\n')
data.remove('') #remove empty lines

#fnb=filename.split('_')[2].split('.')[0]
fnb=filename.split('B')[1].split('_')[0]
i=0
for line in data:          # Boucle sur les lignes du fichier
    if line.strip().startswith('#'): # Ne pas considerer  lignes "commentees"
        print fnb, line
        continue
##     if line.strip().startswith(' '): # Ne pas considerer  lignes "commentees"
##         print line
##         continue
##     row=line.split("\t")
##     new=[fnb]+row
##     i+=1
## #    row[2]="{}".format(ampls[i])
##     print "\t".join(new)

#" + ".join("\t".join(line.split("*")).split("+"))

# line.replace("V", " V ").replace("*"," * ")
