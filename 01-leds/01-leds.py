#!/usr/bin/env python2
 
import RPi.GPIO as GPIO, time
import signal
import sys

#capture ctrl+c and switch off all leds
def signal_handler(signal, frame):
    print 'EXIT'
    LOFFall()
    sys.exit(0)

#define signal for capturing
signal.signal(signal.SIGINT, signal_handler)


def LON(LED): 
    GPIO.output(LED, True)
    return

def LOFF(LED):
    GPIO.output(LED, False)
    return

def LOFFall():
    for LED in LEDS:
        LOFF(LED)
    return

# # # # #
# BEGIN
# # # # #

GPIO.setmode(GPIO.BCM)

#define GPIO ports
LEDr1 = 22
LEDr2 = 17
LEDr3 = 18
LEDo1 = 23
LEDo2 = 24
LEDy1 = 25
LEDy2 = 10
LEDg1 = 4
LEDg2 = 9
LEDg3 = 11

#add led to list
LEDS= [ LEDr1, LEDr2, LEDr3, LEDo1, LEDo2, LEDy1, LEDy2, LEDg1, LEDg2, LEDg3 ]

for LED in LEDS:
    GPIO.setup(LED, GPIO.OUT)
 
def usage():
    print """Raspberry PI GPIO LED SCRIPT
KrisKo 2013

OPTIONS:
    -i NR                   number of iterations
    -s NR, --snake=NR       NR=time of LED shift
    """

def snake(sec, repeat):
    while (repeat > 0):
        for LED in LEDS:
            LEDact=LED
            LON(LEDact)
            try:
                LOFF(LEDprev)
            except:
                pass
            time.sleep(sec)
            LEDprev=LEDact
        repeat = repeat - 1
    LOFFall()

import getopt, sys

def main():
    repeat = 1
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:s:", ["help", "snake="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            repeat = arg
        elif opt in ("-s", "--snake"):
            snake(float(arg), int(repeat))
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()

