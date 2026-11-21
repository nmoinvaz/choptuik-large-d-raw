"""#966: are two saved jets the same series? Compares every array of the two npz files bit for bit, and the meta."""
import json, sys
import numpy as np
a, b = np.load(sys.argv[1]), np.load(sys.argv[2])
ka, kb = sorted(a.files), sorted(b.files)
diff = [k for k in ka if k in kb and k != "meta" and not np.array_equal(a[k], b[k])]
ma, mb = json.loads(str(a["meta"])), json.loads(str(b["meta"]))
print(f"arrays {ka == kb}, differing arrays {diff}, D {ma.get('D')} {mb.get('D')}, meta keys differing "
      f"{[k for k in set(ma) | set(mb) if ma.get(k) != mb.get(k)]}")
sys.exit(0 if ka == kb and not diff else 1)
