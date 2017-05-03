import sys
import itertools
import pysais
import numpy as np

# To install PySAIS module needed for Suffix Arrays and LCP
# follow README.md instructions on https://github.com/AlexeyG/PySAIS

# class RMQ as taken from
# https://gist.github.com/m00nlight/1f226777a49cfc40ed8f
#
# This is most likely not an efficient implementation of RMQ
# Use as a placeholder
#
# When performing queries on a 0-indexed string
# the range considered is [a, b)

class RMQ:
    def __init__(self, n):
        self.sz = 1
        self.inf = (1 << 31) - 1
        while self.sz <= n: self.sz = self.sz << 1
        self.dat = [self.inf] * (2 * self.sz - 1)
    
    def update(self, idx, x):
        idx += self.sz - 1
        self.dat[idx] = x
        while idx > 0:
            idx = (idx - 1) >> 1
            self.dat[idx] = min(self.dat[idx * 2 + 1], self.dat[idx * 2 + 2])
            
    def query(self, a, b):
        return self.query_help(a, b, 0, 0, self.sz)
            
    def query_help(self, a, b, k, l, r):
        if r <= a or b <= l:
            return sys.maxsize
        elif a <= l and r <= b:
            return self.dat[k]
        else:
            return min(self.query_help(a, b, 2 * k + 1, l, (l + r)>>1),
                        self.query_help(a, b, 2 * k + 2, (l + r) >> 1, r))



# l value generating function
def get_LPM(sequence, k):

    # store length of sequence
    n = len(sequence)

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
    rmq = RMQ(n + 1)
    for i in range(n + 1):
        rmq.update(i, lcp[i])

    # optional printing of suffix array
    print_suffix_array = False

    if (print_suffix_array):
        for off in sa :
            print('%3d : %s' % (off, sequence[off:]))

    ########################

    # define generic LCP function
    def LCP(i, j):
        if i == j:
            return n - i

        a = isa[i]
        b = isa[j]

        if a > b:
            a, b = b, a

        return rmq.query(a, b)

    ########################

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
def get_next_LPM(prev_lpm, sequence):

    # store length of sequence
    n = len(sequence)

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
    rmq = RMQ(n + 1)
    for i in range(n + 1):
        rmq.update(i, lcp[i])

    # optional printing of suffix array
    print_suffix_array = False

    if (print_suffix_array):
        for off in sa :
            print('%3d : %s' % (off, sequence[off:]))

    ########################

    # define generic LCP function
    def LCP(i, j):
        if i == j:
            return n - i

        a = isa[i]
        b = isa[j]

        if a > b:
            a, b = b, a

        return rmq.query(a, b)

    ########################

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
def get_longest_closed_border(sequence, k, pseudo=True):

	n = len(sequence)

	if n == 1:
		return 0

	# calculate k-psuedo-closed border
	if (pseudo):
		# calculate LPM values
		lpm = get_LPM(sequence, k)
		print("LPM:", lpm)

		# calcuate lp values by reversing string
		lsm = get_LPM(sequence[::-1], k)[::-1]
		print("LSM:", lsm)

		# get peak locations in l
		lpm_peaks = get_peaks(lpm)
		print("LPM PEAKS:", lpm_peaks)

		# get peak locations in lp
		lsm_peaks = get_peaks(lsm)
		print("LSM PEAKS:", lsm_peaks)

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
		reallpm = get_LPM(sequence, k)
		reallsm = get_LPM(sequence[::-1], k)[::-1]

		closed_border = -1
		lpm = [-1] * n
		lsm = [-1] * n

		for i in range(0, k + 1):
			lpm = get_next_LPM(lpm, sequence)
			lsm = get_next_LPM(lsm[::-1], sequence[::-1])[::-1]

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
							print("k:", i)
							print("REAL LPM:", reallpm)
							print("PROG LPM:", lpm)
							print("REAL LSM:", reallsm)
							print("PROG LSM:", lsm)
							return closed_border

		return -1

# perform tests
line_count = 0
correct_result_count = 0

for line in open('k_closed_identify_tests.txt'):
	
	values = str.split(line)

	pseudo = (str(values[0]) == 'P')
	k = int(values[1])
	sequence = values[2]
	correct_result = int(values[3])
	
	print(k, sequence)

	closed_border = get_longest_closed_border(sequence, k, pseudo)

	# print result of each test
	if (closed_border >= 0):
	    print("CLOSED BORDER LENGTH = " + str(closed_border))
	else:
	    print("NOT CLOSED")

	# increment test result counts
	if closed_border == correct_result:
		correct_result_count += 1
		print("Correct")
	else:
		print("Incorrect")
	print("")

	line_count += 1

print(str(correct_result_count) + " out of " + str(line_count) + " tests passed")
	
