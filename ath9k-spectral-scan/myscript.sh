#!/bin/sh
max_samples=10000
plot_pause=0.05

# The function gathers the binary spectral scan data and outputs it.
# Each packet looks like this:
#   <number>\n
#   <base64 line 1>\n
#   <base64 line ..>\n
#   .\n
spectral_scan() {
	echo manual > /sys/kernel/debug/ieee80211/phy0/ath9k_htc/spectral_scan_ctl
	ifconfig wls35u1 up
	while true
	do
		for i in $(seq 1 10)
		do
			echo $i
			#echo chanscan | tee /sys/kernel/debug/ieee80211/phy1/ath9k_htc/spectral_scan_ctl > /dev/null
			iw dev wls35u1 scan trigger freq 2422  >/dev/null
			cat /sys/kernel/debug/ieee80211/phy0/ath9k_htc/spectral_scan0 | base64
			echo .
		done
	done
}

# The function processes spectral_scan() data into human readable output and puts it into /tmp/fft.dump.all.
# Each time new data arrives it is appended and the oldest data is pruned regularly.
# The output file is intended to be read by gnuplot.
process() {
	while read i
	do
		echo $i
		while read line
		do
			test "$line" = . && break
			echo "$line"
		done | base64 -d > /tmp/fftdump/fft.dump.$i

		cat /tmp/fftdump/fft.dump.all > /tmp/fftdump/fft.dump.all.new
		./fft2txt < /tmp/fftdump/fft.dump.$i | awk '{print $4 " " $6}' >> /tmp/fftdump/fft.dump.all.new
		tail -n $max_samples < /tmp/fftdump/fft.dump.all.new > /tmp/fftdump/fft.dump.all.new.limited
		# cat < /tmp/fftdump/fft.dump.all.new > /tmp/fftdump/fft.dump.all.new.limited
		mv /tmp/fftdump/fft.dump.all.new.limited /tmp/fftdump/fft.dump.all

		# `mv` guarantees /tmp/fft.dump.all stays consistent
	done
}

# Essential gnuplot real-time drawing config
cat << EOF > /tmp/gnuplot.conf
set terminal qt noraise
set yrange [-128:0]
pause $plot_pause
replot
reread
EOF

gnuplot=
trap '
	s=$?
	trap - EXIT QUIT
	kill -HUP $gnuplot
	exit $s
' INT HUP KILL TERM EXIT QUIT
#rm /tmp/fftdump/*
touch /tmp/fftdump/fft.dump.all
gnuplot -persistent -e 'plot "/tmp/fftdump/fft.dump.all"' /tmp/gnuplot.conf & gnuplot=$!
spectral_scan | process
