#!/bin/python3

import sys
import re
import math

#Inaccurate on large numbers due to round-off errors

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		sys.exit('Usage: %s filename' % sys.argv[0])

	n = 0
	sum = 0
	sq_sum = 0
	regex = re.compile("open .* (\d+) usec")
	with open(sys.argv[1], "r") as f:
		for line in f:
			m = regex.match(line)
			if m is not None:
				elem = int(m.group(1))
				sum += elem
				sq_sum += elem*elem
				n += 1

		mean = sum / n
		std_dev = math.sqrt(sq_sum / n - mean * mean)

		print("mean:", mean)
		print("standart deviation:", std_dev)
