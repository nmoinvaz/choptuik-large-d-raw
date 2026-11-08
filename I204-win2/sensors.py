#!/usr/bin/env python3
"""CPU clocks, load and package power of win2 from Windows performance counters (built in, no driver, read only).

    python sensors.py            print one reading.

There is no CPU temperature source on this board without a driver (issue #177): the 'Thermal Zone Information' counter set
has no instances and MSAcpi_ThermalZoneTemperature answers 'Not supported', so `temp` is reported as n/a.
Energy Meter 'Power' is taken as milliwatts (112061 at a busy moment, 112 W is plausible for this CPU)."""
import datetime as dt, re, subprocess

BS = chr(92)  # backslash, kept out of the source text
CTR = [BS + "Processor Information(*)" + BS + "Processor Frequency", BS + "Processor Information(*)" + BS + "% Processor Performance",
       BS + "Processor Information(_Total)" + BS + "% Processor Utility", BS + "Energy Meter(RAPL_Package0_PKG)" + BS + "Power",
       BS + "Energy Meter(RAPL_Package0_PP0)" + BS + "Power"]
PS = ("$c = Get-Counter -Counter @(" + ",".join("'" + c + "'" for c in CTR) + ") -SampleInterval 1 -MaxSamples 2; "
      "foreach ($x in $c[-1].CounterSamples) { '{0}|{1}' -f $x.Path, $x.CookedValue }; "
      "$o = Get-CimInstance Win32_OperatingSystem; 'free_gb|{0}' -f ($o.FreePhysicalMemory/1MB)")
CORE = re.compile(r"processor information[(]([0-9]+),([0-9]+)[)].(.*)$")


def read():
    out = subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True, timeout=60).stdout
    freq, perf, util, pkg, pp0, free = [], [], None, None, None, None
    for line in out.splitlines():
        if "|" not in line:
            continue
        path, val = line.rsplit("|", 1)
        path = path.lower()
        try:
            v = float(val)
        except ValueError:
            continue
        core = CORE.search(path)
        if core and core.group(3) == "processor frequency":
            freq.append(v)
        elif core and core.group(3) == "% processor performance":
            perf.append(v)
        elif path.endswith("% processor utility") and "_total" in path:
            util = v
        elif "rapl_package0_pkg" in path:
            pkg = v / 1000.0
        elif "rapl_package0_pp0" in path:
            pp0 = v / 1000.0
        elif path.startswith("free_gb"):
            free = v
    d = dict(freq_min=min(freq) if freq else None, freq_mean=sum(freq) / len(freq) if freq else None,
             freq_max=max(freq) if freq else None, perf_mean=sum(perf) / len(perf) if perf else None,
             util=util, pkg_w=pkg, core_w=pp0, free_gb=free, temp="n/a", n_threads=len(freq), ct=None)
    try:  # Core Temp's shared memory, read only (coretemp.py); without it the temperature stays n/a
        import coretemp
        d["ct"] = coretemp.read()
        d["temp"] = "max %.0f" % max(d["ct"]["temps"])
    except Exception as e:
        d["temp"] = f"n/a (Core Temp: {e})"
    return d


def fmt(r):
    f = lambda x, p=0: "n/a" if x is None else f"{x:.{p}f}"
    s = (f"clock MHz min/mean/max {f(r['freq_min'])}/{f(r['freq_mean'])}/{f(r['freq_max'])} "
         f"perf% {f(r['perf_mean'])} util% {f(r['util'])} pkgW {f(r['pkg_w'], 1)} coreW {f(r['core_w'], 1)} "
         f"free_GB {f(r['free_gb'], 1)} temp {r['temp']} threads {r['n_threads']}")
    c = r.get("ct")
    if c:
        t = c["temps"]
        s += (f" | CoreTemp {c['cpu_name']} TjMax {'/'.join(f'{x:.0f}' for x in c['tjmax'])} C, core temps C "
              f"min/mean/max {min(t):.0f}/{sum(t) / len(t):.1f}/{max(t):.0f} [{','.join(f'{x:.0f}' for x in t)}] "
              f"core load% [{','.join(str(x) for x in c['load'])}] VID {c['vid']:.3f} V speed {c['speed_mhz']:.0f} MHz")
    return s


if __name__ == "__main__":
    print(dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"), fmt(read()))
