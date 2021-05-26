mylist = ['a', 'aa', 'aaa']
current_idx = 0

# solution:
for index, element in enumerate(mylist):
	if index == len(mylist) - 1:
		# Case: this is teh last element
		pass
	else:
		myvar = mylist[index + 1]
		if len(myvar) == 2:
			# Case: this not the last element and the length of next element is 2
			pass

		else:
			# Case: this is not the last element and the length of next element is not 2
			pass

for element in mylist:
	if current_idx == len(mylist)-1:
		# Case: this is teh last element
		pass

	myvar = mylist[current_idx+1]
	elif len(myvar) == 2:
		# Case: this nto teh last element and the next element length is 2
		pass

	else:
		# Case: this is not the last element and the next element length is not 2 ()
		pass

	current_idx += 1

