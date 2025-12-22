#!/bin/sh

mdeq nve argon_start.xyz --steps 1000 --temp 300 --density 0.838

mdeq nvt argon_start.xyz --steps 1000 --temp 300 --density 0.838 --friction=0.001

mdeq npt argon_start.xyz --steps 1000 --temp 300 --pressure 1.0 --taut 0.5 --taup 0.1
