"""Newton estimates (state Delta plus Newton's step) at the march, #892's end and #897's end, and the D 10.5 gap."""
import json

R = "C:/Users/nathan/Source/choptuik-large-d-raw-754/I897-winb"
I = "C:/Users/nathan/Source/choptuik-large-d-raw-754/I892-rpi5"
BS = chr(92)


def tail(s):
    return s.replace(BS, "/").split("/")[-1]


wd = {tail(json.loads(l)["state"]): json.loads(l) for l in open(R + "/width2.jsonl") if l.strip()}
we = {tail(json.loads(l)["state"]): json.loads(l) for l in open(I + "/width_end.jsonl") if l.strip()}
wm = {json.loads(l)["state"]: json.loads(l) for l in open(I + "/width.jsonl") if l.strip()}
for n, sp in (("up_10.0", "data/sigdss_m03up.npz@10.0"), ("up_10.5", "data/sigdss_m03up.npz@10.5"),
              ("hi_10.5", "data/sigdss_m03hi.npz@10.5"), ("hi_11.0", "data/sigdss_m03hi.npz@11.0")):
    a, b, m = we["walk_%s.npy" % n], wd["walk2_%s.npy" % n], wm[sp]
    print(n, "march Delta + Newton %.6f" % (m["Delta"] + m["newton_dDelta"]),
          "| #892 end + Newton %.6f" % (a["Delta"] + a["newton_dDelta"]),
          "| #897 end + Newton %.6f" % (b["Delta"] + b["newton_dDelta"]))
print("D 10.5 gap, #892 ends %.6e, #897 ends %.6e" % (1.137696236 - 1.115098687, 1.137323569 - 1.120571241))
