# #1080 x2: the extended-precision polish of the float64 continuation end (value_mp.py pointv, M = 5), one process,
# BelowNormal, cap 6 h (killed by exact pid at the cap). Started by WMI (Win32_Process Create). Log: logs/polish_x2.*
$R = 'D:\choptuik-raw-i1080\I1080-win2'
$WT = 'D:\choptuik-i1080x2\solver\inner_stokes'
$PY = 'C:\Users\nathan\source\venv-i962\Scripts\python.exe'
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'; $env:VALUE_MP_PROGRESS = '1'
function Step($s) { Add-Content -Path "$R\steps_polish.txt" -Value ("{0} UTC {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $s) }
$head = (& git -C 'D:\choptuik-i1080x2' rev-parse --short=8 HEAD)
if ($head -ne 'dd00111a') { Step "STOP: HEAD $head, not dd00111a"; exit 9 }
$a = @('-u', 'value_mp.py', 'pointv', '3.526473056695715', '0.211497981391215', '--M=5',
       '--v=1.0648860637097008,-0.02329008304258205,0.48804863057121334,0.011482111329677719')
$p = Start-Process -FilePath $PY -ArgumentList $a -WorkingDirectory $WT -NoNewWindow -PassThru `
     -RedirectStandardOutput "$R\logs\polish_x2.json" -RedirectStandardError "$R\logs\polish_x2_progress.log"
$p.PriorityClass = 'BelowNormal'
Step "start pid $($p.Id), HEAD $head, BelowNormal, cap 21600 s"
Set-Content -Path "$R\polish_x2.pid" -Value $p.Id
$done = $p.WaitForExit(21600 * 1000)
if (-not $done) { & taskkill /T /F /PID $p.Id | Out-Null; Step "CAP: killed pid $($p.Id) after 21600 s"; Set-Content "$R\polish_x2.exit" 'cap'; exit 3 }
Step "exit $($p.ExitCode), cpu $([int]$p.TotalProcessorTime.TotalSeconds) s"
Set-Content -Path "$R\polish_x2.exit" -Value $p.ExitCode
