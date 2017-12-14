import random
import sys

alphabet = "acgt"

if (len(sys.argv) < 2):
	print("Must provide integer length as argument")
	sys.exit(-1)

length = int(sys.argv[1])

with open("chr1_sample.txt", "r") as fd:
    lines = fd.read().splitlines()
    data = "".join(lines)

output = data[0:length]

F = open('realDNA.out', 'w')
F.write(output)
F.close()