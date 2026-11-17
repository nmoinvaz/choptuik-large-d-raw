# Samples the rt_sigma python process (the child of the venv launcher the driver started) every 10 min: working set, peak, cpu minutes, machine cpu and free memory.
# The driver's own resource.log reads the launcher stub (4 MB, 0 cpu), so this is the record of memory and cpu. Ends when the child exits.
param([int]$LauncherPid = 26264, [string]$Log = 'D:\choptuik-i935-raw\I745-win2\logs\resource_child.log')
$t0 = (Get-Process -Id $LauncherPid).StartTime
while ($true) {
    $c = Get-CimInstance Win32_Process -Filter "ParentProcessId=$LauncherPid AND Name='python.exe'" | Select-Object -First 1
    if (-not $c) { "$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC child gone" | Add-Content $Log; break }
    $p = Get-Process -Id $c.ProcessId -ErrorAction SilentlyContinue
    if (-not $p) { "$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC child gone" | Add-Content $Log; break }
    $el = ((Get-Date) - $t0).TotalMinutes
    $os = Get-CimInstance Win32_OperatingSystem
    $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
    '{0} UTC pid {1} elapsed {2:N1} min, working set {3:N0} MB, peak {4:N0} MB, cpu {5:N1} min ({6:N2} threads averaged), machine cpu {7:N0}%, free {8:N1} GB' -f `
        (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss'), $p.Id, $el, ($p.WorkingSet64/1MB), ($p.PeakWorkingSet64/1MB), ($p.CPU/60), ($p.CPU/60/$el), $cpu, ($os.FreePhysicalMemory/1MB) | Add-Content $Log
    Start-Sleep -Seconds 600
}
