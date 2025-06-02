#!/bin/bash

echo "⏳ Waiting for Elasticsearch to be ready..."
until curl -s http://elasticsearch:9200 >/dev/null; do
  sleep 2
done

echo "🚀 Applying Elasticsearch index template..."
curl -X PUT "http://elasticsearch:9200/_index_template/log-template" \
     -H "Content-Type: application/json" \
     --data @/elastic_search/config.json

echo "✅ Template applied!"