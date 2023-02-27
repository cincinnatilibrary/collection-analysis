#!/bin/bash
cd "$(dirname "$0")"

source venv/bin/activate
pwd
jupyter nbconvert \
--execute --to notebook \
--output output \
collection-analysis.cincy.pl_gen_db.ipynb
