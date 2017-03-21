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
            return sys.maxint
        elif a <= l and r <= b:
            return self.dat[k]
        else:
            return min(self.query_help(a, b, 2 * k + 1, l, (l + r)>>1),
                        self.query_help(a, b, 2 * k + 2, (l + r) >> 1, r))



# l value generating function
def generate_l_values(sequence, k):

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

    l = [0] * n

    for i in range(1, n):

        # perform up to k + 1 LCP queries for each suffix
        for j in range(0, k + 1):

            # perform an LCP and update next location to check
            l[i] = l[i] + LCP(0 + l[i], i + l[i]) + 1

            # stop if end of string is reached
            if l[i] > n - i:
                break

        # remove 1 to ensure final mismatch is not included
        l[i] = l[i] - 1

    return l



# determine positions in an array that are larger than all previous values in the array
def get_peaks(array):
    n = len(array)
    peaks = [0] * n

    max_val = array[0]
    for i in range(0, n):
        if array[i] >= max_val:
            peaks[i] = True
            max_val = array[i]
        else:
            peaks[i] = False

    return peaks



# get string input and k parameter
sequence = 'gtgagaggtg'
k = 0
n = len(sequence)

# calculate l values
l = generate_l_values(sequence, k)
print("l", l)

# calcuate lp values by reversing string
lp = generate_l_values(sequence[::-1], k)[::-1]
print("lp", lp)

# get peak locations in l
l_peaks = get_peaks(l)
print("l_peaks", l_peaks)

# get peak locations in lp
lp_peaks = get_peaks(lp[::-1])[::-1]
print("lp_peaks", lp_peaks)



# check conditions
closed_border = -1

for j in range(2, n):
    # 1st condition
    if j + l[j] == n:
        # 2nd condition
        if l_peaks[j]:
            # 3rd condition
            if lp_peaks[j]:
                closed_border = n-j
                break
            else:
                continue
        else:
            continue
    else:
        continue

if (closed_border >= 0):
    print("CLOSED BORDER LENGTH = " + str(closed_border))
else:
    print("NOT CLOSED")



