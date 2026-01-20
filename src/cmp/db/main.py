#!/usr/bin/python3

import numpy as np
from operator import itemgetter

from ase.io import read,write

from cmp.utils import tabulate, show_small_banner, wildcard_match, count_unique, select_atoms
from cmp.db.evaluator_utils import evaluate


def sample(atoms,n_samples,output_name):
	n = len(atoms)

	if '.' in n_samples: N = int(n*float(n_samples))
	else: N = int(n_samples)

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
		'Effective sample rate':round(N/n,3),
	}


def create_tag(atoms,assignment,index=None,debug=None):
	new_tag, expression = assignment.split('=')
	
	# Replace 'energy' in the expression
	if 'energy' in expression:
		E = atoms.get_potential_energy()
		expression = expression.replace('energy', str(E))

	# Replace any info-key in the expression
	for key in atoms.info:
		if key in expression:
			if isinstance(atoms.info[key],(np.ndarray)):
				array_to_list = list(atoms.info[key].flatten('F'))
				expression = expression.replace(key, f'{array_to_list}')
			else:
				expression = expression.replace(key, f'{atoms.info[key]}')

	# Evaluate expression if possible
	try:
		result = evaluate(expression)
	except:
		result = expression
	
	if isinstance(result, list):
		final_tag = ", ".join(map(str, result))
	else:
		final_tag = str(result)
	
	if debug:
		print(final_tag)

	# Assign new tag
	atoms.info[new_tag] = final_tag
	return atoms


def add_tags(atoms,assignment,output_name,debug):
	print(assignment)
	new_atoms = [create_tag(a,assignment, i,debug=debug) for i,a in enumerate(atoms)]
	if output_name is not None:
		write(output_name,new_atoms)


def main(args):
	show_small_banner()
	args = vars(args)
	input_file = args['input']

	# Load file and select search-query
	if args['handle'] is not None:
		handle, value = args['handle']
		print(f'Searching for structures where the info-handle \'{handle}\' matches \'{value}\'')
		atoms, handle_counts = select_atoms(read(input_file, ':'), handle, value)
	else:
		atoms = read(input_file, ':')

	# Create summary dict
	input_summary = {
		'Database size (# structures)':len(atoms),
	}

	# Random sampling
	if args['n_samples'] is not None:
		# Summary
		print(f'\nRandomly sampling from selection.')
		n_samples = args['n_samples']
		if '.' in n_samples:
			input_summary['Sample rate'] = n_samples
		else:
			input_summary['Number of samples'] = n_samples

		# Set seed
		if args['seed'] is not None:
			np.random.seed(args['seed'])
			input_summary['Seed'] = args['seed']

		# Perform random sampling
		output_summary = sample(
			atoms,
			n_samples=args['n_samples'],
			output_name=args['output'],
		)

	
	# Print summaries of inputs and outputs
	tabulate(input_summary,header='\nInput summary:')
	if args['handle'] is not None:
		tabulate(handle_counts,header=f'\nSelected \'{handle}\' info-handles:')
	try:
		tabulate(output_summary,header='\nOutput summary:')
	except:
		pass


	if args['add_info'] is not None:
		print('\nProcessing:')
		add_tags(
			atoms,
			assignment=args['add_info'],
			output_name=args['output'],
			debug=args['debug'],
		)