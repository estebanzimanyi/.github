MobilityDB Ecosystem
====================

<img src="https://github.com/MobilityDB/MobilityDB/blob/master/doc/images/mobilitydb-logo.svg" width="200" alt="MobilityDB Logo" />

This organization hosts the source code for the **MobilityDB ecosystem** — an open-source platform for geospatial trajectory data management and analysis.

For the **conceptual overview, type system, tutorials, quickstarts, and encoding specifications**, see [**libmeos.org**](https://libmeos.org) — the project's public front door. This page is the **repository map**: where each piece of code lives.

The project is developed by the Computer & Decision Engineering Department of the [Université libre de Bruxelles (ULB)](https://www.ulb.be/) under the direction of [Prof. Esteban Zimányi](http://cs.ulb.ac.be/members/esteban/). ULB is an OGC Associate Member and member of the OGC Moving Feature Standard Working Group ([MF-SWG](https://www.ogc.org/projects/groups/movfeatswg)).

<img src="https://github.com/MobilityDB/MobilityDB/blob/master/doc/images/OGC_Associate_Member_3DR.png" width="100" alt="OGC Associate Member Logo" />

## Book

Detailed explanations and application scenarios are in the project's textbook:

> Mahmoud Sakr, Alejandro Vaisman, Esteban Zimányi.
> [*Mobility Data Science: From Data to Insights*](https://link.springer.com/book/10.1007/978-3-031-82636-8). Springer, 2025.

The companion datasets and reproducible scripts live in [MobilityDataScienceBook](https://github.com/MobilityDB/MobilityDataScienceBook).

<img src="https://github.com/MobilityDB/MobilityDataScienceBook/blob/main/978-3-031-82636-8.webp" width="150" alt="Mobility Data Science Book" />

## Repository map

<img src="https://raw.githubusercontent.com/MobilityDB/.github/main/profile/images/mobilitydb_ecosystem.svg" width="800" alt="MobilityDB Ecosystem — MEOS core; MobilityDB, MobilityDuck and MobilitySpark as peer SQL surfaces; MEOS-API as a side codegen catalog projected to OpenAPI/MCP/runtime; a teal portable-data interchange band (Arrow C Data Interface, Parquet / Temporal Data Lake) beneath MEOS; and a dashed, ghosted PLANNED Stream-layers box (MobilityNebula, MobilityKafka, MobilityFlink) as a future fourth peer" />

The sections below follow the figure's boxes **bottom → top, left → right**.

### 🔄 Portable data — the interchange band beneath MEOS

This is the portable-data interchange band drawn beneath MEOS in the figure. MEOS exposes a zero-copy [Arrow C Data Interface](https://arrow.apache.org/docs/format/CDataInterface.html) and a Parquet / *TemporalParquet* on-disk form, so trajectories move between the engines and a **Temporal Data Lake** without re-encoding. It is the data-side complement of the *portable-computation* property of the SQL layers below. Both properties — and their reproducible companions — are catalogued in the mobility-platform interoperability index (in [MobilityDB](https://github.com/MobilityDB/MobilityDB), `doc/temporal-parquet/`).

### ⬛ Core C library

| Repository | Description |
|---|---|
| [MEOS](https://libmeos.org) | Mobility Engine, Open Source — the canonical C library underlying every other piece. |

### 🟫 Tooling

| Repository | Description |
|---|---|
| [MEOS-API](https://github.com/MobilityDB/MEOS-API) | Machine-readable description of the MEOS C-library API (an IDL JSON plus a shape-metadata catalog), generated from the MEOS headers via libclang. Beyond binding code-generation, the enriched catalog is projected into service contracts: an OpenAPI 3.1 contract, a Model Context Protocol (MCP) tool manifest (so LLMs/agents can call the MEOS spatiotemporal algebra directly), and a contract-driven runtime HTTP server. |

### 🟦 SQL layers (peers above MEOS)

Three SQL surfaces share the same MEOS-backed type system, function catalog, and BerlinMOD reference queries. Portable SQL means the same query text runs against any of the three. The portable named-function dialect and its rationale are described in the [edge-to-cloud SQL portability discussion (#861)](https://github.com/MobilityDB/MobilityDB/discussions/861).

This is the platform's **portable computation** property — one query text, three engines. Its data-side complement, **portable data**, is the interchange band described in the *🔄 Portable data — the interchange band beneath MEOS* section above.

| Repository | Description |
|---|---|
| [MobilityDB](https://github.com/MobilityDB/MobilityDB) | PostgreSQL extension — the project's reference SQL surface. |
| [MobilityDuck](https://github.com/MobilityDB/MobilityDuck) | DuckDB extension — peer SQL layer for analytics / columnar workloads. |
| [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) | Apache Spark plugin — peer SQL layer for distributed and large-scale workloads, with MEOS-backed UDFs and DataFrame integration. |

### 🌊 Stream layers

The same edge-to-cloud model runs on the streaming side of the ecosystem, each tool in its canonical role: [MobilityNebula](https://github.com/MobilityDB/MobilityNebula) ([NebulaStream](https://nebula.stream/)) on the **edge**, [MobilityKafka](https://github.com/MobilityDB/MobilityKafka) ([Apache Kafka](https://kafka.apache.org/)) as the streaming **transport backbone** in between, and [MobilityFlink](https://github.com/MobilityDB/MobilityFlink) ([Apache Flink](https://flink.apache.org/)) for **stream processing in the cloud**. The published reference architecture is [*MobilityNebula* (EDBT 2026)](https://docs.mobilitydb.com/pub/MobilityNebula_EDBT_2026.pdf), with real railway data (SNCB) as the application demonstration. It is the second peer in the row of peer surfaces in the figure above.

The parity contract matches the SQL-layer one: **the same BerlinMOD reference queries run across all three platforms in three streaming forms — continuous (always-on), windowed (tumbling / sliding / session), and snapshot (query at time T, ≡ the batch result at the same scale factor)** — with the snapshot form anchored to the batch BerlinMOD outputs in [MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD). The same generator and scale-factor axis as the batch side are reused.

The Flink and Kafka platforms use [JMEOS](https://github.com/MobilityDB/JMEOS); MobilityNebula calls MEOS directly through its C ABI.

The streaming-form parity matrix is scaffolded across all three runtimes — [MobilityFlink#3](https://github.com/MobilityDB/MobilityFlink/pull/3), [MobilityKafka#1](https://github.com/MobilityDB/MobilityKafka/pull/1) and [MobilityNebula#15](https://github.com/MobilityDB/MobilityNebula/pull/15) — each implementing the BerlinMOD-Q × 3-form cells in the runtime's native operator surface. MobilityFlink and MobilityKafka cover all 27 cells fully; MobilityNebula covers all 27 cells too, with 18 cells full in-runtime and 9 cells (Q5, Q6, Q9) expressed as partial — NebulaStream emits the per-window inputs and a consumer post-processes for the final BerlinMOD-Q answer. The path to "full" for those 9 cells is documented one-PR-each in the MobilityNebula scaffold.

On the JVM platforms the spatial-predicate surface routes through a single `MEOSBridge` class — [MobilityFlink#4](https://github.com/MobilityDB/MobilityFlink/pull/4) and [MobilityKafka#2](https://github.com/MobilityDB/MobilityKafka/pull/2) — calling MEOS' `geog_dwithin` over WGS84 geographies via [JMEOS#18](https://github.com/MobilityDB/JMEOS/pull/18)'s `utils.spatial.Haversine` and `utils.spatial.PointToSegment` wrappers when libmeos is loadable, with a pure-Java great-circle fallback for the mini-cluster local-test runs. The 27 cells × 2 platforms are now MEOS-backed at every predicate AND distance site; NebulaStream calls MEOS C ABI directly with no bridge layer needed.

On the NebulaStream side, [MobilityNebula#16](https://github.com/MobilityDB/MobilityNebula/pull/16) adds the `TEMPORAL_LENGTH` aggregation across the four pipeline layers (logical / physical / parser / lowering), upgrading the Q6 × 3 cells from partial to full. The matrix-row is now 21 of 27 cells full + 6 cells partial; the remaining 6 (Q5 × 3 + Q9 × 3) need a Cartesian aggregation following the same template and are each a single follow-up PR away.

| Repository | Engine |
|---|---|
| [MobilityNebula](https://github.com/MobilityDB/MobilityNebula) | [NebulaStream](https://nebula.stream/) — edge |
| [MobilityKafka](https://github.com/MobilityDB/MobilityKafka) | [Apache Kafka](https://kafka.apache.org/) — streaming transport backbone |
| [MobilityFlink](https://github.com/MobilityDB/MobilityFlink) | [Apache Flink](https://flink.apache.org/) — cloud stream processing |

### 🟩 HTTP / API layer

| Repository | Description |
|---|---|
| [MobilityAPI](https://github.com/MobilityDB/MobilityAPI) | HTTP server implementing the OGC API – Moving Features Standard. |

### 🟪 Language bindings of MEOS

Each binding follows its language community's naming convention.

| Repository | Language |
|---|---|
| [PyMEOS](https://github.com/MobilityDB/PyMEOS) | Python |
| [JMEOS](https://github.com/MobilityDB/JMEOS) | Java / JVM |
| [GoMEOS](https://github.com/MobilityDB/GoMEOS) | Go |
| [meos-rs](https://github.com/MobilityDB/meos-rs) | Rust |
| [MEOS.NET](https://github.com/MobilityDB/MEOS.NET) | .NET / C# |
| [MEOS.js](https://github.com/MobilityDB/MEOS.js) | JavaScript / TypeScript |

### 🟨 Application platforms

| Repository | Engine / framework |
|---|---|
| [MobilityPandas](https://github.com/MobilityDB/MobilityPandas) | [MovingPandas](https://movingpandas.org/) backed by PyMEOS |
| [MobilityOpenTripPlanner](https://github.com/MobilityDB/MobilityOpenTripPlanner) | [OpenTripPlanner](https://www.opentripplanner.org/) — multimodal trip planning |
| [MobilityMapMatching](https://github.com/MobilityDB/MobilityMapMatching) | Map matching as a service |
| [MobilityDB-PublicTransport](https://github.com/MobilityDB/MobilityDB-PublicTransport) | [GTFS](https://gtfs.org/) / [Netex](https://netex-cen.eu/) integration |

### 🟧 Visualization and UI integrations

| Repository | Stack |
|---|---|
| [MobilityDeck](https://github.com/MobilityDB/MobilityDeck) | [deck.gl](https://deck.gl/) |
| [MobilityFlink-Deck](https://github.com/MobilityDB/MobilityFlink-Deck) | [deck.gl](https://deck.gl/) on the planned Flink stream layer |
| [MobilityOpenLayers](https://github.com/MobilityDB/MobilityOpenLayers) | [OpenLayers](https://openlayers.org/) |
| [MobilityLeaflet](https://github.com/MobilityDB/MobilityLeaflet) | [Leaflet](https://leafletjs.com/) |
| [MobilityQGIS](https://github.com/MobilityDB/MobilityQGIS) | [QGIS](https://qgis.org/) integration |
| [MobilityGeoServer](https://github.com/MobilityDB/MobilityGeoServer) | [GeoServer](https://geoserver.org/) |
| [MOVE](https://github.com/MobilityDB/move) | QGIS plugin for visualizing MobilityDB query results |
| [Franchise](https://github.com/MobilityDB/Franchise) | Notebook SQL client for exploring MobilityDB / MEOS-backed SQL |

### 🔵 Cloud and deployment

| Repository | Target |
|---|---|
| [MobilityDB-AWS](https://github.com/MobilityDB/MobilityDB-AWS) | Amazon Web Services |
| [MobilityDB-Azure](https://github.com/MobilityDB/MobilityDB-Azure) | Microsoft Azure |
| [MobilityDB-GCP](https://github.com/MobilityDB/MobilityDB-GCP) | Google Cloud Platform |
| [MobilityDB-docker](https://github.com/MobilityDB/MobilityDB-docker) | Docker images |

### 📦 Packaging / distribution

| Repository | Description |
|---|---|
| [meos-feedstock](https://github.com/MobilityDB/meos-feedstock) | conda-forge feedstock for the MEOS C library. |
| [pymeos-feedstock](https://github.com/MobilityDB/pymeos-feedstock) | conda-forge feedstock for PyMEOS. |
| [pymeos-cffi-feedstock](https://github.com/MobilityDB/pymeos-cffi-feedstock) | conda-forge feedstock for PyMEOS-CFFI. |

### 🟤 Datasets and benchmarks

| Repository | Description |
|---|---|
| [MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD) | [BerlinMOD](https://secondo-database.github.io/BerlinMOD/BerlinMOD.html) data generator and benchmark, using [Open Street Map](https://www.openstreetmap.org/) data and [pgRouting](https://pgrouting.org/). Brussels by default; a Hanoi (Vietnam) instantiation lives in [MobilityDB-BerlinMOD-Hanoi](https://github.com/MobilityDB/MobilityDB-BerlinMOD-Hanoi). Also the cross-platform conformance suite for the portable SQL dialect — the same queries run on all three SQL surfaces and must return identical results. |
| [MobilityDB-Brussels](https://github.com/MobilityDB/MobilityDB-Brussels) | Real Brussels public-transport dataset (STIB, TLC) — companion data, not a BerlinMOD instantiation. |
| [MobilityDB-TPCDS](https://github.com/MobilityDB/MobilityDB-TPCDS) | TPC-DS benchmark adaptation. |

### 🟢 Education and workshops

| Repository | Description |
|---|---|
| [MobilityDB-workshop](https://github.com/MobilityDB/MobilityDB-workshop) | Hands-on workshop materials. |
| [MobilityDataScienceBook](https://github.com/MobilityDB/MobilityDataScienceBook) | Companion datasets and scripts for the textbook. |

### 📖 Documentation and websites

| Repository | Description |
|---|---|
| [libmeos-website](https://github.com/MobilityDB/libmeos-website) | Source of [libmeos.org](https://libmeos.org) — the project's public front door (concepts, type system, tutorials, bindings). |
| [mobilitydb-website](https://github.com/MobilityDB/mobilitydb-website) | Source of the MobilityDB project website. |

### 🟥 Research

| Repository | Description |
|---|---|
| [MobilityDB-Semantic](https://github.com/MobilityDB/MobilityDB-Semantic) | Semantic-trajectory research project. |

### 🟣 Indexing primitives

| Repository | Description |
|---|---|
| [mest](https://github.com/MobilityDB/mest) | Multi-Entry Search Trees for PostgreSQL — generic indexing primitive used by MobilityDB. |

### ⬜ Archived

These repositories are preserved in read-only form for historical reference and to keep existing links resolvable. Each carries an in-README banner pointing at its successor.

| Archived repository | Successor / replacement |
|---|---|
| [MobilityDB-python](https://github.com/MobilityDB/MobilityDB-python) | [PyMEOS](https://github.com/MobilityDB/PyMEOS) |
| [MobilityDB-JDBC](https://github.com/MobilityDB/MobilityDB-JDBC) | [JMEOS](https://github.com/MobilityDB/JMEOS) |
| [pg_mfserv](https://github.com/MobilityDB/pg_mfserv) | [MobilityAPI](https://github.com/MobilityDB/MobilityAPI) |
| [MobilityPySpark](https://github.com/MobilityDB/MobilityPySpark) | [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) |

## Where to start

| If you want to… | Go to |
|---|---|
| Understand what MEOS is, the type system, encodings, tutorials | [libmeos.org](https://libmeos.org) |
| Use the SQL surface | [MobilityDB](https://github.com/MobilityDB/MobilityDB) (PostgreSQL), [MobilityDuck](https://github.com/MobilityDB/MobilityDuck) (DuckDB), or [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) (Spark) |
| Move data between engines / build a data lake | The [Arrow C Data Interface](https://arrow.apache.org/docs/format/CDataInterface.html) export + Parquet — see the interoperability index in [MobilityDB](https://github.com/MobilityDB/MobilityDB) (`doc/temporal-parquet/`) |
| Use MEOS from your language | The corresponding [language binding](https://libmeos.org/bindings/) |
| Cite the project in academic work | The book reference above; or the `CITATION.cff` of any binding repo |

## Acknowledgements

<img src="https://github.com/MobilityDB/MobilityDB/blob/master/doc/images/eu-flag.jpg" alt="EU Flag" style="width: 100px; float:left; margin-right: 10px;" align="middle" />
<p>
The MobilityDB project has received funding from the European Union's <a href="https://open-research-europe.ec.europa.eu/gateways/horizon-europe">Horizon Europe</a> research and innovation programme under grant agreements No 101070279 <a href="https://mobispaces.eu/" target="blank">MobiSpaces</a> and No 101093051 <a href="https://emeralds-horizon.eu/" target="blank">EMERALDS</a>.
</p>
