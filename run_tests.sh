#!/bin/bash
N=100
K=1
P=0 #0 = true k-closed, 1=k-pseudo-closed
R=0 #0 = O(n) RMQ, 1 = O(nlogn) RMQ

python randDNA.py $N

if [ $P -eq 1 ]
then
	if [ $R -eq 1 ]
	then
		RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t 100 -p -r)
	else
		RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t 100 -p)
	fi
else
	if [ $R -eq 1 ]
	then
		RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t 100 -r)
	else
		RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t 100)
	fi
fi

TIME_TAKEN=${RESULT##*:}
echo $TIME_TAKEN

echo $TIME_TAKEN >> test_results.txt