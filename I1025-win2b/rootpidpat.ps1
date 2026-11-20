# glue: prints the pid of the root python.exe (the venv launcher stub) of the running command whose command line contains both -Script and -Pat, i.e. the one whose parent is not itself such a python
param([string]$Script, [string]$Pat)
$a = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like "*$Script*" -and $_.CommandLine -like "*$Pat*" })
if ($a.Count -gt 0) { $ids = @($a | ForEach-Object { $_.ProcessId }); ($a | Where-Object { $ids -notcontains $_.ParentProcessId } | Select-Object -First 1).ProcessId }
