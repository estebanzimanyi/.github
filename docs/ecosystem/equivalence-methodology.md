# Equivalence measurement methodology

Shared, cross-machine reference for every MobilityDB-ecosystem tool — MobilityDB, MobilityDuck,
MobilitySpark, MobilityFlink, MobilityKafka, MobilityNebula, PyMEOS, GoMEOS, MEOS.NET, MEOS.js.

## Purpose

The consolidation of a large body of work is delivered as many **one-change deliverable PRs**
(reviewer attention is the scarce resource). An **accumulate / integration branch** is built only to
*prove* the integrated stack works — it is **evidence, never a merge target**. Before launching a
benchmark (or publishing a pin) on the accumulate, prove:

> **accumulate ≡ Σ(individual deliverable PRs)**

so that measuring the accumulate validly stands in for the deliverables. This document is the proven
recipe; reuse it rather than reinventing.

## 1. Symbol level is the authoritative granularity — not line or byte

The ecosystem derives from the public **surface**, so measure the surface, not the text:

| Layer | "Symbol" = |
| --- | --- |
| MEOS / MobilityDB | every `extern …(` function symbol in the public headers (`meos.h`, `meos_{geo,cbuffer,npoint,pose,rgeo,h3,pointcloud}.h`, `meos_internal*.h`) |
| MobilitySpark | each registered UDF name — `.register("<udf>")` |
| MobilityDuck | each registered scalar/aggregate function name |
| PyMEOS / GoMEOS / MEOS.NET | each exported wrapper / public binding symbol |

The binding surface is **pin-independent** (the registration names do not change with the kernel pin),
so this metric sidesteps pin drift across a stack.

## 2. The measurement (fast, local — this is the gate)

```sh
ref   = sorted -u symbols of the REFERENCE  (the accumulate tip, or the pin)
union = sorted -u symbols across ALL deliverable PR branches

comm -23 ref union   # GAPS:   in the reference, delivered by NO PR  -> a genuine hole
comm -13 ref union   # EXTRAS: in a PR, not yet in the reference     -> the accumulate is stale
```

- **GAPS** are the only genuine equivalence holes. Close each by folding it into its **owning
  deliverable PR** — never as an accumulate-only commit.
- **EXTRAS** mean the accumulate predates newer PRs; refresh the accumulate (re-merge the current PR
  tips) before benchmarking.

A healthy result is a tiny, named gap set. (MobilityDB: 3105 reference symbols, **exactly one** gap —
`meos_initialize_noexit_error_handler` — closed by a single PR.)

## 3. What is noise — do not gate on it

- **Line / hunk-level union over-counts massively.** A symbol that is present but whose line differs
  by formatting, signature wrapping, shared-catalog enum numbering, golden floating-point variants, or
  a lagging rebase base is **not** a gap.
- **Naive git-merge ("octopus") assembly is unreliable as the gate** — order-sensitive, with
  conflict-resolution artifacts and stacking-dependent goldens. A rough all-PR merge can diff
  thousands of files against a reference whose real gap is a single symbol. The reference is built by
  a specific integration process that arbitrary merging does not replicate.

## 4. Strongest proof (optional) — cumulative reconstruction

For byte-level confidence beyond the symbol gate: from the base branch, for each deliverable PR in
topological order, materialise only that PR's footprint at the reference's content and commit one
slice per PR:

```sh
git checkout <reference> -- <files owned by this PR>
git commit -m "slice: <PR>"
```

Then triple-prove the reconstructed branch: (a) source/SQL diff vs the reference is **0**; (b) it
**builds**; (c) the **full test suite passes**.

Caveats:

- `git checkout <ref> -- f` **stages** `f`. Detect a real change with `git diff --cached --quiet`,
  **not** `git diff --quiet`, or the slice commits nothing (false "no change").
- Footprint-sync cannot express a **deletion**; a file the reference removes shows as a false
  residual. Verify those per file.

## 5. Disposition

Every genuine gap closes inside its owning one-change PR, with its test and docs in the same commit.
The accumulate is then re-derived (re-merge current PR tips, merge-commit style) and re-measured until
the gap set is empty and the extra set reflects only the just-refreshed surface. Only then is the
accumulate a faithful benchmark stand-in for the deliverables.
