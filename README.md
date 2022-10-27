
# Purpose

This application will export data from the Sierra ILS, and cache it for purpose of feeding collection analysis tools

[https://collection-analysis.cincy.pl/](https://collection-analysis.cincy.pl/)

## Overview

This script will connect to the Sierra database and use the SQL feature to collect required information from the database views for use with the CollectionHQ service.

## Documentation

### collection analysis tool

[https://ilsweb.cincinnatilibrary.org/collection-analysis-docs/](https://ilsweb.cincinnatilibrary.org/collection-analysis-docs/)

## Running the server

Files and configurations for running the server can be found here:

[datasette-cincy.pl](datasette-cincy.pl)

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
