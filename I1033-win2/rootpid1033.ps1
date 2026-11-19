# glue: prints the pid of the root python.exe (the venv launcher stub) of the running tau_map_gain.py command, i.e. the one whose parent is not itself such a python
$a = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*tau_map_gain.py*' })
if ($a.Count -gt 0) { $ids = @($a | ForEach-Object { $_.ProcessId }); ($a | Where-Object { $ids -notcontains $_.ParentProcessId } | Select-Object -First 1).ProcessId }
