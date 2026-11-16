"""accepted-step readings of the four walks (a stalled walk's last Jacobian is not applied)."""
import json
R = "C:/Users/nathan/Source/choptuik-large-d-raw-754/I897-winb"
I = "C:/Users/nathan/Source/choptuik-large-d-raw-754/I892-rpi5"
march = {}
for l in open(I + "/width.jsonl", encoding="utf-8"):
    r = json.loads(l); march[r["state"]] = r
spec = {"up_10.0": "data/sigdss_m03up.npz@10.0", "up_10.5": "data/sigdss_m03up.npz@10.5",
        "hi_10.5": "data/sigdss_m03hi.npz@10.5", "hi_11.0": "data/sigdss_m03hi.npz@11.0"}
wd = {}
for l in open(R + "/width2.jsonl", encoding="utf-8"):
    r = json.loads(l); wd[r["state"].replace("\\", "/").split("/")[-1]] = r
for n in spec:
    k = [json.loads(l) for l in open(f"{R}/walk2_{n}.jsonl", encoding="utf-8") if l.strip()][-1]
    a = [json.loads(l) for l in open(f"{I}/walk_{n}.jsonl", encoding="utf-8") if l.strip()][-1]
    h = k["hist"]
    acc = h[:-1] if k["stalled"] else h
    d = [x["dDelta"] for x in acc]
    m = march[spec[n]]
    w = wd[f"walk2_{n}.npy"]
    end = k["Delta"]
    print(f"{n}: {'stalled' if k['stalled'] else 'settled' if k['settled'] else 'not settled'} after {len(h)} Jacobians "
          f"({len(acc)} applied); Delta {end:.9f}; end-march {end - m['Delta']:+.4e} (march {m['Delta']:.9f}, W march {m['W']:.3e}); "
          f"#892 end {a['Delta']:.9f}, moved {end - a['Delta']:+.4e}")
    print(f"    walk F (last applied) {acc[-1]['F']:.4e}; width F {w['F']:.4e}, W {w['W']:.4e}, Newton {w['newton_dDelta']:+.4e}, "
          f"g {w['g_svd']:.5e} / {w['g_solve']:.5e} rel {abs(w['g_svd']-w['g_solve'])/w['g_svd']:.2e} agree {w['agree']}; smax {w['smax']:.3f} smallest {w['smallest'][0]['s']:.2e}")
    print(f"    applied steps: last {d[-1]:+.3e}, mean of last 10 {sum(d[-10:])/10:+.3e}, first {d[0]:+.3e}"
          + (f"; the Jacobian that stopped it: |F| {h[-1]['F']:.5e} (not lower), step {h[-1]['dDelta']:+.3e}" if k['stalled'] else ""))
    small = [x['jac'] for x in acc if abs(x['dDelta']) < 1e-9]
    print(f"    steps below 1e-9: {small}")
