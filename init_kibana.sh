#!/bin/sh

echo "⏳ Waiting for Kibana to become ready..."
until curl -s http://kibana:5601/api/status | grep -q '"state":"green"'; do
  echo "⌛ Kibana not ready yet..."
  sleep 5
done

echo "🚀 Creating index pattern from JSON file..."
curl -X POST http://kibana:5601/api/saved_objects/index-pattern \
  -H 'Content-Type: application/json' \
  -H 'kbn-xsrf: true' \
  -d @/kibana/create_index.json  # adjust this path if needed

echo "✅ Done creating index pattern!"
