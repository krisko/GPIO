#!/usr/bin/env python2
 
import RPi.GPIO as GPIO, time
import signal
import sys
import getopt

#Set to 1 for debug info
DEBUG=0

def LON(LED): 
    GPIO.output(LED, True)
    return

def LOFF(LED):
    GPIO.output(LED, False)
    return

def LOFFall(LEDS):
    for LED in LEDS:
        LOFF(LED)
    return

def LEDinit():
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

    return LEDS
 
#capture ctrl+c and switch off all leds
def signal_handler(signal, frame):
    print 'EXIT'
    LOFFall(LEDinit())
    sys.exit(0)

#define signal for capturing
signal.signal(signal.SIGINT, signal_handler)

def usage():
    print """Raspberry PI GPIO LED SCRIPT
KrisKo 2013

OPTIONS:
    -i NR                   number of iterations
    -s NR, --snake=NR       snake; NR=time of LED shift
    -r NR, --snaker=NR      snake reversed; NR=time of LED shift
    -b NR, --blink=NR       blink all leds
    """
#create snake like effect
def snake(wait, repeat, LEDS):
    while (repeat > 0):
        for LED in LEDS:
            LEDact=LED
            LON(LEDact)
            try:
                #if we have same LEDs, skip this iteration (this is for reversed LED list)
                if LEDprev == LEDact:
                    if (DEBUG): print "SAME LEDS (GPIO: %s), skipping iteration" % LEDact
                    continue
                LOFF(LEDprev)
            except:
                pass
            time.sleep(wait)
            LEDprev=LEDact
        repeat -= 1
    LOFFall(LEDS)

def snaker(wait, repeat, LEDS):
    #remove first and last element from list
    #LEDSr.pop(0)
    #LEDSr.pop()
    
    #Join reversed list to LEDS
    LEDSr = LEDS + LEDS[::-1]
    #call snake with joined LEDS + reversed LEDS list
    snake(wait, repeat, LEDSr)

def blink(wait, repeat, LEDS):
    while (repeat > 0):
        for LED in LEDS:
            LON(LED)
        time.sleep(wait)
        for LED in LEDS:
            LOFF(LED)
        time.sleep(wait)
        repeat -= 1
    LOFFall(LEDS)


def main():
    repeat = 1
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:s:r:b:", ["help", "snake=", "snaker=", "blink="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for opt, arg in opts:
        #iteration count
        if opt == "-i":
            repeat = arg
        elif opt in ("-s", "--snake"):
            snake(float(arg), int(repeat), LEDinit())
        elif opt in ("-r", "--snaker"):
            snaker(float(arg), int(repeat), LEDinit())
        elif opt in ("-b", "--blink"):
            blink(float(arg), int(repeat), LEDinit())
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()

