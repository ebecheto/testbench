# http://stackoverflow.com/questions/39089776/python-read-named-pipe
import os, argparse
import errno


# from subprocess import Popen, PIPE
# p = Popen(['python', 'reader.py'], stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
parser = argparse.ArgumentParser(description="reader.py -ip '192.168.0.47'")
parser.add_argument('-ip', default='192.168.0.47', help='fifo name creation ')
args = parser.parse_args(); ip=args.ip



import PulseGenerator81160A
print 'Wait 8sec, slow init'
pul = PulseGenerator81160A.PulseGenerator81160A(ip)
pul.connect()
print "pul connected"


FIFOin = '/tmp/pipe_2pul_'+ip
FIFOut = '/tmp/pipe_2cli_'+ip #<= to client (ret=pul.senf()) #<= fifo send

try:
    os.mkfifo(FIFOin)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise
try:
    os.mkfifo(FIFOut)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

    
while True:
    print("Opening FIFO...")
    with open(FIFOin) as fifoin:
        print("FIFO in opened")
        while True:
#            data = fifo.read()
            data = fifoin.readline()
            if len(data) == 0:
                print("Writer closed")
                break
            print('Read: "{}"'.format(data))
            ret=pul.send(data)
            if '?' in data:
                print('opening fifo for read. Wait until fifo is open for read somewhere')
# clean way would be with open (FIFOut, 'w') as fifout ... so that is close it out of the indentation.
#But i prefer to see the close statement for now,..
                fifout=open(FIFOut, 'w') #<== normally if '?' in FIFOut had been open in read by the client.
                fifout.write(ret) 
#                fifout.flush(ret) 
                fifout.close() 

                
# os.linesep#<== is it different from '\n'

            
# Terminal 1:

# $ python reader.py 
# Opening FIFO...
# <blocks>

# Terminal 2:

# $ echo -n 'hello' > mypipe 
# $ echo 'hello' > mypipe  #<= in case of readline

# Terminal 1:

# FIFO opened
# Read: "hello"
# Writer closed
# Opening FIFO...
# <blocks>

# Terminal 2:

# $ echo -n 'hello' > mypipe 

# Terminal 1:

# FIFO opened
# Read: "hello"
# Writer closed
# Opening FIFO...
# <blocks>

# ... and so on.
