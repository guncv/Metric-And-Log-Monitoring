#!/bin/sh

echo "⏳ Waiting for Kibana..."
until curl -s http://kibana:5601/api/status | grep -q '"state":"green"'; do
  echo "⌛ Kibana not ready yet..."
  sleep 5
done

echo "🚀 Importing saved index patterns from NDJSON..."

curl -X POST http://kibana:5601/api/saved_objects/_import?overwrite=true \
     -H "kbn-xsrf: true" \
     -F file=@/kibana/create_index.ndjson

echo "✅ Done importing index patterns!"
