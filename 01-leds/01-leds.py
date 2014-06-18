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
    LEDS = [ LEDr1, LEDr2, LEDr3, LEDo1, LEDo2, LEDy1, LEDy2, LEDg1, LEDg2, LEDg3 ]

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
    -o NR                   time the led are off (matches effect time if not specified)

    -s NR, --snake=NR       snake; NR=time of LED shift
    -r NR, --snaker=NR      snake reversed; NR=time of LED shift
    -b NR, --blink=NR       blink all leds
    -d NR                   double reversed snake

    -v NR, --variant=NR     0 (default)
    -f NR, --fullsnake=NR   snake with several variants (0, 1)
    -g NR                   snake with several variants (0, 1)
    """
    exit(0)

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
    if ( wait[0] == 0 ): wait[0] = wait[1]
    while (repeat > 0):
        for LED in LEDS:
            LON(LED)
        time.sleep(wait[1])
        for LED in LEDS:
            LOFF(LED)
        time.sleep(wait[0])
        repeat -= 1
    LOFFall(LEDS)

#snake like effect which wont turn off leds
def fullsnake(wait, repeat, LEDS, variant):
    if ( variant == 0 ): 
        LEDSoff = LEDS
    elif ( variant == 1 ): 
        LEDSoff = LEDS[::-1]

    while (repeat > 0):
        for LED in LEDS:
            LON(LED)
            time.sleep(wait)
        for LED in LEDSoff:
            LOFF(LED)
            time.sleep(wait)
        repeat -= 1
    LOFFall(LEDS)

def gsnake(wait, repeat, LEDS, variant):
    while (repeat > 0):
        LEDSrev = LEDS
        #copy list content
        LEDScp = LEDS[:]

        for LEDrem in LEDS[::-1]:
            for LED in LEDScp:
                LEDact=LED
                LON(LEDact)
                try:
                    #if we have same LEDs, skip this iteration (this is for reversed LED list)
                    if LEDact == LEDrem:
                        if (DEBUG): print "SAME LEDS (GPIO: %s), skipping iteration" % LEDact
                        #if this is the first LED and the last in sequence, dont LOFF it
                        if LEDact != LEDprev:
                            LOFF(LEDprev)
                        time.sleep(wait)
                        continue
                    if ( variant == 0 and LEDact != LEDprev ): LOFF(LEDprev)
                except:
                    pass
                time.sleep(wait)
                LEDprev=LEDact
            del LEDScp[-1]
        
        LEDScp = LEDS[:]
        if (DEBUG): print "LIST: %s" % LEDScp
        for LEDrem in LEDS[::-1]:
            for LED in LEDScp:
                LEDact=LED
                LOFF(LEDact)
                try:
                    #if we have same LEDs, skip this iteration (this is for reversed LED list)
                    if LEDact == LEDrem:
                        if (DEBUG): print "SAME LEDS (GPIO: %s), skipping iteration" % LEDact
                        #if this is the first LED and the last in sequence, dont LOFF it
                        if LEDact != LEDprev:
                            LON(LEDprev)
                        time.sleep(wait)
                        continue
                    if ( variant == 0 and LEDact != LEDprev ): LON(LEDprev)
                except:
                    pass
                time.sleep(wait)
                LEDprev=LEDact
            if (DEBUG): print "%s" % LEDScp
            del LEDScp[-1]
        repeat -= 1
    LOFFall(LEDS)

# double reversed snake
def dsnake(wait, repeat, LEDS):
    while (repeat > 0):
        LEDr = LEDS[::-1]
        for LED in LEDS:
            LEDact=LED
            LON(LEDact)
            LON(LEDr[0])
            try:
                #if we have same LEDs, skip this iteration (this is for reversed LED list)
                if LEDprev == LEDact:
                    if (DEBUG): print "SAME LEDS (GPIO: %s), skipping iteration" % LEDact
                    continue
                #for smoother effect...
                #if we are not in the middle LOF
                if ( LEDact != LEDrprev and LEDr[0] != LEDprev ):
                    LOFF(LEDprev)
                    LOFF(LEDrprev)
                #else remove next led in LEDr and skip for loop iteration
                elif ( LEDact == LEDrprev and LEDr[0] == LEDprev ):
                    del LEDr[0]
                    continue
            except:
                pass
            time.sleep(wait)
            LEDprev=LEDact
            LEDrprev=LEDr[0]
            del LEDr[0]
        repeat -= 1
    LOFFall(LEDS)



def main():
    repeat = 1
    woff = 0
    variant = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:s:r:b:v:f:g:d:", ["help", "snake=", "snaker=", "blink=", "variant=", "fullsnake="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for opt, arg in opts:
        #iteration count
        if opt == "-i":
            repeat = arg
        elif opt == "-o":
            woff = arg
        elif opt in ("-v", "--variant"):
            variant = int(arg)
        elif opt in ("-s", "--snake"):
            snake(float(arg), int(repeat), LEDinit())
        elif opt in ("-r", "--snaker"):
            snaker(float(arg), int(repeat), LEDinit())
        elif opt in ("-b", "--blink"):
            wait = [ float(woff), float(arg) ]
            blink(wait, int(repeat), LEDinit())
        elif opt in ("-f", "--fullsnake"):
            fullsnake(float(arg), int(repeat), LEDinit(), variant)
        elif opt == "-g":
            gsnake(float(arg), int(repeat), LEDinit(), variant)
        elif opt in ("-d"):
            dsnake(float(arg), int(repeat), LEDinit())
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()

