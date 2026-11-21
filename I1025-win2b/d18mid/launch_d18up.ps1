# launches d18up_driver.sh hidden at BelowNormal; the python processes and the sampler inherit the class
$p = Start-Process 'C:\Program Files\Git\bin\bash.exe' -ArgumentList '-c','"export PATH=/usr/bin:$PATH; cd /d/choptuik-large-d-raw/I1025-win2b/d18mid && bash d18up_driver.sh"' -WindowStyle Hidden -PassThru -RedirectStandardOutput D:\choptuik-large-d-raw\I1025-win2b\d18mid\launcher_up.out -RedirectStandardError D:\choptuik-large-d-raw\I1025-win2b\d18mid\launcher_up.err
$p.PriorityClass = 'BelowNormal'
"launcher pid $($p.Id) priority $($p.PriorityClass)"
