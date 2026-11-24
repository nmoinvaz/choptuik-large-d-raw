# a minimal stand-in so multidouble's own test file can be called without pytest: mark.parametrize keeps the function and its cases
import importlib
class _Mark:
    def parametrize(self, names, cases):
        def deco(f):
            f._cases = (names, cases)
            return f
        return deco
mark = _Mark()
def importorskip(name):
    return importlib.import_module(name)
