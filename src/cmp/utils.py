#!/usr/bin/python3


def tabulate(dictionary,header='',tab_width=4):
	max_key_spacing = max(len(key) for key in dictionary)+tab_width
	max_val_spacing = max(len(str(val)) for val in dictionary.values() if type(val) is not list)
	total_width = max_key_spacing+max_val_spacing+3

	print(header)
	print('+'+'-'*total_width+'+')

	for key, value in dictionary.items():		
		a = ' '*(max_key_spacing-len(key))
		b = ' '*(max_val_spacing-len(str(value))+1)
		if type(value) == list:
			for i,val in enumerate(value):
				alpha = ' '*(len(key)+1)
				beta = ' '*(max_val_spacing-len(str(val))+1)
				if i == 0:
					print(f'| {key}:{a}{val}{beta}|')
				else:
					print(f'| {alpha}{a}{val}{beta}|')
		else:
			print(f'| {key}:{a}{value}{b}|')
	
	print('+'+'-'*total_width+'+\n')