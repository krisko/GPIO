#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import signal

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
col_r=0
col_g=0
col_b=0

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
  h     show tis help
  q     quit

''')

# set color intensity (operation add/sub, col_state 0-100, color r/g/b)
def col_adjust(op, col_state, color):
    if (op == "add"):
        col_state+=1
    elif (op == "sub"):
        col_state-=1
    color.ChangeDutyCycle(col_state)
    return col_state

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

# read stdin in a loop
while True:
    char=func()
    if char == "r" and col_r < 100:
        col_r=col_adjust("add", col_r, r)
    elif char == "e" and col_r > 0:
        col_r=col_adjust("sub", col_r, r)
    elif char == "g" and col_g < 100:
        col_g=col_adjust("add", col_g, g)
    elif char == "f" and col_g > 0:
        col_g=col_adjust("sub", col_g, g)
    elif char == "b" and col_b < 100:
        col_b=col_adjust("add", col_b, b)
    elif char == "v" and col_b > 0:
        col_b=col_adjust("sub", col_b, b)
    elif char == "h":
        usage()
    else:
        print ("Unknown function or color out of range. Type 'q' to quit")
    print("COLOR R:", col_r, "G:", col_g, "B:", col_b)
