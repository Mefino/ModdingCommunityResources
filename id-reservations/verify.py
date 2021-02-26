#!/usr/bin/env python3
import sys
from pyjson5 import load

def slice_overlap(a, b):
    a1, a2 = (a[0], a[1]) if a[0] <= a[1] else (a[1], a[0])
    b1, b2 = (b[0], b[1]) if b[0] <= b[1] else (b[1], b[0])
    return a1 <= b2 and b1 <= a2

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data = load(f)

    reservations = []
    error = False
    for i, item in enumerate(data, 1):
        if len(item) != 3:
            print(f"Invalid record number {i}: {item}", file=sys.stderr)
            error = True
        else:
            first, last, username = item
            x = (first, last)
            ok = True
            order = True
            for (num, y, name) in reservations:
                if slice_overlap(x, y):
                    print(f"Overlapping record number {i} {item}, offends {num} {[y[0], y[1], name]}", file=sys.stderr)
                    error = True
                    ok = False
                elif order and x[0] > y[0]:
                    print(f"Record out of order {i} {item}", file=sys.stderr)
                    error = True
                    order = False
            if ok:
                reservations.append((i, x, username))

    sys.exit(1 if error else 0)
