from k_closed_identify import get_longest_closed_border

# perform tests
line_count = 0
correct_result_count = 0

for line in open('correctness_tests.txt'):
	
	values = str.split(line)

	pseudo = (str(values[0]) == 'P')
	k = int(values[1])
	sequence = values[2]
	correct_result = int(values[3])
	
	print(k, sequence)

	for use_nlogn in [True, False]:
		closed_border = get_longest_closed_border(sequence, k, pseudo, use_nlogn)

		# print result of each test
		if (use_nlogn):
			print("O(n log n) RMQs:")
		else:
			print("O(n) RMQs:")
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

print(str(correct_result_count) + " out of " + str(2 * line_count) + " tests passed")