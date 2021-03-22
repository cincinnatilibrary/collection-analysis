.. collection-analysis documentation master file, created by
   sphinx-quickstart on Tue Mar 16 16:07:10 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

collection-analysis documentation & resources
==================================================

**NOTE: This document and tool is very much a work in progress. Data in the various databases provided, and information found in this documentation is subject to change.**

The interface and included data can be found here:

* https://ilsweb.cincinnatilibrary.org/collection-analysis/

Source for these docs as well as the export / import scripts and more can be found here:

* https://github.com/cincinnatilibrary/collection-analysis


General Purpose of this Resource
--------------------------------

This resource is provided to document the snapshot process for the Cincinnati &
Hamilton County Public Library (CHPL) `"current_collection" data set <https://ilsweb.cincinnatilibrary.org/collection-analysis/>`_ and to provide other resources related to the use of this tool.

Using the Data Set
------------------

The software used to power this data set is called "Datasette" 
(https://datasette.io/) and is currently written and maintained by Simon 
Willison. Datasette documentation can be found here: 
https://docs.datasette.io/en/latest/

To explore the data, it's possible to use this tool to run SQL queries directly on the tables in each of the databases to explore 
various states of the CHPL physical collection. 

For example:
To find the number of total titles that have at least a single item associated with that title, you can use the following query.

.. code-block:: sql

   select
      count(distinct b.bib_record_num)
   from
      bib as b
      join item as i on i.bib_record_num = b.bib_record_num

`Click to Run this query on the "current_collection" snapshot database <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=select%0D%0A++count%28distinct+b.bib_record_num%29%0D%0Afrom%0D%0A++bib+as+b%0D%0A++join+item+as+i+on+i.bib_record_num+%3D+b.bib_record_num>`_

`Click to Run this query on the "collection-2021-01-04" snapshot database <https://ilsweb.cincinnatilibrary.org/collection-analysis/collection-2021-01-04-6a32a78?sql=select%0D%0A++count%28distinct+b.bib_record_num%29%0D%0Afrom%0D%0A++bib+as+b%0D%0A++join+item+as+i+on+i.bib_record_num+%3D+b.bib_record_num>`_

Below are static SQL queries for reports and analysis

.. toctree::
   :maxdepth: 2

   static_queries

More examples, general use-cases and miscellaneous information can be found below.

.. toctree::
   :maxdepth: 1
   
   examples
   misc

What is Included in the Data Set?
---------------------------------

Snapshots of the CHPL physical collection's metadata is done weekly 

There are 3 "levels" of collection metadata snapshots provided as distinct databases:

#. **current_collection**: Most-current snapshot of the metadata.
#. **collection_prev**: Previous snapshot
#. **collection-YYYY-MM-DD**: Start-of-year snapshot. (*e.g., collection-2021-01-04 would represent the state of the collection from the first Monday of 2021*)

There are two primary tables in each data snapshot (additional tables are also included to supplement these tables which can be found in the links below):

#. ``bib``: `Bibliographic <https://en.wikipedia.org/wiki/Bibliographic_record>`_ metadata associated with a resource
#. ``item``: Item-level metadata (such as item location, barcode, etc.)

More detail about what is included in each of the database snapshots can be found below.

.. toctree::
   :maxdepth: 3
   
   database_tables

Uh, OK. But, Like ...Why?
-------------------------

Data is amazing! The ability to examine, aggregate, and transform data can
give incredible and powerful insights into the large physical collection that
CHPL maintains for the public.

Reports, search tools and other really interesting and useful things can be generated from this data

For Example This:

`Top Circulating Titles With Subject Heading 'dystopias' in the CHPL Current Collection <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection-98fefc7/top_circulating_by_subject?subject=dystopias&_hide_sql=1>`_

* :ref:`search`

