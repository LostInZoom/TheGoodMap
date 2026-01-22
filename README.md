# TheGoodMap

> Cartographic application based on vector tiles, PostGIS and Martin.

---

## 📌 Overview

**La Bonne Carte** is a cartographic application designed to visualize and explore geographic data efficiently. The project relies on a vector-tile-based architecture to ensure good performance and scalability.

The application uses:

* **Martin** as a vector tile server (MVT)
* **PostgreSQL / PostGIS** as the spatial database
* **MapLibre-compatible `style.json` files** for cartographic styling

P

## 🗄 Database

The project uses **PostgreSQL with the PostGIS extension**.

**Requirements**:

* PostgreSQL ≥ 16
* PostGIS enabled

SQL scripts provided in this repository allow you to:


* Optimize data for cartographic rendering (indexes, simplification, etc.)

---

## 🗺 Vector tile server (Martin)

[Martin](https://martin.maplibre.org/) is used to serve PostGIS data as **vector tiles (MVT)**.

### Installation

Install Martin from the official repository or using your system package manager.

### Run Martin

Once installed, start the server from the command line in the repository martin:

```bash
martin --config martin/config_bis.yaml
```

Make sure that:

* PostgreSQL is running
* Connection parameters are correctly defined in the configuration file

---

## 🎨 Cartographic styling

Map styling is handled through **`thegoodmap/style.json`** files compatible with MapLibre.

These files define:

* Displayed layers
* Styling rules (colors, sizes, filters)
* Zoom-dependent rendering behavior

---

## 🚀 Getting started

1. Install PostgreSQL and PostGIS
2. import data `data/martin_la_bonne_carte.sql` in PostgreSQL
3. Install Martin
4. Run Martin from the command line
5. Load a `style.json` file in your MapLibre client

---

## 📄 License

Specify the license here.

---
