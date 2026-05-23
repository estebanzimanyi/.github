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

<img src="https://raw.githubusercontent.com/MobilityDB/.github/main/profile/images/mobilitydb_ecosystem.svg?v=2" width="800" alt="MobilityDB Ecosystem — MEOS C core as the foundation; MobilityDB/MobilityDuck/MobilitySpark SQL layers, MobilityNebula/MobilityKafka/MobilityFlink stream layers, MobilityAPI plus the MEOS-API OpenAPI/MCP/runtime contracts as the HTTP/API layer, and six language bindings as peer surfaces; MEOS-API as a side codegen catalog (IDL JSON + shape catalog); application, visualization and cloud as the top layer; a portable-data band (Arrow C Data Interface, TemporalParquet, Temporal Data Lake) beneath MEOS" />

Each section below maps to a colored box in the figure (its heading marker matches the box color); each bullet is one of that box's inner components.

### 🟩 Portable data

The interchange band drawn beneath MEOS: trajectories move between the engines and a **Temporal Data Lake** without re-encoding — the data-side complement of the SQL layers' *portable computation*. Both properties are catalogued in the mobility-platform interoperability index (in [MobilityDB](https://github.com/MobilityDB/MobilityDB), `doc/temporal-parquet/`).

- **Arrow C Data Interface** — the zero-copy **in-memory** form MEOS exposes, so engines share trajectories without re-encoding ([Apache Arrow standard](https://arrow.apache.org/docs/format/CDataInterface.html)).
- **TemporalParquet** — the **on-disk** form: a [Parquet](https://parquet.apache.org/) footer convention for temporal types ([RFC #870](https://github.com/MobilityDB/MobilityDB/discussions/870)).
- **Temporal Data Lake** — the **storage architecture**: trajectories as [Apache Iceberg](https://iceberg.apache.org/) tables under an [Apache Polaris](https://polaris.apache.org/) REST catalog (RBAC, multi-tenancy, credential vending), read by columnar engines such as [Polars](https://pola.rs/) straight off the Arrow stream ([RFC #913](https://github.com/MobilityDB/MobilityDB/discussions/913)).

### 🟪 Core C library

- **[MEOS](https://libmeos.org)** — Mobility Engine, Open Source: the canonical C library underlying every other piece.

### 🟫 Tooling

[MEOS-API](https://github.com/MobilityDB/MEOS-API) is a machine-readable description of the MEOS C-library API, generated from the MEOS headers via libclang:

- **IDL JSON** (`meos-api.json`) — the function and type catalog.
- **Shape-metadata catalog** — argument/return shape annotations for faithful code generation.

From this catalog the ecosystem generates the **language bindings** (PyMEOS, JMEOS, GoMEOS, meos-rs, MEOS.NET, MEOS.js — JMEOS also backs the MobilityFlink and MobilityKafka stream layers) and the **HTTP API contracts** (OpenAPI / MCP / runtime server, shown in the HTTP / API layer below).

### 🟦 SQL layers

Three SQL surfaces share the same MEOS-backed type system, function catalog, and BerlinMOD reference queries — the same query text runs against any of the three. The parity contract: **the same BerlinMOD reference queries run across all three surfaces and must return identical results**, validated by the cross-platform conformance suite in [MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD).

- **[MobilityDB](https://github.com/MobilityDB/MobilityDB)** · [PostgreSQL](https://www.postgresql.org/) — the project's reference SQL surface (PostgreSQL extension), spatiotemporally indexed via [mest](https://github.com/MobilityDB/mest).
- **[MobilityDuck](https://github.com/MobilityDB/MobilityDuck)** · [DuckDB](https://duckdb.org/) — peer SQL layer for analytics / columnar workloads.
- **[MobilitySpark](https://github.com/MobilityDB/MobilitySpark)** · [Apache Spark](https://spark.apache.org/) — peer SQL layer for distributed, large-scale workloads (MEOS-backed UDFs + DataFrame integration).

### 🟥 Stream layers

The same edge-to-cloud model runs on the streaming side, each tool in its canonical role. The published reference architecture is [*MobilityNebula* (EDBT 2026)](https://docs.mobilitydb.com/pub/MobilityNebula_EDBT_2026.pdf), with real railway data (SNCB) as the application demonstration. The parity contract matches the SQL-layer one: **the same BerlinMOD reference queries run across all three platforms in three streaming forms — continuous (always-on), windowed (tumbling / sliding / session), and snapshot (query at time T, ≡ the batch result at the same scale factor)** — the snapshot form anchored to the batch BerlinMOD outputs. The Flink and Kafka platforms reach MEOS through a single `MEOSBridge` over [JMEOS](https://github.com/MobilityDB/JMEOS); MobilityNebula calls MEOS C directly.

- **[MobilityNebula](https://github.com/MobilityDB/MobilityNebula)** · [NebulaStream](https://nebula.stream/) — the **edge**.
- **[MobilityKafka](https://github.com/MobilityDB/MobilityKafka)** · [Apache Kafka](https://kafka.apache.org/) — the streaming **transport backbone**.
- **[MobilityFlink](https://github.com/MobilityDB/MobilityFlink)** · [Apache Flink](https://flink.apache.org/) — **stream processing in the cloud**.

### 🟩 HTTP / API layer

- **[MobilityAPI](https://github.com/MobilityDB/MobilityAPI)** · [OGC API – Moving Features](https://www.ogc.org/standards/ogc-api-moving-features/) — server over moving-feature collections, built on MobilityDB via PyMEOS.

Three further HTTP surfaces are projected from the **[MEOS-API](https://github.com/MobilityDB/MEOS-API)** catalog over the MEOS algebra:
- **OpenAPI** — an OpenAPI 3.1 contract.
- **MCP** — a Model Context Protocol tool manifest, so LLMs / agents call the MEOS algebra directly.
- **runtime** — a runnable HTTP server, auto-generated from the catalog, that serves each MEOS function as an endpoint; the MEOS backend behind it is swappable (a compiled `libmeos`, or a stub for testing).

### 🟪 Language bindings

Each binding follows its language community's naming convention.

- **[PyMEOS](https://github.com/MobilityDB/PyMEOS)** — Python; the reference binding, and the basis for MobilityPandas and MobilityAPI.
- **[JMEOS](https://github.com/MobilityDB/JMEOS)** — Java / JVM; also backs the MobilityFlink and MobilityKafka stream layers via `MEOSBridge`.
- **[GoMEOS](https://github.com/MobilityDB/GoMEOS)** — Go; idiomatic wrappers over the MEOS C ABI.
- **[meos-rs](https://github.com/MobilityDB/meos-rs)** — Rust; safe bindings to MEOS.
- **[MEOS.NET](https://github.com/MobilityDB/MEOS.NET)** — .NET / C#; MEOS for the .NET runtime.
- **[MEOS.js](https://github.com/MobilityDB/MEOS.js)** — JavaScript / TypeScript; MEOS in the browser and Node.

### 🟨 Application platforms

- **[MobilityPandas](https://github.com/MobilityDB/MobilityPandas)** — [MovingPandas](https://movingpandas.org/) backed by PyMEOS.
- **[MobilityOpenTripPlanner](https://github.com/MobilityDB/MobilityOpenTripPlanner)** — [OpenTripPlanner](https://www.opentripplanner.org/) multimodal trip planning.
- **[MobilityMapMatching](https://github.com/MobilityDB/MobilityMapMatching)** — map matching as a service.
- **[MobilityDB-PublicTransport](https://github.com/MobilityDB/MobilityDB-PublicTransport)** — [GTFS](https://gtfs.org/) / [NeTEx](https://netex-cen.eu/) integration.

### 🟧 Visualization and UI integrations

- **[MobilityDeck](https://github.com/MobilityDB/MobilityDeck)** — [deck.gl](https://deck.gl/).
- **[MobilityFlink-Deck](https://github.com/MobilityDB/MobilityFlink-Deck)** — [deck.gl](https://deck.gl/) on the Flink stream layer.
- **[MobilityOpenLayers](https://github.com/MobilityDB/MobilityOpenLayers)** — [OpenLayers](https://openlayers.org/).
- **[MobilityLeaflet](https://github.com/MobilityDB/MobilityLeaflet)** — [Leaflet](https://leafletjs.com/).
- **[MobilityQGIS](https://github.com/MobilityDB/MobilityQGIS)** — [QGIS](https://qgis.org/) integration.
- **[MobilityGeoServer](https://github.com/MobilityDB/MobilityGeoServer)** — [GeoServer](https://geoserver.org/).
- **[MOVE](https://github.com/MobilityDB/move)** — QGIS plugin for visualizing MobilityDB query results.
- **[Franchise](https://github.com/MobilityDB/Franchise)** — notebook SQL client for exploring MobilityDB / MEOS-backed SQL.

### 🟦 Cloud and deployment

- **[MobilityDB-AWS](https://github.com/MobilityDB/MobilityDB-AWS)** — deployment recipes and images for Amazon Web Services.
- **[MobilityDB-Azure](https://github.com/MobilityDB/MobilityDB-Azure)** — deployment recipes and images for Microsoft Azure.
- **[MobilityDB-GCP](https://github.com/MobilityDB/MobilityDB-GCP)** — deployment recipes and images for Google Cloud Platform.
- **[MobilityDB-docker](https://github.com/MobilityDB/MobilityDB-docker)** — official Docker images for MobilityDB.

### 📦 Packaging / distribution

- **[meos-feedstock](https://github.com/MobilityDB/meos-feedstock)** — conda-forge feedstock for the MEOS C library.
- **[pymeos-feedstock](https://github.com/MobilityDB/pymeos-feedstock)** — conda-forge feedstock for PyMEOS.
- **[pymeos-cffi-feedstock](https://github.com/MobilityDB/pymeos-cffi-feedstock)** — conda-forge feedstock for PyMEOS-CFFI.

### 📊 Datasets and benchmarks

[BerlinMOD](https://secondo-database.github.io/BerlinMOD/BerlinMOD.html) is the project's benchmark — a synthetic-trajectory generator and moving-object-database comparison tool that generates data on an [OpenStreetMap](https://www.openstreetmap.org/) base map via [pgRouting](https://pgrouting.org/), and the cross-platform conformance suite for the portable SQL dialect: the same queries run on all three SQL surfaces and must return identical results.

- **[MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD)** — the BerlinMOD generator and benchmark itself.
- **[MobilityDB-Brussels](https://github.com/MobilityDB/MobilityDB-Brussels)** — BerlinMOD instantiated on the **Brussels** base map (default).
- **[MobilityDB-BerlinMOD-Hanoi](https://github.com/MobilityDB/MobilityDB-BerlinMOD-Hanoi)** — BerlinMOD instantiated on the **Hanoi** (Vietnam) base map.

### 🎓 Education and workshops

- **[MobilityDB-workshop](https://github.com/MobilityDB/MobilityDB-workshop)** — hands-on workshop materials.
- **[MobilityDataScienceBook](https://github.com/MobilityDB/MobilityDataScienceBook)** — companion datasets and scripts for the textbook.

### 📖 Documentation and websites

- **[libmeos-website](https://github.com/MobilityDB/libmeos-website)** — source of [libmeos.org](https://libmeos.org), the project's public front door.
- **[mobilitydb-website](https://github.com/MobilityDB/mobilitydb-website)** — source of the MobilityDB project website.

### 🔬 Research

- **[MobilityDB-Semantic](https://github.com/MobilityDB/MobilityDB-Semantic)** — semantic trajectories in MobilityDB; reproducible artifacts accompanying the research.
- **[MobilityDB-TPCDS](https://github.com/MobilityDB/MobilityDB-TPCDS)** — a TPC-DS-based temporal data-warehouse benchmark; reproducible artifacts accompanying the [temporal-OLAP article](https://link.springer.com/article/10.1007/s00778-024-00889-2).

### 🗂️ Indexing primitives

[mest](https://github.com/MobilityDB/mest) provides Multi-Entry GiST and SP-GiST access methods for PostgreSQL — variants of GiST / SP-GiST that index complex and composite types more efficiently. The repository ships three extensions:

- **mest** — multi-entry R-tree / Quadtree for the PostgreSQL `multirange` and `path` types.
- **postgis-mest** — multi-entry R-tree / Quadtree / Kd-tree for PostGIS `geometry` / `geography`.
- **mobilitydb-mest** — the same for MobilityDB's MEOS types (`spanset`, `tgeompoint`) — the spatiotemporal indexes MobilityDB relies on, including in the cross-platform BerlinMOD benchmark.

### 🗄️ Archived

Preserved in read-only form for historical reference and to keep existing links resolvable. Each carries an in-README banner pointing at its successor.

- **[MobilityDB-python](https://github.com/MobilityDB/MobilityDB-python)** → [PyMEOS](https://github.com/MobilityDB/PyMEOS)
- **[MobilityDB-JDBC](https://github.com/MobilityDB/MobilityDB-JDBC)** → [JMEOS](https://github.com/MobilityDB/JMEOS)
- **[pg_mfserv](https://github.com/MobilityDB/pg_mfserv)** → [MobilityAPI](https://github.com/MobilityDB/MobilityAPI)
- **[MobilityPySpark](https://github.com/MobilityDB/MobilityPySpark)** → [MobilitySpark](https://github.com/MobilityDB/MobilitySpark)

## Where to start

| If you want to… | Go to |
|---|---|
| Understand what MEOS is, the type system, encodings, tutorials | [libmeos.org](https://libmeos.org) |
| Use the SQL surface | [MobilityDB](https://github.com/MobilityDB/MobilityDB) (PostgreSQL), [MobilityDuck](https://github.com/MobilityDB/MobilityDuck) (DuckDB), or [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) (Spark) |
| Process trajectories as streams | [MobilityNebula](https://github.com/MobilityDB/MobilityNebula) (NebulaStream), [MobilityKafka](https://github.com/MobilityDB/MobilityKafka) (Kafka), or [MobilityFlink](https://github.com/MobilityDB/MobilityFlink) (Flink) |
| Serve or call MEOS over HTTP | [MobilityAPI](https://github.com/MobilityDB/MobilityAPI) — [OGC API – Moving Features](https://www.ogc.org/standards/ogc-api-moving-features/) over feature collections; [MEOS-API](https://github.com/MobilityDB/MEOS-API) — an OpenAPI 3.1 contract, an MCP tool manifest and a runtime server over the MEOS algebra |
| Move data between engines / build a data lake | The [Arrow C Data Interface](https://arrow.apache.org/docs/format/CDataInterface.html) export + Parquet / *TemporalParquet*; the **Temporal Data Lake** stores to [Apache Iceberg](https://iceberg.apache.org/) under an [Apache Polaris](https://polaris.apache.org/) catalog, read by [Polars](https://pola.rs/) — see the interoperability index in [MobilityDB](https://github.com/MobilityDB/MobilityDB) (`doc/temporal-parquet/`) |
| Use MEOS from your language | [PyMEOS](https://github.com/MobilityDB/PyMEOS) (Python), [JMEOS](https://github.com/MobilityDB/JMEOS) (Java / JVM), [GoMEOS](https://github.com/MobilityDB/GoMEOS) (Go), [meos-rs](https://github.com/MobilityDB/meos-rs) (Rust), [MEOS.NET](https://github.com/MobilityDB/MEOS.NET) (.NET / C#), or [MEOS.js](https://github.com/MobilityDB/MEOS.js) (JavaScript / TypeScript) |
| Cite the project in academic work | The book reference above; or the `CITATION.cff` of any binding repo |

## Acknowledgements

<img src="https://github.com/MobilityDB/MobilityDB/blob/master/doc/images/eu-flag.jpg" alt="EU Flag" style="width: 100px; float:left; margin-right: 10px;" align="middle" />
<p>
The MobilityDB project has received funding from the European Union's <a href="https://open-research-europe.ec.europa.eu/gateways/horizon-europe">Horizon Europe</a> research and innovation programme under grant agreements No 101070279 <a href="https://mobispaces.eu/" target="blank">MobiSpaces</a> and No 101093051 <a href="https://emeralds-horizon.eu/" target="blank">EMERALDS</a>.
</p>
