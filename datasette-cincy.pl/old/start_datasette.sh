#!/bin/bash

venv/bin/datasette \
	-i current_collection.db \
	-i collection_prev.db \
	-i collection-2021-01-04.db \
	-i collection-2020-01-06.db \
	--crossdb \
	--setting hash_urls 1 \
	--setting default_cache_ttl_hashed 31536000 \
	--setting force_https_urls  true \
	--setting default_page_size 100 \
	--setting sql_time_limit_ms 60000 \
	--setting max_returned_rows 3000 \
	--setting allow_facet on \
	--setting suggest_facets off \
	--setting num_sql_threads 20 \
	--setting allow_facet true \
	--setting facet_time_limit_ms 15000 \
	--setting cache_size_kb 5000 \
	--setting base_url /collection-analysis/ \
	--metadata=metadata.yaml \
	--static static:static/ \
	--port 8010
