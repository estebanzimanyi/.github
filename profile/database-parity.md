MobilityDB Databases — Parity & Benchmarks
==========================================

The ecosystem exposes the same MEOS temporal and spatiotemporal operations through SQL on
three engines — [MobilityDB](https://github.com/MobilityDB/MobilityDB) (the reference
implementation), [MobilityDuck](https://github.com/MobilityDB/MobilityDuck), and
[MobilitySpark](https://github.com/MobilityDB/MobilitySpark). This page reports,
**measured rather than estimated**, how much of the MobilityDB SQL surface each engine
covers, how that coverage is verified, and how the engines perform on the BerlinMOD
benchmark. Together these answer the question a prospective adopter asks first — *is the
database layer complete, does it return correct results, and is it fast enough to deploy
on real workloads?* — with reproducible evidence rather than assertion.

> Companion: **[Streaming — parity & benchmarks](streaming-parity.md)** reports the same
> for the stream processors (MobilityFlink / MobilityKafka / MobilityNebula).

## Results at a glance

Coverage of the **MobilityDB SQL surface** — each engine over its active-addressable scope:

```text
MobilityDB      ████████████████████  reference     100 %    full regression suite
MobilityDuck    ████████████████████   943 / 943    100.0%   active scope · extended families in progress
MobilitySpark   ███████████████████▉  1571 / 1577    99.6%   + 29 / 29 portable dialect
```

- **Correctness** — BerlinMOD reference queries return **identical results** across all three engines ✓
- **Benchmark** — cross-platform timings ▸ [report #29](https://github.com/MobilityDB/MobilityDB-BerlinMOD/pull/29) *(dated runs publishing)*

**▶ Full results & raw data**
- MobilityDuck — [`parity-status.md`](https://github.com/MobilityDB/MobilityDuck/blob/main/docs/parity-status.md) · [`PARITY.md`](https://github.com/MobilityDB/MobilityDuck/blob/main/docs/PARITY.md)
- MobilitySpark — [`parity-100.md`](https://github.com/MobilityDB/MobilitySpark/blob/main/docs/parity-100.md)
- MobilityDB cross-type — [methodology #1002](https://github.com/MobilityDB/MobilityDB/pull/1002) · [audit harness #1110](https://github.com/MobilityDB/MobilityDB/pull/1110)

## The surface

The reference is the **public SQL API of MobilityDB** — every `CREATE FUNCTION` it
defines. MobilityDB *is* the reference, so its surface is the parity target;
MobilityDuck and MobilitySpark are each measured against the portion applicable to them.

Functions outside an engine's scope are excluded **by reason, not by omission**, and are
never counted as gaps — chiefly PostgreSQL-only plumbing (`*_in`/`*_out`/`*_recv`/`*_send`,
aggregate transition/combine/finalize internals, selectivity/support functions, GiST/SPGiST
operator classes) for which no DuckDB or Spark equivalent exists, plus a small set of
operations reserved by [semantic exclusion](#cross-type-coverage) because they are
formally meaningless on a given type.

## Coverage

Three layers, increasing in strength:

- **L1 — exported.** The operation is present in the engine's library (MobilityDB `nm -D`).
- **L2 — registered.** It is a callable SQL function in the engine's catalog
  (`pg_proc` / DuckDB scalar registry / Spark UDF registry).
- **L3 — tested.** A regression test mirrored from MobilityDB exercises it and the result
  is checked.

| Engine | L2 registered | L3 tested | of MobilityDB SQL surface |
|---|---|---|---|
| **MobilityDB**    | reference | full regression suite | **100 % (reference)** |
| **MobilityDuck**  | 943 / 943 active-addressable | ported MobilityDB `*.test.sql` mirrors | **100 %** active scope · extended families in progress |
| **MobilitySpark** | 1571 / 1577 active-addressable + 29/29 portable dialect | 907 SQL-parity + BerlinMOD tests | **99.6 %** · all six type families |

Each engine's coverage is audited from its own repository — MobilityDuck via
[`docs/parity-status.md`](https://github.com/MobilityDB/MobilityDuck/blob/main/docs/parity-status.md)
and [`PARITY.md`](https://github.com/MobilityDB/MobilityDuck/blob/main/docs/PARITY.md);
MobilitySpark via [`docs/parity-100.md`](https://github.com/MobilityDB/MobilitySpark/blob/main/docs/parity-100.md).
The figures advance as the accumulated-PR builds of the three engines land; this page
tracks the measured state.

## Cross-type coverage

MobilityDB's parity also has a *cross-type* axis: every temporal spatial type is held to
the same function surface as its reference family — `tgeompoint` is the reference for the
`Point` family (`tgeogpoint`, `tnpoint`), `tgeometry` for the extended-shape family
(`trgeometry`, `tcbuffer`, `tpose`). The methodology and the audit harness are in
MobilityDB ([cross-type parity methodology](https://github.com/MobilityDB/MobilityDB/pull/1002),
[audit harness](https://github.com/MobilityDB/MobilityDB/pull/1110),
[RFC #868](https://github.com/MobilityDB/MobilityDB/discussions/868)).

A handful of operations are **reason-marked as formally meaningless** on specific types
and are deliberately never implemented — they are not gaps:

- `convexhull` on `tgeogpoint` — a point's continuous form collapses to `trajectory()` / `stbox()`.
- `affine` / `rotate` / `scale` / `translate` on `tnpoint`, `tcbuffer`, `tpose`, `trgeometry` — an affine transform bypasses the type invariant (rigid pose / centre+radius / route+fraction).
- `atGeometry` / `minusGeometry` on `tnpoint` — a network point is constrained to its 1-D edge; use route filtering.

## Query-result parity (BerlinMOD)

The three engines run the **BerlinMOD** reference queries and must return **identical
results** — the cross-engine portability contract
([discussion #861](https://github.com/MobilityDB/MobilityDB/discussions/861), conformance
suite [MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD)). This
batch result is also the anchor for the streaming **snapshot** form, linking database
parity to [streaming parity](streaming-parity.md).

## Benchmarks (BerlinMOD)

Coverage and correctness establish that the queries *run* and *agree*; the BerlinMOD
benchmark establishes that they run *fast enough to deploy*. The cross-platform timing
report is organised by **what each measurement licenses to claim**
([MobilityDB-BerlinMOD #29](https://github.com/MobilityDB/MobilityDB-BerlinMOD/pull/29)):
the `th3index` matrix is the cross-platform-comparable axis, native-index results are
intra-platform only, and their composition is reported only where it beats both alone.
Results are published here as each dated run is finalised; the benchmark harness lives in
[MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD) with the
Spark driver in [MobilitySpark `berlinmod/bench`](https://github.com/MobilityDB/MobilitySpark/tree/main/berlinmod/bench).

## Reproduce it

The coverage numbers come from per-repo audit scripts, and the cross-type figures from a
config-driven harness:

```sh
# MobilityDuck
python3 scripts/parity-audit.py        # -> docs/parity-status.md (943/943 active)
# MobilitySpark
python3 scripts/parity-audit.py        # -> docs/parity-status.md (1571/1577)
python3 scripts/portable_parity.py     # 29/29 portable bare names
# MobilityDB cross-type
tools/parity_audit/                    # nm -D / pg_proc / test — 3-condition gate
```

*Status as of 2026-05-23. MobilityDB is the reference; MobilityDuck and MobilitySpark
coverage and the benchmark tables advance as the accumulated-PR builds and dated runs
land.*
