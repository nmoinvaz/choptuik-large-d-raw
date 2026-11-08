#!/usr/bin/env python3
"""Log only. Every INTERVAL s append util_report.py's report line (time, cpu, memory used and free, commit) to
mem_log.txt next to this file. It kills nothing and stops nothing: no memory guard runs on win2 from 2026-11-08 13:31 UTC
(Nathan, relayed by the coordinator). Exits when no amp_flint_par K 45 process is left.

    python mem_log.py [INTERVAL_S]     default 300
"""
import os, subprocess, sys, time

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-t126")
import util_report as u  # report_line() only

HERE = os.path.dirname(os.path.abspath(__file__))
PS = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match "
      "'amp_flint_par\.py\s+\S+\s+45\s' } | Measure-Object | Select-Object -ExpandProperty Count")


def main():
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 300
    while True:
        with open(os.path.join(HERE, "mem_log.txt"), "a") as f:
            f.write(u.report_line() + "\n")
        n = subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True).stdout.strip()
        if n == "0":
            return 0
        time.sleep(interval)


if __name__ == "__main__":
    sys.exit(main())
