#!/usr/bin/env python3
"""Every INTERVAL s append one row per #82 process to worker_mem.csv: UTC time, node (omega/omega_inf), role (main or
worker), PID, working set in GB, and the node's last printed order k. Run detached next to the #82 runs; it reads
Win32_Process through PowerShell and the logs, and exits when no amp_flint_par process is left.

    python worker_mem_sampler.py [INTERVAL_S]     default 300
"""
import csv, datetime as dt, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
NODES = ("1.09", "1.10", "1.11")
ORDER = re.compile(r"^k (\d+):", re.M)
PS = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | ForEach-Object { "
      "'{0}|{1}|{2:N3}|{3}' -f $_.ProcessId, $_.ParentProcessId, ($_.WorkingSetSize/1GB), "
      "$(if ($_.CommandLine -match 'amp_flint_par\\.py\\s+(\\S+)\\s+45\\s') { $Matches[1] } else { '' }) }")


def last_k(node):
    try:
        with open(os.path.join(HERE, f"w{node}.log"), encoding="utf-8", errors="replace") as f:
            ks = ORDER.findall(f.read())
        return int(ks[-1]) if ks else 0
    except OSError:
        return -1


def sample():
    out = subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True).stdout
    rows = [l.strip().split("|") for l in out.splitlines() if l.count("|") == 3]
    node_of = {r[0]: r[3] for r in rows if r[3]}
    # The venv shim and the real interpreter both carry the node; the main is the one whose parent carries it too.
    mains = {r[0]: r[3] for r in rows if r[3] and r[1] in node_of}
    res = []
    for r in rows:
        if r[0] in mains:
            res.append((mains[r[0]], "main", r[0], r[2]))
        elif r[1] in mains:
            res.append((mains[r[1]], "worker", r[0], r[2]))
    return res


def main():
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 300
    path = os.path.join(HERE, "worker_mem.csv")
    new = not os.path.exists(path)
    while True:
        res = sample()
        if not res:
            return 0
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["utc", "node", "role", "pid", "ws_gb", "node_last_k"])
                new = False
            for node, role, pid, ws in sorted(res):
                w.writerow([now, node, role, pid, ws, last_k(node)])
        time.sleep(interval)


if __name__ == "__main__":
    sys.exit(main())
