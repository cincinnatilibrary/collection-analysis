Examples and Uses
=================

There are many use-cases for these data sets--some examples can be found below.

**TODO** add many use-cases

Aggregate Counts
----------------

This basic example gives an overall count of the numbers of items included in the snapshots.

.. code-block:: sql

   select
      count(distinct b.bib_record_num)
   from
      bib as b
      join item as i on i.bib_record_num = b.bib_record_num