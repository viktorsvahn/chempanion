#!/bin/sh
cmp
cmp -h

cmp mdeq -h
cmp mdeq nve argon_start.xyz -n 100 --temperature 300 --density 0.838
cmp mdeq nvt argon_start.xyz -n 100 --vscale 1.05 --temperature 300 --density 0.838 --friction=0.001
cmp mdeq npt argon_start.xyz -n 100 --temperature 300 --pressure 1.0 --taut 0.5 --taup 0.1

cmp vscan -h
cmp vscan a argon_start.xyz -n 10 --max 2 -i 0
cmp vscan m ec_emc.xyz -n 10 --max 2

cmp db -h
cmp db sample db.xyz -n 0.5
cmp db sample db.xyz -n 3 --seed 123
