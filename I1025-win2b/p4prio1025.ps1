# glue for p4cap1025.sh: the pinned driver starts each row with `nice -n 10`, which Git Bash turns into the Idle priority class; the coordinator ordered BelowNormal.
# Sets every running p4_hybrid.py python.exe (the venv launcher stub and its child) that is Idle to BelowNormal and prints one line per change: "pid IdleToBelowNormal".
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*p4_hybrid.py*' } | ForEach-Object {
  $p = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
  if ($p -and $p.PriorityClass -eq 'Idle') { $p.PriorityClass = 'BelowNormal'; '{0} IdleToBelowNormal' -f $_.ProcessId }
}
