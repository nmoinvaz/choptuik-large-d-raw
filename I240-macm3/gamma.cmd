cd ~/Source/choptuik-large-d && PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH caffeinate -is nice -n 10 python3 hp/gamma_dd.py ../choptuik-large-d-raw/I240-macm3/gamma.jsonl hp/data/states/up10_D54.0414.npz > ../choptuik-large-d-raw/I240-macm3/gamma.log 2>&1
echo "gamma_dd exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> ../choptuik-large-d-raw/I240-macm3/exits.txt
