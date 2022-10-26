#!/bin/bash
cd "$(dirname "$0")"

source venv/bin/activate
pwd
papermill collection-analysis.cincy.pl_gen_db.ipynb -p gen_collection 'daily' output.ipynb
