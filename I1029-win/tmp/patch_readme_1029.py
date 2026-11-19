p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\README.md"
s = open(p, encoding="utf-8").read()
pairs = [
 ("(sigma_2 = 0.1284 - 0.6748i and -0.8857 + 1.1061i at wf 0.100532)", "(sigma_1 = -0.8857 + 1.1061i and sigma_2 = 0.1284 - 0.6748i at wf 0.100532)"),
 ("|f(k,3) A^k| = 4.03, 39.8 at k = 3, 5 (both zeros the same to 3 digits across J), then", "|f(k,3) A^k| = 4.03, 39.8 at k = 3, 5 at wf 0.065740 and 4.12, 34.3 at wf 0.100532 (equal across J), then"),
 ("because the f at k = 21 to 25 reach 1e330 to 1e550 and dominate", "because the f at the highest orders (k = 21 to 25) reach 1e270 to 1e540 and dominate"),
 ("(orders 21 to 25 mostly: 33, 26, 29 and 18 of 78)", "(mostly orders 21 to 25: 33, 26, 29 and 18 of 78 entries)"),
]
for a, b in pairs:
    assert a in s, a
    s = s.replace(a, b, 1)
open(p, "w", encoding="utf-8").write(s)
