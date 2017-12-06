import sys
import itertools
import pysais
import argparse
from LCA import RangeMin
from LCA import LogarithmicRangeMin
from timeit import default_timer as timer

# To install PySAIS module needed for Suffix Arrays and LCP
# follow README.md instructions on https://github.com/AlexeyG/PySAIS

# When performing queries on a 0-indexed string
# the range considered is [a, b)


# l value generating function
def get_LPM(sequence, k, LCP):

    # store length of sequence (ignoring $ character)
    n = len(sequence) - 1

    lpm = [0] * n
    lpm[0] = -1

    for i in range(1, n):

        # perform up to k + 1 LCP queries for each suffix
        for j in range(0, k + 1):

            # perform an LCP and update next location to check
            lpm[i] = lpm[i] + LCP(0 + lpm[i], i + lpm[i]) + 1

            # stop if end of string is reached
            if lpm[i] > n - i:
                break

        # remove 1 to ensure final mismatch is not included
        lpm[i] = lpm[i] - 1

    return lpm


# l value generating function from previous l
def get_next_LPM(prev_lpm, sequence, LCP):

    # store length of sequence (ignoring $ character)
    n = len(sequence) - 1

    for i in range(1, n):
        # stop if end of string is reached
        if prev_lpm[i] == n - i:
            continue

        # perform up to 1 additional LCP query for each suffix
        prev_lpm[i] = prev_lpm[i] + LCP(0 + prev_lpm[i] + 1, i + prev_lpm[i] + 1)

        # to ensure final mismatch is included
        prev_lpm[i] = prev_lpm[i] + 1

    return prev_lpm


# determine positions in an array that are larger than all previous values in the array
def get_peaks(array):
    n = len(array)
    peaks = [0] * n

    max_val = -1
    for i in range(0, n):
        if array[i] > max_val:
            peaks[i] = True
            max_val = array[i]
        else:
            peaks[i] = False

    return peaks


# return length of longest closed border (if not closed returns -1)
def get_longest_closed_border(sequence, k, pseudo=False, use_nlogn=False):

	# store length of sequence
	n = len(sequence)

	# trivial case
	if (n == 1):
		return 0

	# append unique terminal character to sequence
	sequence = sequence + "$"

	########################

	# create suffix array and LCP array
	sa = pysais.sais(sequence)
	lcp, lcp_lm, lcp_mr = pysais.lcp(sequence, sa)

	# create inverse suffix array
	isa = [0] * (n + 1)
	for i in range(0, n + 1):
		isa[sa[i]] = i

	# preprocess LCP array for RMQ
	if (use_nlogn):
		rmq = LogarithmicRangeMin(lcp)
	else:
		rmq = RangeMin(lcp)

	# optional printing of suffix array
	if (False):
		for off in sa :
			print('%3d : %s' % (off, sequence[off:]))

    ########################

	# define generic LCP function
	def LCP(i, j):
		if i == j:
			return LCP.n - i

		a = LCP.isa[i]
		b = LCP.isa[j]

		if a > b:
			a, b = b, a

		return LCP.rmq[a:b]

	LCP.n = n
	LCP.isa = isa
	LCP.rmq = rmq

	########################

	# calculate k-psuedo-closed border
	if (pseudo):
		# calculate LPM values
		lpm = get_LPM(sequence, k, LCP)
		#print("LPM:", lpm)

		# calcuate lp values by reversing string
		lsm = get_LPM(sequence[::-1], k, LCP)[::-1]
		#print("LSM:", lsm)

		# get peak locations in l
		lpm_peaks = get_peaks(lpm)
		#print("LPM PEAKS:", lpm_peaks)

		# get peak locations in lp
		lsm_peaks = get_peaks(lsm)
		#print("LSM PEAKS:", lsm_peaks)

		# check conditions
		closed_border = -1

		for j in range(1, n):
		    # 1st condition
		    if j + lpm[j] == n:
		        # 2nd condition
		        if lpm_peaks[j]:
		            # 3rd condition
		            if lsm_peaks[n-1-j]:
		                closed_border = n-j
		                break
		            else:
		                continue
		        else:
		            continue
		    else:
		        continue

		return closed_border
	# calculate k-closed border
	else:
		reallpm = get_LPM(sequence, k, LCP)
		reallsm = get_LPM(sequence[::-1], k, LCP)[::-1]

		closed_border = -1
		lpm = [-1] * n
		lsm = [-1] * n

		for i in range(0, k + 1):
			lpm = get_next_LPM(lpm, sequence, LCP)
			lsm = get_next_LPM(lsm[::-1], sequence[::-1], LCP)[::-1]

			lpm_peaks = get_peaks(lpm)
			lsm_peaks = get_peaks(lsm)

			for j in range(1, n):
				# 1st condition
				if j + lpm[j] == n:
					# 2nd condition
					if lpm_peaks[j]:
						# 3rd condition
						if lsm_peaks[n-1-j]:
							closed_border = n-j
							#print("k:", i)
							#print("REAL LPM:", reallpm)
							#print("PROG LPM:", lpm)
							#print("REAL LSM:", reallsm)
							#print("PROG LSM:", lsm)
							return closed_border

		return -1


# main execution
def main():
	# create argument parser
	parser = argparse.ArgumentParser(description='Identify if given text is k-closed')

	# add arguments f, k, p, t, r
	parser.add_argument('-f', metavar="", type=str, required=True, nargs=1,
	                    help='a text filename')
	parser.add_argument('-k', metavar="", type=int, required=True, nargs=1,
	                    help='a k-error value')
	parser.add_argument('-p', required=False, action='store_true',
	                    help='pseudo-closed flag')
	parser.add_argument('-t', metavar="", type=int, required=False, nargs=1,
	                    help='number of repetitions to calculate timing')
	parser.add_argument('-r', required=False, action='store_true',
	                    help='if set uses O(nlogn) RMQs, otherwise uses O(n) RMQs')

	# store user given arguments
	args = parser.parse_args()
	filename = vars(args)['f'][0]
	k = vars(args)['k'][0]
	use_pseudo = vars(args)['p']

	if vars(args)['t'] == None:
		timing_reps = None
	else:
		timing_reps = vars(args)['t'][0]

	use_nlogn = vars(args)['r']

	# open given text
	with open(filename, 'r') as file:
	    seq = file.readlines()

	seq = "".join(seq).replace('\n','')

	# optionally time execution of algorithm
	start = 0
	end = 0

	if (timing_reps != None):
		start = timer()
		for i in range(0, timing_reps):
			get_longest_closed_border(seq, k, use_pseudo, use_nlogn)
		end = timer()

	# final (or only) run of algorithm to determine solution
	border = get_longest_closed_border(seq, k, use_pseudo, use_nlogn)

	# print solution
	print("Border: " + str(border))

	# optionally print timing result
	if (timing_reps != None):
		print("Time(s): " + str((end - start) / timing_reps))


# call main
if __name__ == "__main__":
	main()
