#!/bin/bash
cd docs/
make html
cd ..
rsync -Pav --delete \
	./docs/_build/html/ \
	ilsweb-behind:/home/plchuser/html/collection-analysis-docs/
