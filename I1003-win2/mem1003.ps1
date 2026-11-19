# glue (read only): free physical memory in GiB, and the summed working set in GiB and the count of the process tree under the root pid (the venv launcher stub of an amp_flint_par run, its main python and the spawn workers).
param([int]$Root)
$all = Get-CimInstance Win32_Process
$ids = New-Object System.Collections.Generic.HashSet[int]
if ($all | Where-Object { [int]$_.ProcessId -eq $Root }) { [void]$ids.Add($Root) }
do { $n = $ids.Count; foreach ($p in $all) { if ($ids.Contains([int]$p.ParentProcessId)) { [void]$ids.Add([int]$p.ProcessId) } } } while ($ids.Count -gt $n)
$ws = 0; $c = 0
foreach ($p in $all) { if ($ids.Contains([int]$p.ProcessId)) { $ws += [int64]$p.WorkingSetSize; $c++ } }
$free = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
'{0:N1} {1:N2} {2}' -f $free, ($ws / 1GB), $c
