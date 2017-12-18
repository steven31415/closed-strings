set output 'output3.png'
set terminal pngcairo size 1024,768 enhanced font 'Verdana,25'

set key top left
set key width -1
set key height 0.5

set title "n=2^4 MB"
set ylabel "run time (s)"
set xlabel "k (MB)"

set pointsize 3

plot '3.dat' using 2:3:xtic(1) title "O(n) RMQs" with linespoints lt 6 lc -1, \
	 '3.dat' using 2:4:xtic(1) title "O(n log(n)) RMQs" with linespoints lt 4 lc -1, \


