# #1080 x2 check (ii): zero_mp.py at r1 0.2, --iters=0 (centre at both precisions, the 4 offsets, the unapplied step), from
#  main:    the located point = walk_x2.jsonl's last row (it 7): A, wf and its F3 (42 digits)
#  control: walk_x2.jsonl's row it 6 (1.6e-8 from the zero): must read NOT located
# Both started at once, 3 processes each, BelowNormal, cap 4 h each (killed by pid). Code: wip/i1080-x2 10a5854f.
$R = 'D:\choptuik-raw-i1080\I1080-win2'
$WT = 'D:\choptuik-i1080x2\solver\inner_stokes'
$PY = 'C:\Users\nathan\source\venv-i962\Scripts\python.exe'
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'
function Step($s) { Add-Content -Path "$R\steps_ii.txt" -Value ("{0} UTC {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $s) }
$head = (& git -C 'D:\choptuik-i1080x2' rev-parse --short=8 HEAD)
if ($head -ne '10a5854f') { Step "STOP: HEAD $head, not 10a5854f"; exit 9 }
foreach ($f in 'ii_x2_r02.jsonl', 'ii_ctl_row6_r02.jsonl') { if (Test-Path "$R\$f") { Step "STOP: $f exists"; exit 9 } }
$code = @"
import json, sys
rows = [json.loads(l) for l in open(r'$R\walk_x2.jsonl') if l.strip()]
for name, it in (('x2', 7), ('ctl', 6)):
    r = [q for q in rows if q['it'] == it][0]
    print(name, repr(r['A']), repr(r['wf']), ','.join(r['F3']))
"@
$lines = & $PY -c $code
Step "inputs: $($lines -join ' | ')"
$procs = @()
foreach ($ln in $lines) {
    $t = $ln -split ' '
    $name = $t[0]; $out = if ($name -eq 'x2') { "$R\ii_x2_r02.jsonl" } else { "$R\ii_ctl_row6_r02.jsonl" }
    $a = @('-u', 'zero_mp.py', $t[1], $t[2], '-', $out, '--M=5', "--v0=$($t[3])", '--procs=3', '--iters=0', '--r1=0.2')
    $log = if ($name -eq 'x2') { "$R\logs\ii_x2_r02" } else { "$R\logs\ii_ctl_row6_r02" }
    $p = Start-Process -FilePath $PY -ArgumentList $a -WorkingDirectory $WT -NoNewWindow -PassThru -RedirectStandardOutput "$log.log" -RedirectStandardError "$log.err"
    $null = $p.Handle
    $p.PriorityClass = 'BelowNormal'
    Step "$name start pid $($p.Id)"
    Set-Content -Path "$R\ii_$name.pid" -Value $p.Id
    $procs += [pscustomobject]@{ n = $name; p = $p }
}
$t0 = [DateTime]::UtcNow
foreach ($e in $procs) {
    $left = [int](14400 - ([DateTime]::UtcNow - $t0).TotalSeconds); if ($left -lt 1) { $left = 1 }
    if (-not $e.p.WaitForExit($left * 1000)) { & taskkill /T /F /PID $e.p.Id | Out-Null; Step "$($e.n) CAP: killed pid $($e.p.Id)"; Set-Content "$R\ii_$($e.n).exit" 'cap' }
    else { Step "$($e.n) exit $($e.p.ExitCode)"; Set-Content "$R\ii_$($e.n).exit" $e.p.ExitCode }
}
