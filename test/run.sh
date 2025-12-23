#!/bin/sh

ccm mdeq nve argon_start.xyz --steps 1000 --temp 300 --density 0.838
ccm mdeq nvt argon_start.xyz --steps 1000 --temp 300 --density 0.838 --friction=0.001
ccm mdeq npt argon_start.xyz --steps 1000 --temp 300 --pressure 1.0 --taut 0.5 --taup 0.1


ccm vscan a argon_start.xyz -n 10 --max 2
ccm vscan m mols.xyz -n 10 --max 2
