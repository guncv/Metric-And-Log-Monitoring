#!/bin/sh

echo "⏳ Waiting for Kibana..."
until curl -s http://kibana:5601/api/status > /dev/null; do sleep 5; done

echo "🚀 Importing saved objects..."
curl -X POST http://kibana:5601/api/saved_objects/_import?overwrite=true \
     -H "kbn-xsrf: true" \
     -F file=@/tmp/kibana.ndjson
