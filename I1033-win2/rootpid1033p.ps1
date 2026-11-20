# glue: prints the pid of the root python.exe (the venv launcher stub) of the running tau_map_gain.py command whose command line contains -Pat (the job's own --out file name), i.e. the one whose parent is not itself such a python
param([string]$Pat)
$a = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*tau_map_gain.py*' -and $_.CommandLine -like "*$Pat*" })
if ($a.Count -gt 0) { $ids = @($a | ForEach-Object { $_.ProcessId }); ($a | Where-Object { $ids -notcontains $_.ParentProcessId } | Select-Object -First 1).ProcessId }
