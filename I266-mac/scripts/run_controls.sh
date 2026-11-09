#!/bin/bash
# The projection's control (#266): a planted difference along the third weakest direction must come back (plant),
# and with the amplitudes swapped the same check must fail (plant_strong). From the worktree root.
RAW=/Users/nathan/Source/choptuik-large-d-raw/I266-mac
S=$RAW/states/up8_D50.0075_M48_r2.npz
G=$RAW/states/up8_D50.0075_M48_gamma.npz
bash $RAW/scripts/run_cmd.sh control_plant analyze $RAW/controls.jsonl $G $S --mutate=plant
bash $RAW/scripts/run_cmd.sh control_plant_strong analyze $RAW/controls.jsonl $G $S --mutate=plant_strong
