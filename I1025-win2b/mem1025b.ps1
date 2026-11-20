# glue (read only): "free_GiB commit_GiB commit_limit_GiB ws_GiB nprocs rustc_max_ws_GiB" for a root pid's process tree (the D 16.75 solve), free physical memory, commit charge (TotalVirtualMemorySize - FreeVirtualMemory), and the largest rustc working set
param([int]$Root)
$all = Get-CimInstance Win32_Process
$ids = New-Object System.Collections.Generic.HashSet[int]
if ($all | Where-Object { [int]$_.ProcessId -eq $Root }) { [void]$ids.Add($Root) }
do { $n = $ids.Count; foreach ($p in $all) { if ($ids.Contains([int]$p.ParentProcessId)) { [void]$ids.Add([int]$p.ProcessId) } } } while ($ids.Count -gt $n)
$ws = 0; $c = 0; $rs = 0
foreach ($p in $all) {
  if ($ids.Contains([int]$p.ProcessId)) { $ws += [int64]$p.WorkingSetSize; $c++ }
  if ($p.Name -eq 'rustc.exe' -and [int64]$p.WorkingSetSize -gt $rs) { $rs = [int64]$p.WorkingSetSize }
}
$o = Get-CimInstance Win32_OperatingSystem
'{0:N1} {1:N1} {2:N1} {3:N2} {4} {5:N1}' -f ($o.FreePhysicalMemory / 1MB), (($o.TotalVirtualMemorySize - $o.FreeVirtualMemory) / 1MB), ($o.TotalVirtualMemorySize / 1MB), ($ws / 1GB), $c, ($rs / 1GB)
