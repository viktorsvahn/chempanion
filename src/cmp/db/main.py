#!/usr/bin/python3

import numpy as np
from operator import itemgetter

from ase.io import read,write

from cmp.utils import tabulate, show_small_banner, wildcard_match, count_unique


def sample(atoms,n_samples,output_name):
	n = len(atoms)

	if '.' in n_samples:
		N = int(n*float(n_samples))
	else:
		N = int(n_samples)

	# Sample
	rand = np.random.choice(np.arange(n), N, replace=False)
	if len(rand) > 0:
		new_atoms = list(
			itemgetter(*rand)(atoms)
		)
		nn = len(new_atoms)

		if output_name is not None:
			write(output_name,new_atoms)

		return {
			'Structures sampled':nn,
			'Sample rate':round(N/n,3),
		}
	else:
		print('\nCould not find any matches! Aborting.')
		quit()


def select_info(atoms,handle,value):
	if '*' in value:
		new_atoms = [a for a in atoms if wildcard_match(value, a.info[handle])]
	else:
		new_atoms = [a for a in atoms if value == a.info[handle]]
	handle_counts = count_unique([a.info[handle] for a in new_atoms])
	return new_atoms, handle_counts


def main(args):
	args = vars(args)	
	input_file = args['input']

	if args['handle'] is not None:
		handle, value = args['handle']
		atoms, handle_counts = select_info(read(input_file, ':'), handle, value)
	else:
		atoms = read(input_file, ':')


	show_small_banner()
	if args['mode'] == 'sample':
		print(f'Sampling from {input_file} using Chempanion.')
		if args['handle'] is not None:
			print(f'Searching for structures where the info-handle \'{handle}\' matches \'{value}\'')

		summary = {
			'Database size (# structures)':len(atoms),
			'Sample rate (# or %)':args['n_samples'],
		}
		if args['seed'] is not None:
			np.random.seed(args['seed'])
			summary['Seed'] = args['seed']

		out = sample(
			atoms,
			n_samples=args['n_samples'],
			output_name=args['output'],
		)

	
	tabulate(summary,header='\nInput summary:')
	if args['handle'] is not None:
		tabulate(handle_counts,header=f'Selected \'{handle}\' info-handles:')
	tabulate(out,header='Output summary:')
