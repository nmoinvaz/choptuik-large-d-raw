# run_one.ps1 M XI1 [OUTDIR]: first_order_run.py M --xi1=XI1 --fresh, one thread, BelowNormal, 4 h cap, with wall, cpu,
# peak memory and exit code of the interpreter. The venv's python.exe is a launcher that starts the real interpreter as a
# child, so the stats are taken from that child (the first version of this script, which watched the launcher,
# gave cpu 0, 4 MB and a null exit code; its stats files are replaced by those of the rerun in rerun_stats/).
param([int]$M, [string]$Xi1, [string]$OutDir = 'D:\choptuik-large-d-raw-i385\I385-win2')
$ErrorActionPreference = 'Stop'
(Get-Process -Id $PID).PriorityClass = 'BelowNormal'            # the launcher and its child inherit it
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'
$env:PYTHONIOENCODING = 'utf-8'
$py = 'C:\Users\nathan\Source\venv-md510\Scripts\python.exe'
$tag = "M${M}_xi${Xi1}"
$out = "$OutDir\first_order_$tag.json"; $log = "$OutDir\first_order_$tag.log"; $err = "$OutDir\first_order_$tag.err"
$stats = "$OutDir\first_order_$tag.stats.json"
New-Item -ItemType Directory -Force $OutDir | Out-Null
$t0 = Get-Date
$p = Start-Process -FilePath $py -ArgumentList @('-u', 'first_order_run.py', "$M", "--xi1=$Xi1", '--fresh', "--out=$out") `
    -WorkingDirectory 'D:\choptuik-i385\solver\inner_pert' -RedirectStandardOutput $log -RedirectStandardError $err `
    -PassThru -WindowStyle Hidden
$null = $p.Handle                                               # cache the handle so ExitCode is readable
function Get-Deepest([int]$id) {
    $k = Get-CimInstance Win32_Process -Filter "ParentProcessId=$id AND Name='python.exe'" | Select-Object -First 1
    if ($k) { return Get-Deepest $k.ProcessId } else { return $id }
}
$c = $null
while (-not $c -and -not $p.HasExited) {
    $d = Get-Deepest $p.Id
    if ($d -ne $p.Id) { Start-Sleep -Milliseconds 500; $d = Get-Deepest $p.Id; $c = [System.Diagnostics.Process]::GetProcessById($d); $null = $c.Handle }
    else { Start-Sleep -Milliseconds 20 }
}
"$tag launcher pid $($p.Id), interpreter pid $($c.Id), started $($t0.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC, priority $($c.PriorityClass)" | Write-Host
$prio = "$($c.PriorityClass)"
$peak = 0; $cap = $t0.AddHours(4); $capped = $false
while (-not $c.HasExited) {
    Start-Sleep -Milliseconds 200
    try { $c.Refresh(); if ($c.PeakWorkingSet64 -gt $peak) { $peak = $c.PeakWorkingSet64 } } catch {}
    if ((Get-Date) -gt $cap) { Stop-Process -Id $c.Id -Force; $capped = $true; "$tag hit the 4 h cap, killed pid $($c.Id)" | Write-Host; break }
}
$c.WaitForExit(); $p.WaitForExit()
$t1 = Get-Date
$s = [ordered]@{
    tag = $tag; launcher_pid = $p.Id; interpreter_pid = $c.Id; priority = $prio; capped = $capped
    exit_code_interpreter = $c.ExitCode; exit_code_launcher = $p.ExitCode
    start_utc = $t0.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss'); end_utc = $t1.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')
    wall_s = [math]::Round(($t1 - $t0).TotalSeconds, 1); cpu_s = [math]::Round($c.TotalProcessorTime.TotalSeconds, 2)
    peak_working_set_MB = [math]::Round($peak / 1MB, 1)
}
$s | ConvertTo-Json | Set-Content -Encoding utf8 $stats
$s | ConvertTo-Json -Compress | Write-Host
exit $c.ExitCode
