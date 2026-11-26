# #1080 walk d diagnosis: iteration 1's centre call with a line per residual call. One process, BelowNormal, cap 3600 s.
$R = 'D:\choptuik-raw-i1080\I1080-win2\control_d\diag'
$PYEXE = 'C:\Users\nathan\source\venv-i962\Scripts\python.exe'
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'
function Step($s) { Add-Content -Path "$R\steps_diag_it1.txt" -Value ("{0} UTC {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $s) }
$head = (& git -C 'D:\choptuik-i1080d' rev-parse --short=8 HEAD)
$blob = (& git -C 'D:\choptuik-i1080d' hash-object --no-filters 'D:\choptuik-i1080d\solver\inner_stokes\value_mp.py').Substring(0, 8)
if ($head -ne '73dcf243' -or $blob -ne '56bb4856') { Step "STOP: HEAD $head value_mp $blob"; exit 9 }
$p = Start-Process -FilePath $PYEXE -ArgumentList @('-u', "$R\diag_it1.py", "$R\..\control_walk_d.jsonl") -WorkingDirectory $R -NoNewWindow -PassThru `
     -RedirectStandardOutput "$R\diag_it1.log" -RedirectStandardError "$R\diag_it1.err"
$null = $p.Handle
$p.PriorityClass = 'BelowNormal'
Step "diag start pid $($p.Id), BelowNormal, cap 3600 s, HEAD $head value_mp $blob"
Set-Content -Path "$R\diag_it1.pid" -Value $p.Id
if (-not $p.WaitForExit(3600 * 1000)) { & taskkill /T /F /PID $p.Id | Out-Null; Step "CAP: killed pid $($p.Id) after 3600 s"; Set-Content "$R\diag_it1.exit" 'cap'; exit 3 }
Step "diag exit $($p.ExitCode)"
Set-Content -Path "$R\diag_it1.exit" -Value $p.ExitCode
