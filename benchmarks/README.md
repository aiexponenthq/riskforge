# RiskForge benchmarks

Reproducible performance measurements. Run:

```bash
make bench          # or: python benchmarks/perf.py
```

Timings are wall-clock and indicative, not a guarantee. The numbers below were
taken on a developer laptop (Apple Silicon, Python 3.12) and are here to show the
scaling behaviour, not absolute performance.

## Audit append (hash-chained log)

Each append chains from the current tail and verifies that tail entry, so building
a chain is linear in the number of entries.

| entries | total (s) | per entry (ms) | verify chain (s) |
|--------:|----------:|---------------:|-----------------:|
| 100     | 0.03      | 0.35           | 0.001            |
| 500     | 0.19      | 0.37           | 0.003            |
| 1000    | 0.38      | 0.38           | 0.006            |
| 2000    | 0.89      | 0.45           | 0.013            |

Per-entry time is flat (~0.4 ms), confirming O(n). Full-chain `verify` is a single
linear pass and is fast even at 2000 entries.

## add_risk (full engine path)

`add_risk` appends one audit entry (O(1), above) and rewrites the register YAML,
which serialises every item. The rewrite is O(n) per call, so adding items
one-by-one is O(n^2) in the register size.

| items | total (s) | per item (ms) |
|------:|----------:|--------------:|
| 10    | 0.06      | 5.6           |
| 50    | 1.01      | 20.2          |
| 100   | 4.10      | 41.0          |
| 200   | 16.55     | 82.7          |

This is comfortable at the sizes a real Article 9 assessment produces (a pattern
plus a question bank of 37 items lands in the tens). It only becomes noticeable
past ~100 items in one register. If a future use case needs very large registers,
the register store would move from a whole-file rewrite to an append-structured
item log; the audit log already works that way.

## Interpreting drift

A regression here shows up as the per-entry or per-item column growing
super-linearly. The audit column should stay flat; if it starts climbing with
size, the tail-chaining path has regressed to a full-chain scan.
