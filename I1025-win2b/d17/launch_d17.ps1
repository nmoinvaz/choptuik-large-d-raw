# launches d17_hybrid.sh hidden at BelowNormal; children inherit the class
$p = Start-Process 'C:\Program Files\Git\bin\bash.exe' -ArgumentList '-c','"export PATH=/usr/bin:$PATH; cd /d/choptuik-large-d-raw/I1025-win2b/d17 && bash d17_hybrid.sh"' -WindowStyle Hidden -PassThru -RedirectStandardOutput D:\choptuik-large-d-raw\I1025-win2b\d17\d17_launcher.out -RedirectStandardError D:\choptuik-large-d-raw\I1025-win2b\d17\d17_launcher.err
$p.PriorityClass = 'BelowNormal'
"launcher pid $($p.Id) priority $($p.PriorityClass)"
