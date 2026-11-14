"""number the displayed equations of a LaTeX file by section (equation, eqnarray, align: one number per row unless
\\nonumber / \\notag; subequations: a, b, ...); print the number of each row with its \\label. Macros: \\be, \\ee,
\\bea, \\eea, \\beq, \\eeq, \\beqa, \\eeqa, \\nn (\\nonumber) and \\non (\\nonumber \\\\, Kol's)."""
import re
import sys

src = open(sys.argv[1]).read()
src = re.sub(r"(?m)(?<!\\)%.*$", "", src)
for a, b in (("beqa", r"\begin{eqnarray}"), ("eeqa", r"\end{eqnarray}"), ("bea", r"\begin{eqnarray}"),
             ("eea", r"\end{eqnarray}"), ("beq", r"\begin{equation}"), ("eeq", r"\end{equation}"),
             ("be", r"\begin{equation}"), ("ee", r"\end{equation}")):
    src = re.sub(r"\\" + a + r"(?![a-zA-Z])", lambda m, b=b: b, src)
src = re.sub(r"\\non(?![a-zA-Z])", lambda m: r"\nonumber \\", src)
src = re.sub(r"\\nn(?![a-zA-Z])", lambda m: r"\nonumber", src)
tok = re.compile(r"\\section\*?\{|\\appendix|\\begin\{(equation|eqnarray|align|subequations)\}"
                 r"|\\end\{(subequations)\}")
sec, eq, appendix, sub = 0, 0, False, None
out = []
for m in tok.finditer(src):
    t = m.group(0)
    if t.startswith(r"\section"):
        if not t.startswith(r"\section*"):
            sec += 1
            eq = 0
        continue
    if t == r"\appendix":
        appendix, sec = True, 0
        continue
    if t == r"\begin{subequations}":
        eq += 1
        sub = 0
        continue
    if t == r"\end{subequations}":
        sub = None
        continue
    name = m.group(1)
    end = src.index(r"\end{%s}" % name, m.end())
    body = src[m.end():end]
    rows = [body] if name == "equation" else re.split(r"\\\\", body)
    for r in rows:
        if name != "equation" and (r"\nonumber" in r or r"\notag" in r or not r.strip()):
            continue
        lab = re.search(r"\\label\{([^}]*)\}", r)
        S = chr(64 + sec) if appendix else str(sec)
        if sub is not None:
            sub += 1
            num = "%s.%d%s" % (S, eq, chr(96 + sub))
        else:
            eq += 1
            num = "%s.%d" % (S, eq)
        out.append((num, lab.group(1) if lab else "", " ".join(r.split())[:90]))
for num, lab, txt in out:
    print("(%s) %-28s %s" % (num, lab, txt))
