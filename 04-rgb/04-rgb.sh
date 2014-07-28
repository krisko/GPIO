#!/bin/bash

# LED mapping
#R = 17
#G = 27
#B = 22

# declare associative array
declare -A LEDArray
LEDArray[r]=17
LEDArray[g]=27
LEDArray[b]=22
LEDArray[y]="r g"
LEDArray[l]="g b"
LEDArray[p]="r b"
LEDArray[w]="r g b"

usage(){
cat << EOF
Direct access to Raspberry PI GPIO pins
krisko 2014

USAGE:
	$0 [OPTION]

EXAMPLE:
	$0 help           display this help
	$0                use STDIN
	$0 (char)         toggle color ([r]ed, [g]reen, [b]lue, [y]ellow, [l]ightblue, [p]urple, [w]hite)
	$0 0.2 (char)...  blink leds, interval 0.2 sec
	$0 inf 0.3 (char) blink leds, interval 0.3 sec, infite loop
EOF
	exit 0
}

# after receiving exit signal, shut down all leds
cleanup(){
	echo -e "\nINFO: Cleaning up..."
	for LED in ${LEDArray[*]}; do
        # only shutdown if the led was/is initialized
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
	# receive color char
	COL="$1"
	# if we have a color combination, else just toggle color
	if [[ "$COL" == [ylpw] ]]; then
		for COLOR in ${LEDArray[$COL]}; do
			[ ! -L /sys/class/gpio/gpio${LEDArray[$COLOR]} ] && initialize "${LEDArray[$COLOR]}"
			[ $(cat /sys/class/gpio/gpio${LEDArray[$COLOR]}/value) -eq 0 ] && val=1 || val=0
			echo $val > /sys/class/gpio/gpio${LEDArray[$COLOR]}/value
		done
	else
	[ ! -L /sys/class/gpio/gpio${LEDArray[$COL]} ] && initialize "${LEDArray[$COL]}"
	[ $(cat /sys/class/gpio/gpio${LEDArray[$COL]}/value) -eq 0 ] && val=1 || val=0
	echo $val > /sys/class/gpio/gpio${LEDArray[$COL]}/value
	fi
}

# close STDERR so we wont see error msg from invalid conditions
exec 2>&-

# do the core cycle
iterate(){
	PARAM=$1
	# if true do only one led toggle and exit w/o cleanup (led stays as is was set)
	NOCLEAN=$2
	[ "$PARAM" == "inf" ] && INF=: && continue
	[ ! $NOCLEAN ] && [ -z $TIME ] && TIME=$PARAM && continue
	# defaul RUN is true
	RUN=:
	while $RUN; do
		# do the iteration x-times
		for (( c=0; c<${#PARAM}; c++ )); do
			COL=${PARAM:$c:1}
			[[ "$COL" == [rgbylpw] ]] && {
				toggle "$COL"
			} || echo -e "\nERROR: invalid color"
		sleep $TIME
		done
		# if not infinite cycle, set RUN to false (this will end while cycle)
		[ ! $INF ] && RUN="false"
	done
	# if NOCLEAN is true, don't clean, just exit
	[ ! $NOCLEAN ] && cleanup || exit 0
}

# handle parameters specified from cmd line
for PARAM; do
	# call usage if we need help
	[ "$1" == "help" -o "$1" == "--help" ] && usage
	# set only if one NR is specified from cmd line
	[ "$#" -eq 1 ] && NOCLEAN=:
	iterate $PARAM $NOCLEAN
done

# if no input was specified, use stdin
echo "INFO: Enter r g b to toggle LEDs color state"
while read -n1 COL; do
	[[ "$COL" == [rgbylpw] ]] && {
	toggle "$COL"
} || echo -e "\nERROR: invalid syntax"
done

