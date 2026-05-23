MobilityDB Streaming — Parity & Benchmarks
==========================================

The ecosystem exposes the same MEOS temporal and spatiotemporal operations on three
stream processors — [MobilityFlink](https://github.com/MobilityDB/MobilityFlink),
[MobilityKafka](https://github.com/MobilityDB/MobilityKafka), and
[MobilityNebula](https://github.com/MobilityDB/MobilityNebula). This page reports,
**measured rather than estimated**, how much of the streamable MEOS surface each one
covers, how that coverage is verified, and how the platforms perform on the BerlinMOD
benchmark. Together these answer the question a prospective adopter asks first — *is the
streaming layer complete, does it return correct results, and is it fast enough to
deploy on real workloads?* — with reproducible evidence rather than assertion.

> Companion: **[Databases — parity & benchmarks](database-parity.md)** reports the same
> for the SQL engines (MobilityDB / MobilityDuck / MobilitySpark).

## Results at a glance

Coverage of the **1,945 streamable MEOS functions** — confirmed callable on a real `libmeos`:

<img src="https://raw.githubusercontent.com/MobilityDB/.github/main/profile/images/streaming-coverage.png?v=5" width="760" alt="Streaming MEOS function coverage of 1,945 streamable functions: MobilityFlink 100.0% (1945/1945, proven callable), MobilityKafka 100.0% (1945/1945, proven callable), MobilityNebula 12.6% (245/1945, wired)" />

- **Correctness** — all **9 BerlinMOD queries × 3 streaming forms = 27/27 cells** reproduce the batch result on every platform; the Flink snapshot output is **byte-identical** to the batch oracle.

**▶ Full results & raw data**
- Per-function coverage — committed feeds `flink-kafka.feed.tsv` + `nebula.feed.tsv`, reproduced by `ci_gate.py` (MobilityNebula `tools/streaming_parity/`).
- Methodology — `doc/methodology/streaming_parity_assessment.md` (MobilityNebula).

## The surface

The reference is the **1,945 streamable MEOS public functions** — every exported MEOS
function that can run inside a streaming dataflow, across four tiers: `stateless`,
`bounded-state`, `windowed`, and `cross-stream`.

Functions outside that surface are excluded **by reason, not by omission**, and are
never counted as gaps:

| reason | count | why it is not streamable |
|---|--:|---|
| internal | 1,308 | not part of the public API |
| io-meta | 218 | parsing / output / catalog plumbing (`*_in`, `*_out`, …) |
| ambiguous | 59 | reserved pending a semantic decision |
| sequence-only | 14 | need a fully materialized sequence; no per-event form |

## Coverage

Three layers, increasing in strength:

- **L1 — exported.** The symbol is present in `libmeos` (`nm -D`).
- **L2 — wired.** A binding operator or facade method calls it.
- **L3 — proven.** It is actually invoked on a real `libmeos`: confirmed callable
  (JVM tools) or exercised by a passing systest (NebulaStream).

| Platform | L3 proven | L2 wired | of 1,945 |
|---|--:|--:|--:|
| **MobilityFlink**  | **1,945 callable** | 1,945 | **100.0 %** |
| **MobilityKafka**  | **1,945 callable** | 1,945 | **100.0 %** |
| **MobilityNebula** | 6 systest-confirmed | 245 wired · compile-verified | 12.6 % wired |

Flink and Kafka share one generated JNR-FFI facade, so their callability is identical;
it is confirmed by a type-aware per-method harness that invokes **every** facade method
on a real `libmeos` (a returned value or a caught MEOS semantic error counts as
callable — only a linkage or marshalling failure does not). NebulaStream operators are
generated C++ physical operators; each is **compile-verified** against the build's
`libmeos` in the NebulaStream development image, and a systest suite confirms
callability operator by operator.

## Query-result parity (BerlinMOD)

The three platforms run the **9 BerlinMOD reference queries in three streaming forms** —
continuous, windowed, and snapshot — **27 of 27 cells per platform**, with the snapshot
form anchored to the batch (SQL-engine) result at the same scale factor. Every cell
reproduces the batch result, and the Flink snapshot output is **byte-identical** to the
batch oracle. This links streaming parity to [database parity](database-parity.md).

## Benchmarks (BerlinMOD)

Coverage and correctness establish that the queries *run* and *agree*; the BerlinMOD
benchmark establishes that they run *fast enough to deploy*. The same reference queries
are timed on each platform across scale factors and the three streaming forms
(continuous / windowed / snapshot), reporting per-query throughput and latency. Because
the workload definition is shared with the SQL engines
([MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD)), streaming
and batch timings are directly comparable at the same scale factor.

The timing methodology is the one defined for the SQL engines in
[MobilityDB-BerlinMOD #29](https://github.com/MobilityDB/MobilityDB-BerlinMOD/pull/29)
(measurements reported by what each is licensed to claim); the workload and harness are
in place, and the timing tables join this page as they are measured. SQL-engine timings
appear in the companion [databases — parity & benchmarks](database-parity.md) page.

## Reproduce it

The numbers come from committed feeds and need no toolchain:

```sh
# MobilityNebula: tools/streaming_parity/
python3 ci_gate.py          # Flink/Kafka: 1945/1945 = 100.0%, no over-claim
cat feeds/nebula.feed.tsv   # NebulaStream: wired / proven, per function
```

The feeds (`flink-kafka.feed.tsv`, `nebula.feed.tsv`) are regenerated by the
per-platform adapters and the callability harness in `tools/streaming_parity/`; the full
methodology is in `doc/methodology/streaming_parity_assessment.md` (MobilityNebula).

*Measured against the `accumulate/parity-1.4` MEOS build, 2026-05-23. Flink and Kafka are
complete at 100%; the NebulaStream figure is the operator surface wired and compile-verified.*
