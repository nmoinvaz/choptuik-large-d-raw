"""Stage this machine's outputs of run893.sh under the Mac's I887-mac file names (appended records only for the
appended logs), so that compare_i885.py can compare them with I887-mac as its 'stored' directory.
usage: python -I stage893.py <I893-winb> <worktree solver/proof> <stage dir>"""
import os
import shutil
import subprocess
import sys

R, PROOF, STAGE = sys.argv[1], sys.argv[2], sys.argv[3]
WT = os.path.dirname(os.path.dirname(PROOF))
os.makedirs(STAGE, exist_ok=True)


def rd(p):
    return open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")


def put(name, text):
    open(os.path.join(STAGE, name), "w", encoding="utf-8", newline="\n").write(text)


def stored(name):
    return subprocess.run(["git", "-C", WT, "show", "HEAD:solver/proof/" + name], capture_output=True,
                          encoding="utf-8").stdout.replace("\r\n", "\n")


# stdout logs: this machine's name -> the Mac's name
OUTS = {
    "b5_jump.log": "b5_jump.log", "b5_jump_d0.log": "b5_jump_d0_1e7.log", "b5_jump_sum.log": "b5_jump_mut_sum.log",
    "b5_threshold.log": "b5_threshold.log", "b7_ift.log": "b7_ift.log", "b7_ift_JD.log": "b7_ift_mutJD.log",
    "b8m_atoms.log": "b8m_atoms_K4.log", "b8m_h8.log": "b8m_h8_K4_L73.89.log",
    "b8m_h8_d0.log": "b8m_h8_K4_L73.89_d0_1e7.log", "b8m_scan_box.log": "b8m_scan_K4_box.out",
    "b8m_scan_d0.log": "b8m_scan_K4_d0_1e7.out", "b8m_scan_k085.log": "b8m_scan_K4_k0.85.out",
    "b8m_lc.log": "b8m_lc_K4.out", "b8m_lc_mut_rho2L.log": "b8m_lc_K4_mut_rho2L.out",
    "b8m_lc_lipcheck.log": "b8m_lc_lipcheck.log", "b8m_lc_numcheck_mut.log": "b8m_lc_numcheck_mut.log",
    "b8m_lc_numcheck.log": "b8m_lc_numcheck_n1e3.log", "b8m_lc_numcheck_d0.log": "b8m_lc_numcheck_mut_d0.log",
    "b8m_lcj.log": "b8m_lcj.log", "b8m_lcj_kernel.log": "b8m_lcj_mut_kernel.log",
}
for mine, mac in OUTS.items():
    put(mac, rd(os.path.join(R, mine)))

# JSON files the run rewrote (in changed/) or left alone (read from the worktree)
def changed(name):
    p = os.path.join(R, "changed", name)
    return rd(p) if os.path.isfile(p) else stored(name)


for name in ("b5_jump.json", "b5_jump_d0_1e7.json", "b7_ift.json", "b8m_lc_lip.json", "b8m_lcj.json"):
    put(name, changed(name))

# appended logs: the lines beyond the stored count
for name in ("b8m_scan_K4_box.log", "b8m_scan_K4_d0_1e7.log", "b8m_scan_K4_k0.85.log", "b8m_lc_K4.log",
             "b8m_lc_K4_mut_rho2L.log"):
    old, new = stored(name).splitlines(), changed(name).splitlines()
    assert new[:len(old)] == old, name
    put(name, "\n".join(new[len(old):]) + "\n")
    print(name, "stored", len(old), "now", len(new), "appended", len(new) - len(old))
