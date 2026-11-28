{
cd ~/Source/choptuik-large-d/hp || exit 1
echo "start $(date -u '+%Y-%m-%d %H:%M:%S')"
timeout 7200 nice -n 10 ~/venv-314/bin/python3 ladder_fit.py planted --ladders=X $(cat I1098-mac-a/fit17/ladder_args.txt) --sigmas=1e-25 --seeds=20 --out=I1098-mac-a/fit17/planted17.json > I1098-mac-a/fit17/planted17.log 2>&1
echo "planted rc $? $(date -u '+%H:%M:%S')"
F=$(~/venv-314/bin/python3 -c "import json,sys; d=json.load(open('I1098-mac-a/fit17/planted17.json')); L=d['ladders']; print(L[list(L)[0]]['F'])" 2>/dev/null)
echo "F $F"
timeout 3600 nice -n 10 ~/venv-314/bin/python3 ladder_fit.py real I1098-mac-a/ladder_records/D* --F=${F:-3} --out=I1098-mac-a/fit17/real17.json > I1098-mac-a/fit17/real17.log 2>&1
echo "real rc $? $(date -u '+%H:%M:%S')"
timeout 3600 nice -n 10 ~/venv-314/bin/python3 ladder_pade.py real I1098-mac-a/ladder_records/D* --Ms=1,2,3 > I1098-mac-a/fit17/pade17.log 2>&1
echo "pade rc $? $(date -u '+%H:%M:%S')"
exit
}
