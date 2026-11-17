import numpy as np
src = open("pinnedo_gapcount.py").read()
i = src.index("def classify"); j = src.index("def wrap")
exec("import numpy as np\n" + src[i:j])
def col(*p): return [np.array([v]) for v in (list(p) + [0.0] * (8 - len(p)))]
dense = col(1.0, 2.0**-54, 2.0**-108, 2.0**-162)
interior = col(1.0, 0.0, 0.0, 2.0**-200)
bigjump = col(1.0, 2.0**-130)
zero = col()
for nm, p in (("dense", dense), ("zero part before a nonzero one", interior), ("part 130 bits down", bigjump), ("all zero", zero)):
    print(f"{nm}: (n, all-zero, gap class) = {classify(p)}")
