# cpu and memory snapshot for the #1025 posts: machine CPU % (1 s sample), commit and free physical memory, and the python processes above 0.5 GiB with their priority class and CPU seconds
$o = Get-CimInstance Win32_OperatingSystem
$cpu = (Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 3).CounterSamples | ForEach-Object { $_.CookedValue } | Measure-Object -Average | Select-Object -ExpandProperty Average
'machine CPU {0:N0}% (3 s mean), commit {1:N1} of {2:N1} GiB, free physical {3:N1} GiB' -f $cpu, (($o.TotalVirtualMemorySize - $o.FreeVirtualMemory)/1MB), ($o.TotalVirtualMemorySize/1MB), ($o.FreePhysicalMemory/1MB)
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.WorkingSet64 -gt 0.5GB } | ForEach-Object {
  $c = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine
  $k = if ($c -match 'p4_hybrid|signtest') { 'mine' } else { 'other' }
  'python pid {0} [{1}] {2:N1} GiB working set, {3}, {4:N0} cpu-s, up {5:N0} s: {6}' -f $_.Id, $k, ($_.WorkingSet64/1GB), $_.PriorityClass, $_.CPU, ((Get-Date) - $_.StartTime).TotalSeconds, $c.Substring(0, [math]::Min(90, $c.Length))
}
