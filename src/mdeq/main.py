#!/usr/bin/python3


#import sys
import pandas as pd

from mdeq.parser import argument_parser
from mdeq.temp import nvt



def main():
	input_args = argument_parser()
	args = vars(input_args)
	print(args)

	if args['ensemble'].lower() == 'nvt':
		nvt(
			input_name=args['input'],
			steps=args['steps'],
			T=args['temperature'],
			dt=args['dt'],
			cell_scale=args['scale'],
			friction=args['friction'],
			output_name=args['output'],
		)



if __name__ == '__main__':
	main()