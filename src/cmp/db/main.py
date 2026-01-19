#!/usr/bin/python3

import numpy as np
from operator import itemgetter

from ase.io import read,write

from cmp.utils import tabulate, show_small_banner, wildcard_match, count_unique, select_atoms


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


def create_tag(atoms,assignment):
	new_tag, statement = assignment.split('=')
	
	# Replace 'energy' in the statement
	if 'energy' in statement:
		E = atoms.get_potential_energy()
		statement = statement.replace('energy', str(E))

	# Replace any info-key in the statement
	for key in atoms.info:
		if key in statement:
			statement = statement.replace(key, f'{atoms.info[key]}')
			#eval_statement = True

	# Evaluate statement if possible
	try:
		final_tag = eval(statement)
	except:
		final_tag = statement
	
	# Assign new tag
	atoms.info[new_tag] = final_tag
	return atoms


def add_tags(atoms,assignment,output_name):
	print(assignment)
	new_atoms = [create_tag(a,assignment) for a in atoms]
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
			output_name=args['output']
		)