#!/usr/bin/env python3
"""#1025 winb (t5's order of 2026-11-22 ~21:03 UTC, after Modern Standby froze the D 19.25 regrid for 2 h 12 min): holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) from this
process' main thread until the watched pid is gone (or the cap in seconds has passed), then clears it with ES_CONTINUOUS and ends. No change to the power plan, no setting written, nothing killed.
The state is per thread and is dropped by Windows when this process ends, so it cannot outlive the helper. Log: rows/LABEL_keepawake.log in the scan folder (one line at start, one per 15 min, one at the end).
usage: keepawake_1025.py WATCHED_PID LABEL CAP_SECONDS [--selftest]    (--selftest: sets the state, reads nothing back, clears it, exits 0 if both calls returned non-zero)"""
import ctypes, datetime, sys, time

ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
k = ctypes.WinDLL("kernel32", use_last_error=True)
k.SetThreadExecutionState.argtypes = [ctypes.c_uint]
k.SetThreadExecutionState.restype = ctypes.c_uint
k.OpenProcess.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
k.OpenProcess.restype = ctypes.c_void_p
k.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
k.CloseHandle.argtypes = [ctypes.c_void_p]
STILL_ACTIVE = 259


def alive(pid):
    h = k.OpenProcess(0x1000, 0, pid)           # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    c = ctypes.c_uint()
    ok = k.GetExitCodeProcess(h, ctypes.byref(c))
    k.CloseHandle(h)
    return bool(ok) and c.value == STILL_ACTIVE


if "--selftest" in sys.argv:
    a = k.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    b = k.SetThreadExecutionState(ES_CONTINUOUS)
    print(f"set returned {a:#x}, clear returned {b:#x}; the clear returns the state it replaced, so {b:#x} must contain ES_SYSTEM_REQUIRED (0x1)")
    sys.exit(0 if a != 0 and b & ES_SYSTEM_REQUIRED else 1)

pid, label, cap = int(sys.argv[1]), sys.argv[2], float(sys.argv[3])
LOG = f"C:/Users/nathan/Source/kc87d22875s_1025/I1025-win/kc87_d22875_secant/rows/{label}_keepawake.log"


def say(m):
    open(LOG, "a").write(f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}\n")


t0 = time.time()
r = k.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
say(f"keep-awake helper ({label}), pid {__import__('os').getpid()}: SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) returned {r:#x} ({'ok' if r else 'FAILED'}; it returns the previous state, 0 on failure); "
    f"holds it until pid {pid} is gone or {cap:.0f} s pass; power plan untouched")
n = 0
while alive(pid) and time.time() - t0 < cap:
    time.sleep(15)
    n += 1
    if n % 60 == 0:
        say(f"still holding, pid {pid} alive, {time.time() - t0:.0f} s")
why = "cap reached" if alive(pid) else f"pid {pid} is gone"
b = k.SetThreadExecutionState(ES_CONTINUOUS)
say(f"{why} after {time.time() - t0:.0f} s; cleared with ES_CONTINUOUS (returned {b:#x}); helper ends")
