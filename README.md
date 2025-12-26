# Chempanion
This package consits of a set of tools that can be useful for molecular dynamics simulations. It includes features for quickly equilibrating atomic structures that have been generated elsewhere using, e.g., the atomic simulation environment (ASE) or Packmol. The volume-scan and random sampling tools are useful when it comes to generating datasets intended for machine learning purposes.

This package is based on ASE and although it can be used to run MD in different ensembles, the results should not be subject to rigorous interpretation. The NVT ensemble simulation uses a Langevin thermostat, and the NPT ensemble simulation is based on the Berendsen thermostat/barostat, both of which can be used during equilibration but not production.

**Currently the equilibration is based on a Lennard-Jones potential.**

For instructions on usage, call `cmp -h` in a terminal environment.
