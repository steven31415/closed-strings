import random
import sys

alphabet = "acgt"

if (len(sys.argv) < 2):
	print("Must provide integer length as argument")
	sys.exit(-1)

length = int(sys.argv[1])

output = ""
for i in range(0, length):
	output += random.choice(alphabet)

F = open('randDNA.out', 'w')
F.write(output)
F.close()

