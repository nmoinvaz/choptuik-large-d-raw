#!/usr/bin/env python3
"""Core Temp's shared-memory readings, read only (issue #177). Standard library only.

    python coretemp.py          print one reading and the layout checks.

Core Temp publishes CORE_TEMP_SHARED_DATA_EX in the named mapping 'CoreTempMappingObjectEx' (the older, shorter block is
'CoreTempMappingObject'). The mapping is opened with FILE_MAP_READ only (OpenFileMappingW + MapViewOfFile), so nothing in
Core Temp can be changed from here. Layout of the Ex block, from the struct on https://alcpu.com/CoreTemp/developers.html
(4-byte aligned, 4740 bytes; the mapping is a page-rounded 8192):

    uint   uiLoad[256]        offset 0
    uint   uiTjMax[128]       1024
    uint   uiCoreCnt          1536
    uint   uiCPUCnt           1540
    float  fTemp[256]         1544
    float  fVID               2568
    float  fCPUSpeed          2572
    float  fFSBSpeed          2576
    float  fMultiplier        2580
    char   sCPUName[100]      2584
    uchar  ucFahrenheit       2684
    uchar  ucDeltaToTjMax     2685   (set: fTemp is the distance below TjMax, not a temperature)
    uchar  ucTdpSupported     2686
    uchar  ucPowerSupported   2687
    uint   uiStructVersion    2688   (2 in the current version)
    uint   uiTdp[128]         2692
    float  fPower[128]        3204
    float  fMultipliers[256]  3716

Temperatures are per core (fTemp[0 .. cores*cpus-1]); with the delta flag the temperature is TjMax - value; with the
Fahrenheit flag the values are converted to Celsius here."""
import ctypes, struct
from ctypes import wintypes

FILE_MAP_READ = 4
NAMES = ["CoreTempMappingObjectEx", "Global" + chr(92) + "CoreTempMappingObjectEx", "CoreTempMappingObject",
         "Global" + chr(92) + "CoreTempMappingObject"]

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.OpenFileMappingW.restype = wintypes.HANDLE
k32.OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
k32.MapViewOfFile.restype = ctypes.c_void_p
k32.MapViewOfFile.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]
k32.UnmapViewOfFile.argtypes = [ctypes.c_void_p]
k32.CloseHandle.argtypes = [wintypes.HANDLE]


class MBI(ctypes.Structure):
    _fields_ = [("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p), ("AllocationProtect", wintypes.DWORD),
                ("PartitionId", wintypes.WORD), ("RegionSize", ctypes.c_size_t), ("State", wintypes.DWORD),
                ("Protect", wintypes.DWORD), ("Type", wintypes.DWORD)]


k32.VirtualQuery.argtypes = [ctypes.c_void_p, ctypes.POINTER(MBI), ctypes.c_size_t]


def snapshot():
    """(name, bytes) of the first mapping that opens, or raises OSError with what was tried"""
    errs = []
    for name in NAMES:
        h = k32.OpenFileMappingW(FILE_MAP_READ, False, name)
        if not h:
            errs.append(f"{name}: error {ctypes.get_last_error()}")
            continue
        try:
            p = k32.MapViewOfFile(h, FILE_MAP_READ, 0, 0, 0)
            if not p:
                errs.append(f"{name}: MapViewOfFile error {ctypes.get_last_error()}")
                continue
            try:
                mbi = MBI()
                k32.VirtualQuery(p, ctypes.byref(mbi), ctypes.sizeof(mbi))
                return name, ctypes.string_at(p, mbi.RegionSize)
            finally:
                k32.UnmapViewOfFile(p)
        finally:
            k32.CloseHandle(h)
    raise OSError("; ".join(errs))


def parse(name, raw):
    r = dict(mapping=name, size=len(raw))
    load = struct.unpack_from("<256I", raw, 0)
    tj = struct.unpack_from("<128I", raw, 1024)
    cores, cpus = struct.unpack_from("<II", raw, 1536)
    temp = struct.unpack_from("<256f", raw, 1544)
    vid, speed, fsb, mult = struct.unpack_from("<4f", raw, 2568)
    cpu_name = raw[2584:2684].split(b"\0")[0].decode("ascii", "replace")
    fahr, delta, tdp_ok, power_ok = raw[2684], raw[2685], raw[2686], raw[2687]
    ver = struct.unpack_from("<I", raw, 2688)[0]
    power = [x for x in struct.unpack_from("<128f", raw, 3204)[:max(cpus, 1)]] if ver >= 2 and power_ok else []
    n = min(cores * max(cpus, 1), 256)
    conv = (lambda v: (v - 32) * 5 / 9) if fahr else (lambda v: v)
    tjmax = [conv(float(x)) for x in tj[:max(cpus, 1)]]
    vals = [conv(t) for t in temp[:n]]
    temps = [(tjmax[min(i // max(cores, 1), len(tjmax) - 1)] - v) if delta else v for i, v in enumerate(vals)]
    r.update(cores=cores, cpus=cpus, load=list(load[:n]), tjmax=tjmax, temps=temps, raw_temps=list(temp[:n]),
             vid=vid, speed_mhz=speed, fsb=fsb, multiplier=mult, cpu_name=cpu_name, fahrenheit=fahr, delta=delta,
             struct_version=ver, tdp_supported=tdp_ok, power_supported=power_ok, power_w=power)
    return r


def read():
    return parse(*snapshot())


def fmt(r):
    t = r["temps"]
    return (f"CoreTemp {r['cpu_name']!r} cores {r['cores']}x{r['cpus']} TjMax {'/'.join(f'{x:.0f}' for x in r['tjmax'])} "
            f"temp C min/mean/max {min(t):.0f}/{sum(t) / len(t):.1f}/{max(t):.0f} per-core {','.join(f'{x:.0f}' for x in t)} "
            f"load% {','.join(str(x) for x in r['load'])} VID {r['vid']:.3f} MHz {r['speed_mhz']:.0f}")


if __name__ == "__main__":
    try:
        r = read()
    except OSError as e:
        print("no Core Temp mapping:", e)
        raise SystemExit(3)
    print(f"mapping {r['mapping']} size {r['size']} struct_version {r['struct_version']} fahrenheit {r['fahrenheit']} "
          f"delta_to_tjmax {r['delta']}")
    print(fmt(r))
    print("raw fTemp:", [round(x, 1) for x in r["raw_temps"]])
