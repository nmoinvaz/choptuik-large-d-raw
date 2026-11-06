#!/bin/bash
# the remaining checks in order: (d) the chain step and its restart, (c) the control, (e) before and after
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
bash $A/run_d.sh
bash $A/run_checks.sh c e_before e_after
