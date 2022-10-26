
# Purpose

This application will export data from the Sierra ILS, and cache it for purpose of feeding collection analysis tools

[https://ilsweb.cincinnatilibrary.org/collection-analysis/](https://ilsweb.cincinnatilibrary.org/collection-analysis/)

## Overview

This script will connect to the Sierra database and use the SQL feature to collect required information from the database views for use with the CollectionHQ service.

## Documentation

### collection analysis tool

[https://ilsweb.cincinnatilibrary.org/collection-analysis-docs/](https://ilsweb.cincinnatilibrary.org/collection-analysis-docs/)


## Building SQLite DB / Export Process 

For the purpose of hosting an instance of Datasette, we can build an SQLite 
database from the Jupyter Notebook : [collection-analysis.cincy.pl_gen_db.ipynb](collection-analysis.cincy.pl_gen_db.ipynb)

Run the notebook in the terminal like this:

```bash
jupyter nbconvert \
--execute --to notebook \
--output output \
collection-analysis.cincy.pl_gen_db.ipynb
```
~
