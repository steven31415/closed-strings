from k_closed_identify import get_longest_closed_border

# perform tests
line_count = 0
correct_result_count = 0

for line in open('tests.txt'):
	
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