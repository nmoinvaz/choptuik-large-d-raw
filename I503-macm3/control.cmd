cd ~/Source/choptuik-large-d && export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
out=../choptuik-large-d-raw/I503-macm3
for spec in "0.0075 40" "0.0075 80" "0.00375 20"; do
    set -- $spec
    caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,$1 --M=48 --kf=27 --n0=$2 --fmax=1e-15 --tag=D61.0264_M48_kf27 --data=$out/data >> $out/control.log 2>&1
    echo "control R $1 n0 $2 exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt
done
