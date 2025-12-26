#!/usr/bin/python3

import numpy as np

from ase.io import read,write

from cmp.utils import show_small_banner


def vscan(atoms,mode,min_scale,max_scale,npoints,output_name):
	new_atoms = []
	if mode == 'a':
		print('Atomic mode (atomic coordinates are being scaled)')
	elif mode == 'm':
		print('Molecular mode (atomic coordinates are being scaled relative to molecular centre of mass)')

	for x in np.linspace(min_scale,max_scale,npoints):
		ats = atoms.copy()
		ats.info = atoms.info
		ats.info['config_type'] = 'vscan'

		if mode == 'a':
			ats.set_cell(ats.cell*x, scale_atoms=True)
			new_atoms.append(ats)

		elif mode == 'm':
			if 'molID' not in ats.arrays:
				print('Structure has no molIDs! Aborting.')
				quit()
			
			molIDs = set(ats.arrays['molID'])
			com = np.array(
				[
					ats[ats.arrays['molID']==i].get_center_of_mass()*(x-1)
					for i in molIDs
					for _ in range(len(ats[ats.arrays['molID']==i]))
				]
			)
			ats.positions += com
			ats.set_cell(ats.cell*x, scale_atoms=False)
			new_atoms.append(ats)
		print(f'Scale factor = {x:.2f}\tCell volume = {ats.get_volume():.3f} Å3')
	
	return new_atoms



def generate_volume_scans(atoms,mode,min_scale,max_scale,npoints,output_name):
	new_atoms = []

	if type(atoms) != list:
		atoms = [atoms]

	for i,a in enumerate(atoms):
		if len(atoms) > 1:
			print(f'\nScanning structure {i+1}')
		scan = vscan(
			atoms=a,
			mode=mode,
			min_scale=min_scale,
			max_scale=max_scale,
			npoints=npoints,
			output_name=output_name,
		)
		new_atoms += scan
	
	if output_name is not None:
		write(output_name,new_atoms)


def main(args):
	args = vars(args)
	
	input_file = args['input']
	index = args['index']
	atoms = read(input_file, index)

	show_small_banner()
	if index == ':':
		pass
		print(f'Generating a volume-scan of all structures in {input_file} using Chempanion.\n')
	else:
		idx = int(index)+1
		if idx == 1:
			suffix = 'st'
		elif idx == 2:
			suffix = 'nd'
		elif idx > 2:
			suffix = 'th'
		print(f'Generating a volume-scan of the {idx}{suffix} structure in {input_file} using Chempanion.\n')

	generate_volume_scans(
		atoms,
		mode=args['mode'],
		min_scale=args['min'],
		max_scale=args['max'],
		npoints=args['num_points'],
		output_name=args['output'],
	)