# simple formatter that enforces 4-space indent for .py files in protolang/
import sys, os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'protolang')

for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.endswith('.py'):
            p = os.path.join(dirpath, fn)
            with open(p, 'r', encoding='utf-8') as f:
                txt = f.read()
            # naive: replace tabs with 4 spaces
            new = txt.replace('\t', '    ')
            if new != txt:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(new)
                print('fixed', p)
