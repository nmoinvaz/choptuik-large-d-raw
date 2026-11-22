# #1025 D 18.0625 scan: passive sampler, every -Interval s one machine row (cpu %, commit GiB, free physical GiB) and one row per python.exe whose command line contains -Pat
# (working set, private bytes, cpu seconds, priority). Reads only; the driver ends it by its exact pid. CSV: utc,kind,pid,v1,v2,v3,v4 (kind machine: v1 cpu %, v2 commit GiB, v3 free GiB; kind proc: v1 working set GiB, v2 private GiB, v3 cpu s, v4 priority)
param([string]$Out, [int]$Interval = 60, [string]$Pat = 'd18_hybsign.py')
$ic = [System.Globalization.CultureInfo]::InvariantCulture
if (-not (Test-Path $Out)) { 'utc,kind,pid,v1,v2,v3,v4' | Out-File -FilePath $Out -Encoding ascii }
while ($true) {
  $t = [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss')
  $o = Get-CimInstance Win32_OperatingSystem
  $cpu = (Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1).CounterSamples[0].CookedValue
  $rows = @(('{0},machine,0,{1},{2},{3},' -f $t, $cpu.ToString('F1', $ic), (($o.TotalVirtualMemorySize - $o.FreeVirtualMemory) / 1MB).ToString('F2', $ic), ($o.FreePhysicalMemory / 1MB).ToString('F2', $ic)))
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like "*$Pat*" } | ForEach-Object {
    $g = Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue
    if ($g) { $rows += ('{0},proc,{1},{2},{3},{4},{5}' -f $t, $_.ProcessId, ($g.WorkingSet64 / 1GB).ToString('F3', $ic), ($g.PrivateMemorySize64 / 1GB).ToString('F3', $ic), $g.CPU.ToString('F0', $ic), $g.PriorityClass) }
  }
  $rows | Out-File -FilePath $Out -Encoding ascii -Append
  Start-Sleep -Seconds $Interval
}
