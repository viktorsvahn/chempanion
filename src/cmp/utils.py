#!/usr/bin/python3

def show_small_banner():
    small_banner = r"""
  ___ _                              _          
 / __| |_  ___ _ __  _ __  __ _ _ _ (_)___ _ _  
| (__| ' \/ -_) '  \| '_ \/ _` | ' \| / _ \ ' \ 
 \___|_||_\___|_|_|_| .__/\__,_|_||_|_\___/_||_|
                    |_|                         

    """
    print(small_banner)


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
	
	print('+'+'-'*total_width+'+')


def wildcard_match(pattern, string):
	sub_patterns = pattern.split('*')
	string = str(string)

	# Beginning with wildcard
	if sub_patterns[0] != '':
		start = sub_patterns.pop(0)
		starts_with = string.startswith(start)
	else:
		starts_with = True
	
	# Ending with wildcard
	if sub_patterns[-1] != '':
		end = sub_patterns.pop(-1)
		ends_with = string.endswith(end)
	else:
		ends_with = True
	
	# Check beginning, end and middle wildcard match
	return starts_with and ends_with and all(
		p in string for p in sub_patterns
	)


def count_unique(arr):
	items = set(arr)
	counts = {
		str(item):arr.count(item) for item in items
	}
	return counts