#!/usr/bin/env python2
 
import RPi.GPIO as GPIO, time
import signal
import sys
import getopt

#Set to 1 for debug info
DEBUG=1

def LACTION(LED, SET): 
    GPIO.output(LED, SET)
    return

def LOFFall(LEDS):
    for LED in LEDS:
        LACTION(LED, False)
    return

def LEDret(color):
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
    if color == "red":
        LEDS = [ LEDr1, LEDr2, LEDr3 ]
    elif color == "yellow":
        LEDS = [ LEDo1, LEDo2, LEDy1, LEDy2 ]
    elif color == "green":
        LEDS = [ LEDg1, LEDg2, LEDg3 ]
    elif color == "all":
        LEDS = [ LEDr1, LEDr2, LEDr3, LEDo1, LEDo2, LEDy1, LEDy2, LEDg1, LEDg2, LEDg3 ]

    return LEDS


def LEDinit():
    GPIO.setmode(GPIO.BCM)

    for LED in LEDret("all"):
        GPIO.setup(LED, GPIO.OUT)

#capture ctrl+c and switch off all leds
def signal_handler(signal, frame):
    print 'EXIT'
    LOFFall(LEDinit())
    sys.exit(0)

#define signal for capturing
signal.signal(signal.SIGINT, signal_handler)

def usage():
    print """Raspberry PI GPIO LED SCRIPT
KrisKo 2014

OPTIONS:
    Turn LED color ON/OFF (NR=1/0)
    -r NR   --red=NR
    -y NR   --yellow=NR
    -g NR   --green=NR
    """
    exit(0)

def led_action(state, LEDS):
    if state == 1:
        for LED in LEDS:
            if (DEBUG): print "Executing LON for: %s" % LED
            LACTION(LED, True)
    else:
        for LED in LEDS:
            LACTION(LED, False)


def main():
    repeat = 1
    woff = 0
    variant = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hir:y:g:", ["help", "init", "red=", "yellow=", "green="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    
    LEDinit()

    for opt, arg in opts:
        #iteration count
        if opt in ("-i", "--init"):
            LOFFall(LEDret("all"))
        elif opt in ("-r", "--red"):
            action = "red"
            led_action(int(arg), LEDret(action))
        elif opt in ("-y", "--yellow"):
            action = "yellow"
            led_action(int(arg), LEDret(action))
        elif opt in ("-g", "--green"):
            action = "green"
            led_action(int(arg), LEDret(action))
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"


if __name__ == "__main__":
    main()

##################
# ChangeLog/TODO #
##################
# 1.0.0 2014-06-18 Genesis
##################
