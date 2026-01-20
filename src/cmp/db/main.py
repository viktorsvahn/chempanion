import numpy as np

from ase.io import read

from cmp.utils import tabulate, show_small_banner, wildcard_match, count_unique, select_atoms
from cmp.db.utils import sample, add_tags


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