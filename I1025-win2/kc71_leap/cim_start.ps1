# cim_start.ps1 -Name NAME -Bash 'bash script.sh args' [-Dir /d/...]: starts a bash command OUTSIDE the calling terminal (the coordinator's order of 2026-11-22): writes $d\NAME.cmd and creates cmd.exe /c NAME.cmd through
# Win32_Process.Create, so that the parent chain runs bash <- cmd <- WmiPrvSE <- svchost and does not touch claude.exe. The .cmd starts bash at BelowNormal and waits for it (cmd stays as bash's parent); output goes to NAME.stdout/.stderr.
param([string]$Name, [string]$Bash, [string]$Dir = '/d/choptuik-i935-raw/I1025-win2/kc71_leap', [switch]$Wt)
$d = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$cmd = "@echo off`r`nstart `"`" /wait /belownormal /b `"C:\Program Files\Git\bin\bash.exe`" -c `"export PATH=/usr/bin:`$PATH; cd $Dir && $Bash`" 1>> $d\$Name.stdout 2>> $d\$Name.stderr`r`n"
[IO.File]::WriteAllText("$d\$Name.cmd", $cmd, [Text.Encoding]::ASCII)
# 2026-11-22 21:10 UTC: the console is a headless conhost (no Windows Terminal handoff, no OpenConsole -Embedding host); -Wt gives the earlier form, cmd.exe /c with the handoff
$cl = if ($Wt) { "cmd.exe /c $d\$Name.cmd" } else { "conhost.exe --headless cmd.exe /c $d\$Name.cmd" }
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $cl; CurrentDirectory = $d }
"$Name cmd.exe pid $($r.ProcessId) return $($r.ReturnValue)"
