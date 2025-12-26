#!/usr/bin/python3

import numpy as np
from operator import itemgetter

from ase.io import read,write

from cmp.utils import tabulate, show_small_banner


def sample(atoms,n_samples,output_name):
	n = len(atoms)

	if '.' in n_samples:
		N = int(n*float(n_samples))
	else:
		N = int(n_samples)

	# Sample
	rand = np.random.choice(np.arange(n), N, replace=False)
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


def main(args):
	args = vars(args)
	
	input_file = args['input']
	atoms = read(input_file, ':')

	show_small_banner()
	if args['mode'] == 'sample':
		print(f'Sampling from {input_file} using Chempanion.\n')
		summary = {
			'Database size (# structures)':len(atoms),
			'Sample rate (# or %)':args['n_samples'],
			#'test':[0,1,2,3],
		}
		if args['seed'] is not None:
			np.random.seed(args['seed'])
			summary['Seed'] = args['seed']

		out = sample(
			atoms,
			n_samples=args['n_samples'],
			output_name=args['output'],
		)
	
	tabulate(summary,header='Input summary:')
	tabulate(out,header='Output summary:')
