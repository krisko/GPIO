#!/bin/bash

# LED mapping
#LEDr1 = 22
#LEDr2 = 17
#LEDr3 = 18
#LEDo1 = 23
#LEDo2 = 24
#LEDy1 = 25
#LEDy2 = 10
#LEDg1 = 4
#LEDg2 = 9
#LEDg3 = 11

# map leds to numbers 0..9
LEDArray=(22 11 9 4 10 25 24 23 18 17)

usage(){
cat << EOF
Direct access to Raspberry PI GPIO pins
krisko 2014

USAGE:
	$0 [OPTION]

EXAMPLE:
	$0 help        display this help
	$0             use STDIN
	$0 0.2 12345   blink leds 1..5, interval 0.2 sec
	$0 inf 0.3 123 blink leds 1..3, interval 0.3 sec, infite loop

	e.g. double reversed snake
		$0 inf 0.01 102910382947385647746583749283019201
EOF
	exit 0
}

# after receiving exit signal, shut down all leds
cleanup(){
	echo -e "\nINFO: Cleaning up..."
	for LED in ${LEDArray[*]}; do
		[ -L /sys/class/gpio/gpio$LED ] && echo 0 > /sys/class/gpio/gpio$LED/value
	done
	exit 0
}

# trap signals and call cleanup
trap cleanup SIGHUP SIGINT SIGTERM

# init led 
initialize(){
	echo $1 > /sys/class/gpio/export
	echo out > /sys/class/gpio/gpio$1/direction
}

# toggle leds state 0/1
toggle(){
	[ $(cat /sys/class/gpio/gpio$1/value) -eq 0 ] && val=1 || val=0
	echo $val > /sys/class/gpio/gpio$1/value 
}

# close STDERR so we wont see error msg from -le condition
exec 2>&-

iterate(){
	PARAM=$1
	[ "$PARAM" == "inf" ] && INF=: && continue
	[ -z $TIME ] && TIME=$PARAM && continue
	RUN=:
	while $RUN; do
		for (( c=0; c<${#PARAM}; c++ )); do
			NUM=${PARAM:$c:1}
			[ $NUM -le 9 ] && {
				[ ! -L /sys/class/gpio/gpio${LEDArray[$NUM]} ] && initialize "${LEDArray[$NUM]}"
				toggle "${LEDArray[$NUM]}"
			} || echo -e "\nERROR: invalid number"
		sleep $TIME
		done
		[ ! $INF ] && RUN="false"
	done
	cleanup
}

for PARAM; do
	[ "$1" == "help" -o "$1" == "--help" ] && usage
	iterate $PARAM
done

echo "INFO: Enter number 0-9 to toggle LEDs state"
while read -n1 NUM; do
	[ $NUM -le 9 ] && {
	[ ! -L /sys/class/gpio/gpio${LEDArray[$NUM]} ] && initialize "${LEDArray[$NUM]}"
	toggle "${LEDArray[$NUM]}"
} || echo -e "\nERROR: invalid number"
done

