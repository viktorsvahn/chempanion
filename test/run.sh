#!/bin/sh

cmp mdeq nve argon_start.xyz --steps 1000 --temp 300 --density 0.838
cmp mdeq nvt argon_start.xyz --steps 1000 --temp 300 --density 0.838 --friction=0.001
cmp mdeq npt argon_start.xyz --steps 1000 --temp 300 --pressure 1.0 --taut 0.5 --taup 0.1


cmp vscan a argon_start.xyz -n 10 --max 2
cmp vscan m ec_emc.xyz -n 10 --max 2
