set output 'output1.png'
set terminal pngcairo size 1024,768 enhanced font 'Verdana,25'

set key top left
set key width 3
set key height 1

set ylabel "run time (s)"
set xlabel "n (MB)"

set pointsize 3

plot '1.dat' using 2:3:xtic(1) title "k=2^6 kB" with linespoints lt 6 lc -1, \
	 '1.dat' using 2:4:xtic(1) title "k=2^7 kB" with linespoints lt 8 lc -1, \
	 '1.dat' using 2:5:xtic(1) title "k=2^8 kB" with linespoints lt 12 lc -1, \
	 '1.dat' using 2:6:xtic(1) title "k=2^9 kB" with linespoints lt 4 lc -1


