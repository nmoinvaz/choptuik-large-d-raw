cd ~/Source/choptuik-large-d && PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH caffeinate -is nice -n 10 python3 hp/gamma_dd.py ../choptuik-large-d-raw/I237-macm3/D53/gamma.jsonl hp/data/states/up10_D53.7914.npz > ../choptuik-large-d-raw/I237-macm3/D53/gamma.log 2>&1
echo "D53 gamma_dd exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> ../choptuik-large-d-raw/I237-macm3/exits.txt
