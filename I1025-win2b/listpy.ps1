param([string]$Pat)
# lists python.exe processes whose command line contains -Pat, with the parent's liveness
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like "*$Pat*" } | ForEach-Object {
  $par = Get-Process -Id $_.ParentProcessId -ErrorAction SilentlyContinue
  '{0} parent {1} (parent alive: {2}) started {3}' -f $_.ProcessId, $_.ParentProcessId, [bool]$par, $_.CreationDate
}
