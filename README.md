# Metric-And-Log-Monitoring

A real-time observability stack for structured logs and metri across **multiple API services** using Fluent Bit, Elasticsearch, Kibana, Prometheus, and Grafana.

---

## 🧭 Overview Diagram

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
```

```
make rebuild  # removes & rebuilds entire monitoring stack
```

You’ll get:

![image](https://github.com/user-attachments/assets/9320956b-1a9c-41d8-b482-c997846f52e1)
## Live structured logs per app in Kibana


![image](https://github.com/user-attachments/assets/4798ff32-6119-4fce-8cca-5f991638c85e)
## Multi-app metric dashboards in Grafana

---

## 📬 Contributions

* Add more app services
* Extend metric rules (e.g., DB latency, queue depth)
* Improve filtering and template mapping in Fluent Bit
