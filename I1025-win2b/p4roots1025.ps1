# glue for p4cap1025.sh: one line per root python.exe (the venv launcher stub, whose parent is not itself such a python) of a running p4_hybrid.py: "pid age_seconds kind", kind = cross (the Fb D 16 k_c 55 cross-check row), kc71 (the l1kc71Fw1025c row) or other
$a = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*p4_hybrid.py*' })
if ($a.Count -gt 0) {
  $ids = @($a | ForEach-Object { $_.ProcessId })
  $a | Where-Object { $ids -notcontains $_.ParentProcessId } | ForEach-Object {
    $kind = if ($_.CommandLine -like '*l1kc55Fb1025*') { 'cross' } elseif ($_.CommandLine -like '*l1kc71Fw1025c*') { 'kc71' } else { 'other' }
    '{0} {1} {2}' -f $_.ProcessId, [int]((Get-Date) - $_.CreationDate).TotalSeconds, $kind
  }
}
