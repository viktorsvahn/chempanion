#!/usr/bin/python3

import numpy as np
from operator import itemgetter

from ase.io import read,write

from cmp.utils import tabulate


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
	
	atoms = read(args['input'], ':')
	np.random.seed(args['seed'])
		

	if args['mode'] == 'sample':
		summary = {
			'Database size (# structures)':len(atoms),
			'Sample rate (# or %)':args['n_samples'],
			'Seed':np.random.get_state()[1][2],
			#'test':[0,1,2,3],
		}

		out = sample(
			atoms,
			n_samples=args['n_samples'],
			output_name=args['output'],
		)
	
	tabulate(summary,header='Input summary:')
	tabulate(out,header='Output summary:')
