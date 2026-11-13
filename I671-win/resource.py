"""A stand-in for the Unix module `resource` on Windows (the interpreter in this venv has none): only what solver/rt/rt_run.py's rss_peak_gb() uses.
getrusage(RUSAGE_SELF).ru_maxrss is returned in KiB (rt_run.py divides by 2**20 to get GB on non-macOS platforms), from the process's peak working set
(GetProcessMemoryInfo). It sits in this folder so that solves already running with an older rt_launch.py find it by their sys.path; rt_launch.py defines
the same module for the solves it starts."""
import ctypes
import ctypes.wintypes as wt

RUSAGE_SELF = 0


class _PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]


class _Usage:
    def __init__(self, ru_maxrss):
        self.ru_maxrss = ru_maxrss


def getrusage(who=RUSAGE_SELF):
    pmc = _PMC()
    pmc.cb = ctypes.sizeof(_PMC)
    k32, ps = ctypes.WinDLL("kernel32"), ctypes.WinDLL("psapi")
    k32.GetCurrentProcess.restype = wt.HANDLE
    ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(_PMC), wt.DWORD]
    ps.GetProcessMemoryInfo.restype = wt.BOOL
    ok = ps.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
    return _Usage(int(pmc.PeakWorkingSetSize // 1024) if ok else 0)
