# Metric-And-Log-Monitoring

A real-time observability stack for structured logs and metri across **multiple API services** using Fluent Bit, Elasticsearch, Kibana, Prometheus, and Grafana.

---

## 🧭 Overview Diagram

<p align="center">
  <img src="meta/overview_diagram.png" width="750"/>
</p>

---

## 🔧 Components

### 🔹 **1. Server (Source of Logs and Metrics)**

* Each server exposes:

  * A `/metrics` endpoint (e.g., via Prometheus client in Flask, Node Exporter, etc.)
  * Structured logs, which are forwarded via the **Fluent Bit forward protocol**

---

### 🔸 **2. Metric Monitoring Pipeline**

#### 🟠 **Prometheus**

* **Pulls metrics** from each server's `/metrics` endpoint on a scheduled interval
* Stores time-series data in an internal TSDB (Time Series Database)

#### 🟠 **Grafana**

* **Pulls data** from Prometheus via **PromQL queries**
* Displays custom dashboards for:

  * HTTP request count and rates
  * Response time (p95, p99)
  * CPU, memory, and disk usage
  * Alert thresholds (visual + AlertManager integration)

---

### 🔸 **3. Log Monitoring Pipeline**

#### 🔵 **Fluent Bit**

* Listens on multiple TCP ports (e.g., `24224`, `24225`, `24226`)
* **Pulls data** from each port via the **forward protocol**
* Filters, parses, and structures logs from each server/service
* **Pushes logs** to **Elasticsearch** using the HTTP API

#### 🔵 **Elasticsearch**

* Stores logs in **daily rotated indices**, such as:

  * `api-server-1-logs-*`
  * `api-server-2-logs-*`
  * `api-server-3-logs-*`
* Supports full-text search and log aggregation

#### 🔵 **Kibana**

* **Pulls data** from Elasticsearch via dynamic queries
* Visualizes logs with:

  * Time-based filters
  * Custom dashboards
  * Searchable fields per service

---

## 📦 Folder Structure

```
├── demo_app/                 # Flask apps with Prometheus + Fluent logging
├── elastic_search/          # Elasticsearch configs and index template
├── grafana/                 # Dashboards and datasources
├── kibana/                  # Index pattern loaders
├── log_collections/         # Fluent Bit configs and parsers
├── metrics/                 # Prometheus rules and alertmanager.yml
├── docker-compose.yaml      # Stack orchestration
├── init_elastic_search.sh   # Auto apply ES template
├── init_kibana.sh           # Auto create Kibana index patterns
└── README.md
```

---
Here's an enhanced version of your **✅ Getting Started** section — now including:

* The mock traffic script (to simulate logs and metrics)
* Access URLs for **Kibana (5601)** and **Grafana (3000)**
* Clear instructions after `make rebuild`

---

## ✅ Getting Started

### 📥 Clone the Repository

```bash
git clone https://github.com/guncv/Metric-And-Log-Monitoring.git
cd Metric-And-Log-Monitoring
```

---

### 🔄 Rebuild the Entire Monitoring Stack

```bash
make rebuild
```

This will:

* Start all containers (Fluent Bit, Elasticsearch, Kibana, Prometheus, Grafana, etc.)
* Auto-apply index templates and Kibana patterns
* Expose services on the correct ports

---

### 🚀 Simulate Traffic (Generate Logs & Metrics)

Once the stack is running, you can **mock API requests** to generate traffic:

```bash
for i in {1..1000}; do curl -s http://localhost:5003/ > /dev/null; done
sleep 1
for i in {1..1000}; do curl -s http://localhost:5001/ > /dev/null; done
sleep 1
for i in {1..1000}; do curl -s http://localhost:5002/ > /dev/null; done
```

This will:

* Generate structured logs per app (to be parsed by Fluent Bit)
* Populate Prometheus metrics (e.g., request count, latency)

---

### 🌐 Access Dashboards

| Tool        | URL                                            | Purpose                     |
| ----------- | ---------------------------------------------- | --------------------------- |
| **Kibana**  | [http://localhost:5601](http://localhost:5601) | View logs, search, filter   |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | View metrics and dashboards |

---

### 📊 What You’ll See:

<p align="center">
  <img src="meta/log_visualization.png" width="750"/>
</p>

<p align="center"><strong>🔍 Live Structured Logs per App in Kibana</strong></p>

<p align="center">
  <img src="meta/metric_visualization.png" width="750"/>
</p>

<p align="center"><strong>📈 Multi-App Metrics Dashboard in Grafana</strong></p>

