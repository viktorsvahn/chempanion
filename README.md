# Chempanion
This package consits of a set of tools that can be useful for molecular dynamics simulations. It includes features for quickly equilibrating atomic structures that have been generated elsewhere using, e.g., the atomic simulation environment (ASE) or Packmol. The volume-scan and random sampling tools are useful when it comes to generating datasets intended for machine learning purposes.

This package is based on ASE and although it can be used to run MD in different ensembles, the results should not be subject to rigorous interpretation. The NVT ensemble simulation uses a Langevin thermostat, and the NPT ensemble simulation is based on the Berendsen thermostat/barostat, both of which can be used during equilibration but not production.

**Currently the equilibration is based on a Lennard-Jones potential.**

For instructions on usage, call `cmp -h` in a terminal environment.

# Modules
## vscan
Create structures with expanded volumes using either atomic or molecular centre-of-mass coordinates.

## db
This module is of general purpose and supports the following for ASE-type exyz-format databases:
- Select structures based on info tags
- Random sampling/selection of structures
- Add new info-tags (see below)

New info-tags are added by calling `cmp db filename.xyz --add-info new_tag=some_string`. If some string has a sub-string that matches an already present info-key, the program will substitute this sub-string for the actual value associated with that key. For example, if the `some_string` contains the word 'energy', this part will be replaced by the actual energy of that structure. Furtermore, any mathematical operators part of `some_string` will be evaluated. As a result, `cmp db filename.xyz --add-info new_tag=2*energy` will create a `new_tag` in all structures that is equal to two times the energy of said structure. This will work for the energy as weel as any key present in atoms.info. If unable to evaluate `some_string` as intended, the program will simply add it as a string.

## mdeq
Equilibrate temperature, pressure or total energy in MD structures. This is experimental and currently only supports a Lennard-Jones pair potential. Please use at your own discretion. 
