# 2026-11-22 UTC: restarts what died with the old runner's terminal at 07:17 UTC (all BelowNormal, hidden): the leg-1 guard (copier, 12 h cap by exact pid, end markers), the D 19 scan waiter
# (kcl_scan.sh 19 1.40 1.80 1.545995, as armed at 03:07 UTC), and the two samplers (mem_watch.ps1, commit_watch.ps1). The leap's python (35992/23496) is not touched.
$d = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$bash = 'C:\Program Files\Git\bin\bash.exe'
function Start-Bash($name, $cmd) {
  $p = Start-Process $bash -ArgumentList '-c', "`"export PATH=/usr/bin:`$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && $cmd`"" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$d\$name.stdout" -RedirectStandardError "$d\$name.stderr"
  $p.PriorityClass = 'BelowNormal'
  "$name pid $($p.Id) $($p.PriorityClass)"
}
Start-Bash 'leg1_guard' 'bash leg1_guard.sh'
Start-Bash 'kcl_scan_D19b' 'bash kcl_scan.sh 19 1.40 1.80 1.545995'
foreach ($s in 'mem_watch', 'commit_watch') {
  $p = Start-Process 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -ArgumentList '-NoProfile', '-File', "$d\$s.ps1", '-Out', $d -WindowStyle Hidden -PassThru
  $p.PriorityClass = 'BelowNormal'
  "$s pid $($p.Id) $($p.PriorityClass)"
}
