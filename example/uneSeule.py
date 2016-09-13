import argparse, time
parser = argparse.ArgumentParser(description='uneSeule -ch 1')
parser.add_argument('-ch', default=1, help='chanel number')
args = parser.parse_args()
i=int(args.ch)

import OscilloWavePro
osc = OscilloWavePro.OscilloWavePro('192.168.0.46')
osc.send("CLSW")
while float(osc.getMeasurement(2).SWEEPS)<=10:
    True
measures=osc.avgs()[:-1]; print measures #skip last measure
msg="{}".format(i)+"\t"+"\t".join(measures)+'\n'

print msg

foutName="clipboard.txt"
fout=open(foutName, "w")
fout.write(msg)
fout.close()
time.sleep(0.1)#<== write is not instantaneous, wait just a while

import subprocess
cmd="cat "+foutName+ "|sed -e '/^#/d'|xclip -i &"
print cmd
p = subprocess.Popen( cmd , stdout=subprocess.PIPE, shell=True) ; p.kill()
#p = subprocess.Popen( "echo \'Hello World!\'" , stdout=subprocess.PIPE, shell=True) ; p.kill()

