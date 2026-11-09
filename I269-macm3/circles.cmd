cd ~/Source/choptuik-large-d && PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH && R=../choptuik-large-d-raw/I269-macm3
PATH=$PATH caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up10_D55.0351.npz 0.06118,3.85263,0.3 2.04768412771239,0,0.2 --M=40 --kf=23 --n0=20 --fmax=1e-15 --tag=D55.0351_M40_kf23 --data=$R/D55/data > $R/D55/circles.log 2>&1
echo "circles D55 exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
PATH=$PATH caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 2.0073,0.9727,0.2 2.043532530673195,0,0.2 --M=40 --kf=23 --n0=20 --fmax=1e-15 --tag=D61.0264_M40_kf23 --data=$R/D61/data > $R/D61/circles.log 2>&1
echo "circles D61 exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
