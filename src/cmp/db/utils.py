import numpy as np
from operator import itemgetter

from cmp.db.evaluator_utils import evaluate


def sample(atoms,n_samples):
	n = len(atoms)

	if '.' in n_samples: N = int(n*float(n_samples))
	else: N = int(n_samples)

	# Sample
	rand = np.random.choice(np.arange(n), N, replace=False)
	new_atoms = list(
		itemgetter(*rand)(atoms)
	)
	nn = len(new_atoms)

	return new_atoms, {
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


def add_tags(atoms,assignment,debug):
	print(assignment)
	new_atoms = [create_tag(a,assignment, i,debug=debug) for i,a in enumerate(atoms)]
	return new_atoms
