#!/bin/bash

OUTPUT_FILE=test_run_$(date "+%F-%T").txt
echo -e "n\t\t\tk\t\t\tp r time" >> $OUTPUT_FILE

N=2

while [ $N -lt 1000000000 ]
do
	echo "Testing N=$N"
	K=1

	while [ $K -lt $N ]
	do
		for PR in `seq 1 4`;
		do
			#P:   0 = true k-closed, 1=k-pseudo-closed
			#R:   0 = O(n) RMQ, 1 = O(nlogn) RMQ

			case $PR in
				1)
					P=0
					R=0
					;;
				2)
					P=0
					R=1
					;;
				3)
					P=1
					R=0
					;;
				4)
					P=1
					R=1
					;;
			esac

			TOTAL_TIME_TAKEN=0

			# Perform tests on 10 different randomized strings, each looped 10 times
			TEXT_REPEATS=10
			SCRIPT_REPEATS=10

			for i in `seq 1 $TEXT_REPEATS`;
			do	
				python randDNA.py $N

				if [ $P -eq 1 ]
				then
					if [ $R -eq 1 ]
					then
						RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t $SCRIPT_REPEATS -p -r)
					else
						RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t $SCRIPT_REPEATS -p)
					fi
				else
					if [ $R -eq 1 ]
					then
						RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t $SCRIPT_REPEATS -r)
					else
						RESULT=$(python k_closed_identify.py -f randDNA.out -k $K -t $SCRIPT_REPEATS)
					fi
				fi

				TIME_TAKEN=${RESULT##*:}
				TOTAL_TIME_TAKEN=$(echo $TOTAL_TIME_TAKEN+$TIME_TAKEN | bc -l)
			done

			TOTAL_TIME_TAKEN=$(echo $TOTAL_TIME_TAKEN/$TEXT_REPEATS | bc -l)

			echo -e "$N\t\t\t$K\t\t\t$P $R$TIME_TAKEN" >> $OUTPUT_FILE
		done

		K=$((2*$K))

	done

	N=$((2*$N))

done