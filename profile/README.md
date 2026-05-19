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

<img src="https://raw.githubusercontent.com/MobilityDB/.github/main/profile/images/mobilitydb_ecosystem.svg" width="800" alt="MobilityDB Ecosystem" />

### ⬛ Core C library

| Repository | Description |
|---|---|
| [MEOS](https://libmeos.org) | Mobility Engine, Open Source — the canonical C library underlying every other piece. |

### 🟦 SQL layers (peers above MEOS)

| Repository | Description |
|---|---|
| [MobilityDB](https://github.com/MobilityDB/MobilityDB) | PostgreSQL extension. The project's reference SQL surface. |
| [MobilityDuck](https://github.com/MobilityDB/MobilityDuck) | DuckDB extension. Peer SQL layer for analytics and columnar workloads. |
| [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) | Apache Spark layer. Peer SQL surface for large-scale distributed analytics, exposing MEOS through Spark SQL. |

### 🟩 HTTP / API layer

| Repository | Description |
|---|---|
| [MobilityAPI](https://github.com/MobilityDB/MobilityAPI) | HTTP server implementing the OGC API – Moving Features Standard. |

### 🟪 Language bindings of MEOS

Each binding follows its language community's naming convention.

| Repository | Language |
|---|---|
| [PyMEOS](https://github.com/MobilityDB/PyMEOS) | Python |
| [PyMEOS-CFFI](https://github.com/MobilityDB/PyMEOS-CFFI) | Python (low-level CFFI layer underlying PyMEOS) |
| [JMEOS](https://github.com/MobilityDB/JMEOS) | Java / JVM |
| [GoMEOS](https://github.com/MobilityDB/GoMEOS) | Go |
| [meos-rs](https://github.com/MobilityDB/meos-rs) | Rust |
| [MEOS.NET](https://github.com/MobilityDB/MEOS.NET) | .NET / C# |
| [MEOS.js](https://github.com/MobilityDB/MEOS.js) | JavaScript / TypeScript |

Runnable example programs and notebooks live in [PyMEOS-Examples](https://github.com/MobilityDB/PyMEOS-Examples) (Python) and [JMEOS-Examples](https://github.com/MobilityDB/JMEOS-Examples) (Java).

### 🟫 Tooling

| Repository | Description |
|---|---|
| [MEOS-API](https://github.com/MobilityDB/MEOS-API) | Machine-readable description of the MEOS C-library API (an IDL JSON plus a shape-metadata catalog), generated from the MEOS headers via libclang. Beyond binding code-generation, the enriched catalog is projected into service contracts: an OpenAPI 3.1 contract, a Model Context Protocol (MCP) tool manifest (so LLMs/agents can call the MEOS spatiotemporal algebra directly), and a contract-driven runtime HTTP server. |

### 🟧 Visualization and UI integrations

| Repository | Stack |
|---|---|
| [MobilityDeck](https://github.com/MobilityDB/MobilityDeck) | [deck.gl](https://deck.gl/) |
| [MobilityOpenLayers](https://github.com/MobilityDB/MobilityOpenLayers) | [OpenLayers](https://openlayers.org/) |
| [MobilityLeaflet](https://github.com/MobilityDB/MobilityLeaflet) | [Leaflet](https://leafletjs.com/) |
| [MobilityQGIS](https://github.com/MobilityDB/MobilityQGIS) | [QGIS](https://qgis.org/) integration |
| [MobilityGeoServer](https://github.com/MobilityDB/MobilityGeoServer) | [GeoServer](https://geoserver.org/) |
| [move](https://github.com/MobilityDB/move) | QGIS plugin for visualizing MobilityDB query results |

### 🟨 Application platforms

| Repository | Engine / framework |
|---|---|
| [MobilityFlink](https://github.com/MobilityDB/MobilityFlink) | [Apache Flink](https://flink.apache.org/) — streaming |
| [MobilityFlink-Deck](https://github.com/MobilityDB/MobilityFlink-Deck) | Flink + deck.gl integration |
| [MobilityKafka](https://github.com/MobilityDB/MobilityKafka) | [Apache Kafka](https://kafka.apache.org/) — streaming |
| [MobilityNebula](https://github.com/MobilityDB/MobilityNebula) | [NebulaStream](https://nebula.stream/) |
| [MobilityPandas](https://github.com/MobilityDB/MobilityPandas) | [MovingPandas](https://movingpandas.org/) backed by PyMEOS |
| [MobilityOpenTripPlanner](https://github.com/MobilityDB/MobilityOpenTripPlanner) | [OpenTripPlanner](https://www.opentripplanner.org/) — multimodal trip planning |
| [MobilityMapMatching](https://github.com/MobilityDB/MobilityMapMatching) | Map matching as a service |
| [MobilityDB-PublicTransport](https://github.com/MobilityDB/MobilityDB-PublicTransport) | [GTFS](https://gtfs.org/) / [Netex](https://netex-cen.eu/) integration |

### 🔵 Cloud and deployment

| Repository | Target |
|---|---|
| [MobilityDB-AWS](https://github.com/MobilityDB/MobilityDB-AWS) | Amazon Web Services |
| [MobilityDB-Azure](https://github.com/MobilityDB/MobilityDB-Azure) | Microsoft Azure |
| [MobilityDB-GCP](https://github.com/MobilityDB/MobilityDB-GCP) | Google Cloud Platform |
| [MobilityDB-docker](https://github.com/MobilityDB/MobilityDB-docker) | Docker images |

### 🟤 Datasets and benchmarks

| Repository | Description |
|---|---|
| [MobilityDB-BerlinMOD](https://github.com/MobilityDB/MobilityDB-BerlinMOD) | [BerlinMOD](https://secondo-database.github.io/BerlinMOD/BerlinMOD.html) data generator and benchmark, using [Open Street Map](https://www.openstreetmap.org/) data and [pgRouting](https://pgrouting.org/) (Brussels by default). |
| [MobilityDB-BerlinMOD-Hanoi](https://github.com/MobilityDB/MobilityDB-BerlinMOD-Hanoi) | BerlinMOD generator instantiated with OSM data for Hanoi, Vietnam. |
| [MobilityDB-Brussels](https://github.com/MobilityDB/MobilityDB-Brussels) | Brussels mobility dataset. |
| [MobilityDB-TPCDS](https://github.com/MobilityDB/MobilityDB-TPCDS) | TPC-DS benchmark adaptation. |

### 🟢 Education and workshops

| Repository | Description |
|---|---|
| [MobilityDB-workshop](https://github.com/MobilityDB/MobilityDB-workshop) | Hands-on workshop materials. |
| [MobilityDataScienceBook](https://github.com/MobilityDB/MobilityDataScienceBook) | Companion datasets and scripts for the textbook. |

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
| [MobilityPySpark](https://github.com/MobilityDB/MobilityPySpark) | [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) |
| [pg_mfserv](https://github.com/MobilityDB/pg_mfserv) | [MobilityAPI](https://github.com/MobilityDB/MobilityAPI) |

## Where to start

| If you want to… | Go to |
|---|---|
| Understand what MEOS is, the type system, encodings, tutorials | [libmeos.org](https://libmeos.org) |
| Use the SQL surface | [MobilityDB](https://github.com/MobilityDB/MobilityDB) (PostgreSQL), [MobilityDuck](https://github.com/MobilityDB/MobilityDuck) (DuckDB), or [MobilitySpark](https://github.com/MobilityDB/MobilitySpark) (Spark SQL) |
| Use MEOS from your language | The corresponding [language binding](https://libmeos.org/bindings/) |
| Cite the project in academic work | The book reference above; or the `CITATION.cff` of any binding repo |

## Acknowledgements

<img src="https://github.com/MobilityDB/MobilityDB/blob/master/doc/images/eu-flag.jpg" alt="EU Flag" style="width: 100px; float:left; margin-right: 10px;" align="middle" />
<p>
The MobilityDB project has received funding from the European Union's <a href="https://open-research-europe.ec.europa.eu/gateways/horizon-europe">Horizon Europe</a> research and innovation programme under grant agreements No 101070279 <a href="https://mobispaces.eu/" target="blank">MobiSpaces</a> and No 101093051 <a href="https://emeralds-horizon.eu/" target="blank">EMERALDS</a>.
</p>
