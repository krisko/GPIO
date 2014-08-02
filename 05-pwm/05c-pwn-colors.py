#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import signal
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

# define LED connection @ 75Hz
r = GPIO.PWM(17, 75)
g = GPIO.PWM(27, 75)
b = GPIO.PWM(22, 75)

r.start(0)
g.start(0)
b.start(0)

# initial values
col_r=-100
col_g=-100
col_b=-100

def usage():
    print ('''
krisko 2014
Script for adjusting RGB LED color intensity (uses software PWM)

USAGE:
  r     RED+
  e     RED-
  g     GREEN+
  f     GREEN-
  b     BLUE+
  b     BLUE-
  a     add colors
  s     sub colors
  c     run automatic cycle
  h     show this help
  q     quit

''')

# set color intensity (operation add/sub, col_X -100 - +100, color r/g/b)
def col_adjust(op, col_r, col_g, col_b, color):
    if (op == "add"):
        if (color == "r") and (col_r < 100):
            col_r+=1
        elif (color == "g") and (col_g < 100):
            col_g+=1
        elif (color == "b") and (col_b < 100):
            col_b+=1
    elif (op == "sub"):
        if (color == "r") and (col_r > -100):
            col_r-=1
        elif (color == "g") and (col_g > -100):
            col_g-=1
        elif (color == "b") and (col_b > -100):
            col_b-=1
    #set_color(col_r, col_g, col_b)
    return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}

def set_color(col_r, col_g, col_b):
    if (col_r >= 0):
        col_r=(col_r*(-1))+100
    else:
        col_r+=100
    if (col_g >= 0):
        col_g=(col_g*(-1))+100
    else:
        col_g+=100
    if (col_b >= 0):
        col_b=(col_b*(-1))+100
    else:
        col_b+=100
    r.ChangeDutyCycle(col_r)
    g.ChangeDutyCycle(col_g)
    b.ChangeDutyCycle(col_b)

def col_spectrum(op, col_r, col_g, col_b):
    if (op == "add"):
        if (col_b < 50) and (col_r != 100 ) and (col_g != 100):
            col_b+=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_b < 100) and (col_r != 100) and (col_g != 100):
            col_b+=1
            col_g+=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_g < 0) and (col_r != 100):
            col_g+=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_r < 0) and (col_r != 100):
            col_g+=1
            col_r+=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_r < 100) and (col_r != 100) and (col_b == 100): 
            col_r+=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_g == 100) and (col_r > 0) and (col_b > 0):
            col_b-=1
            col_r-=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        else:
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
    elif (op == "sub"):
        if (col_r != 100) and (col_b != 100) and (col_g == 100):
            col_b+=1
            col_r+=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_r > 0):
            col_r-=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_r > -100):
            col_r-=1
            col_g-=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_g > -50):
            col_g-=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_g > -100):
            col_b-=1
            col_g-=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        elif (col_b > -100):
            col_b-=1
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}
        else:
            return {'col_b':col_b, 'col_g':col_g, 'col_r':col_r}


#def signal_handler(signal, frame):
#    print('You pressed Ctrl+C!')
#    sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)

#def init_worker():
#    signal.signal(signal.SIGTERM, signal.SIG_TERM)

# do the cleanup before exit
def cleanup():
    r.stop()
    g.stop()
    b.stop()
    GPIO.cleanup()

# read one char from stdin
def func():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ( ch == "q" ):
        cleanup()
        sys.exit(0)
    return ch

print ("Press 'q' to quit, 'h' to show help.")

def cycle(col_r, col_g, col_b):
    count=1
    try:
        time=float(input('sleeptime: '))
        cycles=int(input('cycles: '))
    except ValueError:
        print("Not a number")
        return 0
    while (count <= cycles):
        while (col_r != 100) or (col_b != 100) or (col_g != 100):
            col_new=col_spectrum("add", col_r, col_g, col_b)
            col_b=col_new['col_b']
            col_g=col_new['col_g']
            col_r=col_new['col_r']
            set_color(col_r, col_g, col_b)
            print("color r:", col_r, "g:", col_g, "b:", col_b)
            sleep(time)
        while (col_r != 0) or (col_b != 0) or (col_g != 100):
            col_new=col_spectrum("add", col_r, col_g, col_b)
            col_b=col_new['col_b']
            col_g=col_new['col_g']
            col_r=col_new['col_r']
            set_color(col_r, col_g, col_b)
            print("color r:", col_r, "g:", col_g, "b:", col_b)
            sleep(time)
        while (col_r != -100) or (col_b != -100) or (col_g != -100):
            col_new=col_spectrum("sub", col_r, col_g, col_b)
            col_b=col_new['col_b']
            col_g=col_new['col_g']
            col_r=col_new['col_r']
            set_color(col_r, col_g, col_b)
            print("color r:", col_r, "g:", col_g, "b:", col_b)
            sleep(time)
        count+=1


# read stdin in a loop
while True:
    char=func()
    if char == "r":
        col_new=col_adjust("add", col_r, col_g, col_b, "r")
    elif char == "e":
        col_new=col_adjust("sub", col_r, col_g, col_b, "r")
    elif char == "g":
        col_new=col_adjust("add", col_r, col_g, col_b, "g")
    elif char == "f":
        col_new=col_adjust("sub", col_r, col_g, col_b, "g")
    elif char == "b":
        col_new=col_adjust("add", col_r, col_g, col_b, "b")
    elif char == "v":
        col_new=col_adjust("sub", col_r, col_g, col_b, "b")
    elif char == "a":
        col_new=col_spectrum("add", col_r, col_g, col_b)
    elif char == "s":
        col_new=col_spectrum("sub", col_r, col_g, col_b)
    elif char == "c":
        cycle(col_r, col_g, col_b)
        continue
    elif char == "h":
        usage()
        continue
    else:
        print ("Unknown function or color out of range. Type 'q' to quit")
        continue

    col_b=col_new['col_b']
    col_g=col_new['col_g']
    col_r=col_new['col_r']
    set_color(col_r, col_g, col_b)
    print("COLOR R:", col_r, "G:", col_g, "B:", col_b)

exit(0)
