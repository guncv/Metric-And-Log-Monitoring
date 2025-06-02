# Metric-And-Log-Monitoring

A real-time observability stack for structured logs and metri across **multiple API services** using Fluent Bit, Elasticsearch, Kibana, Prometheus, and Grafana.

---

## 🧭 Overview Diagram

```mermaid
graph TD
    subgraph API Servers
        A1[demon-app-first:5001] --> FBit1
        A2[demon-app-second:5002] --> FBit2
        A3[demon-app-third:5003] --> FBit3
    end

    subgraph Fluent Bit (Log Collector)
        FBit1[Forward Input 24224] --> ES1
        FBit2[Forward Input 24225] --> ES2
        FBit3[Forward Input 24226] --> ES3
    end

    subgraph Elasticsearch
        ES1[api-server-1-logs-*]
        ES2[api-server-2-logs-*]
        ES3[api-server-3-logs-*]
    end

    subgraph Kibana
        KB1[Kibana Index Patterns] --> KBUI[Kibana UI]
        ES1 --> KB1
        ES2 --> KB1
        ES3 --> KB1
    end

    subgraph Prometheus
        A1 --> PM
        A2 --> PM
        A3 --> PM
        PM --> AlertManager
        PM --> Grafana
    end

    AlertManager -->|Email| EmailSys
    subgraph Grafana
        GF[Dashboards]
    end

    PM --> GF
```

---

## 🔧 Components

### 1. **Log Collection**

* **Fluent Bit** is configured with multiple `[INPUT]` ports (24224, 24225, 24226)
* Each app sends structured logs to Fluent Bit via TCP
* Logs are parsed, filtered (e.g., removing `_type`, `_score`), and sent to Elasticsearch indices

### 2. **Storage**

* **Elasticsearch** stores time-series logs in daily indices:

  * `api-server-1-logs-*`
  * `api-server-2-logs-*`
  * `api-server-3-logs-*`

### 3. **Visualization**

* **Kibana** auto-configured with multiple index patterns
* Provides search, filter, and time-based exploration

### 4. **Metrics**

* **Prometheus** scrapes `/metrics` from Flask apps
* **AlertManager** sends email alerts based on thresholds (CPU, memory, disk)
* **Grafana** provides dashboards with:

  * Server requests
  * API response codes (2xx, 4xx, 5xx)
  * Latency p95
  * System resource usage

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

## ✅ Getting Started

```bash
git clone <this-repo>
make rebuild  # removes & rebuilds entire monitoring stack
```

You’ll get:

* Live structured logs per app in Kibana
* Real-time alerts by email
* Multi-app metric dashboards in Grafana

---

## 📬 Contributions

* Add more app services
* Extend metric rules (e.g., DB latency, queue depth)
* Improve filtering and template mapping in Fluent Bit
