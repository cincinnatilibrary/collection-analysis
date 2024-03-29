Examples and Uses
=================

There are many use-cases for these data sets--some examples can be found below.

**TODO** add many use-cases

``bib`` and ``item`` Tables
---------------------------

The ``bib`` and ``item`` tables are the two primary tables, that when combined, give a
more complete picture of the CHPL physical collection.

For example, the below query will produce a simples shelf list for a given 
location (``1cjbd`` is the Main - 1st Floor - Children's Library - Board Books location): 

.. code-block:: sql

   select
     item.item_record_num,
     item.bib_record_num,
     item.location_code,
     item.item_format,
     item.item_callnumber,
     item.barcode,
     item.item_status_code,
     item.checkout_total
   from
     item
   where
     item.location_code = '1cjbd'
   order by
     item.location_code,
     item.item_format,
     item.item_callnumber
   limit
     10   

... produces the following output:
     
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| item_record_num | bib_record_num | location_code |  item_format  |     item_callnumber    |    barcode    | item_status_code | checkout_total |
+=================+================+===============+===============+========================+===============+==================+================+
| 10888518        | 3550528        | 1cjbd         | Book          | easy                   | A000070519154 | \-               | 0              |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 10965112        | 3233617        | 1cjbd         | Juvenile Book |                        | A000070640273 | \-               | 1              |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 11017035        | 3236372        | 1cjbd         | Juvenile Book |                        | A000069475681 | \-               | 1              |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 10965362        | 2688799        | 1cjbd         | Juvenile Book |                        | A000069006551 | m                | 1              |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 9447427         | 3286714        | 1cjbd         | Juvenile Book | 204.32 v573      2017  | A000055734628 | \-               | 5              |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 2246684         | 1692412        | 1cjbd         | Juvenile Book | 591.981102 qd221       | 0987553048016 | \-               | 25             |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 11055933        | 3578761        | 1cjbd         | Juvenile Book | 973.099 g795      2021 | A000065991095 | \-               | 1              |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 8684222         | 3116516        | 1cjbd         | Juvenile Book | easy                   | A000049629173 | \!               | 17             |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 8110672         | 3015738        | 1cjbd         | Juvenile Book | easy                   | A000043824309 | \!               | 17             |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+
| 7037916         | 2828323        | 1cjbd         | Juvenile Book | easy                   | A000037885829 | \!               | 15             |
+-----------------+----------------+---------------+---------------+------------------------+---------------+------------------+----------------+

If we wanted to include the bibliographic record data along with the item data, we would perform a ``JOIN`` on the ``bib`` table

.. code-block:: sql

   select
     item.item_record_num,
     item.bib_record_num,
     item.location_code,
     item.item_format,
     item.item_callnumber,
     bib.best_author,
     bib.best_title,
     item.barcode,
     item.item_status_code,
     item.checkout_total
   from
     item
     join bib on bib.bib_record_num = item.bib_record_num
   where
     item.location_code = '1cjbd'
   order by
     item.location_code,
     item.item_format,
     bib.best_author,
     bib.best_title,
     item.item_callnumber
   limit
     10

... produces the following output:

+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| item_record_num | bib_record_num | location_code |  item_format  | item_callnumber |           best_author           |                                                      best_title                                                      |    barcode    | item_status_code | checkout_total |
+=================+================+===============+===============+=================+=================================+======================================================================================================================+===============+==================+================+
| 10888518        | 3550528        | 1cjbd         | Book          | easy            | Sill, Cathryn P., 1953- author. | Curious about mammals                                                                                                | A000070519154 | \-               | 0              |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 5197805         | 2778660        | 1cjbd         | Juvenile Book | easy            |                                 | 1, 2, 3, sí! : a numbers book in English and Spanish / [design by Madeleine Budnick ; photography by Peggy Tenison]. | A000029565165 | n                | 19             |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 8956516         | 3171999        | 1cjbd         | Juvenile Book | easy            |                                 | 123 Blaze!                                                                                                           | A000052530748 | \-               | 7              |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 5473860         | 2764313        | 1cjbd         | Juvenile Book | easy            |                                 | 5 busy ducklings.                                                                                                    | 1825831-1001  | w                | 26             |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 6787418         | 2793571        | 1cjbd         | Juvenile Book | easy            |                                 | A day at the zoo.                                                                                                    | A000037147154 | n                | 5              |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 10214507        | 3407900        | 1cjbd         | Juvenile Book | easy            |                                 | A little book about ABCs                                                                                             | A000062920188 | n                | 5              |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 7337421         | 2841761        | 1cjbd         | Juvenile Book | easy            |                                 | ABC 123.                                                                                                             | A000037726080 | e                | 4              |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 10125351        | 3393624        | 1cjbd         | Juvenile Book | easy chagollan  |                                 | ABC animals                                                                                                          | A000064045935 | \-               | 14             |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 9688691         | 3316941        | 1cjbd         | Juvenile Book | easy            |                                 | ABC color                                                                                                            | A000058339714 | \-               | 8              |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+
| 10270587        | 3421412        | 1cjbd         | Juvenile Book | easy            |                                 | ABC what can she be? : girls can be anything they want to be, from A to Z                                            | A000064370325 | \-               | 11             |
+-----------------+----------------+---------------+---------------+-----------------+---------------------------------+----------------------------------------------------------------------------------------------------------------------+---------------+------------------+----------------+


Full Text Search
----------------

It's possible to use a feature called "Full Text Search" or "FTS" with the bib data. Below is an example:

.. code-block:: sql

   with fts_search as (
     select
       rowid,
       rank
     from
       bib_fts
     where
       bib_fts match :search
   )
   select
     (
       select
         sum(checkout_total)
       from
         item
       where
         item.bib_record_num = bib.bib_record_num
     ) as checkouts_total,
     bib_record_num,
     'https://cincinnatilibrary.bibliocommons.com/item/show/' || bib_record_num || '170' as catalog_link,
     creation_date,
     record_last_updated,
     isbn,
     best_author,
     best_title,
     publisher,
     publish_year,
     bib_level_callnumber,
     indexed_subjects
   from
     fts_search
     join bib on bib.rowid = fts_search.rowid
   order by
     rank

Using FTS values, ``"black lives matter" NOT ("fiction" OR "fictitious")``, for example, you can build useful searches across the bib (title) text data and extract extra item information as well. Below is the link for this particular search.

`"current-collection" FTS example <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection-87a9011?sql=with+fts_search+as+%28%0D%0A++select%0D%0A++++rowid%2C%0D%0A++++rank%0D%0A++from%0D%0A++++bib_fts%0D%0A++where%0D%0A++++bib_fts+match+%3Asearch%0D%0A%29%0D%0Aselect%0D%0A++%28%0D%0A++++select%0D%0A++++++sum%28checkout_total%29%0D%0A++++from%0D%0A++++++item%0D%0A++++where%0D%0A++++++item.bib_record_num+%3D+bib.bib_record_num%0D%0A++%29+as+checkouts_total%2C%0D%0A++bib_record_num%2C%0D%0A++%27https%3A%2F%2Fcincinnatilibrary.bibliocommons.com%2Fitem%2Fshow%2F%27+%7C%7C+bib_record_num+%7C%7C+%27170%27+as+catalog_link%2C%0D%0A++creation_date%2C%0D%0A++record_last_updated%2C%0D%0A++isbn%2C%0D%0A++best_author%2C%0D%0A++best_title%2C%0D%0A++publisher%2C%0D%0A++publish_year%2C%0D%0A++bib_level_callnumber%2C%0D%0A++indexed_subjects%0D%0Afrom%0D%0A++fts_search%0D%0A++join+bib+on+bib.rowid+%3D+fts_search.rowid%0D%0Aorder+by%0D%0A++rank&search=%22black+lives+matter%22+NOT+%28%22fiction%22+OR+%22fictitious%22%29>`_ 

More details on syntax of the sqlite FTS feature can be found here `<https://www.sqlite.org/fts5.html#full_text_query_syntax>`_

Limit to "active" Items
-----------------------------------

In certain circumstances, you may want to limit a search to "active" items only.
This could be useful in aggregating, and including only the items that the
system considers "active".

For example, these codes (defined in the ``item_status_property_myuser`` table) could be used when targeting "active" items:
``item.item_status_code IN ('-', '!', 'b', 'p', '(', '@', ')', '_', '=', '+', 't')``

+------+---------------+------------------------+
| code | display_order | name                   |
+======+===============+========================+
| \!   | 0             | ON HOLDSHELF           |
+------+---------------+------------------------+
| \(   | 5             | SearchOH OL PAGED      |
+------+---------------+------------------------+
| \)   | 6             | SearchOH OL CANCEL'D   |
+------+---------------+------------------------+
| \+   | 7             | RENEWAL PENDING        |
+------+---------------+------------------------+
| \-   | 8             | CHECK SHELVES          |
+------+---------------+------------------------+
| \=   | 9             | RENEWAL DENIED         |
+------+---------------+------------------------+
| \@   | 10            | SearchOH/OL OFFSITE    |
+------+---------------+------------------------+
| \_   | 11            | SearchOH/OL RE-REQUEST |
+------+---------------+------------------------+
| b    | 12            | AT BINDERY             |
+------+---------------+------------------------+
| p    | 22            | IN PROCESSING          |
+------+---------------+------------------------+
| t    | 25            | IN TRANSIT             |
+------+---------------+------------------------+

To use these codes in an example query:

.. code-block:: sql

   select
     i.item_record_num,
     i.bib_record_num,
     i.barcode,
     i.location_code,
     i.item_status_code
   from
     item as i
   where
     i.item_status_code IN ('-', '!', 'b', 'p', '(', '@', ')', '_', '=', '+', 't')
   order by
     random()
   limit
     10



+-----------------+----------------+---------------+---------------+------------------+
| item_record_num | bib_record_num |    barcode    | location_code | item_status_code |
+=================+================+===============+===============+==================+
| 8165911         | 3026290        | A000046716239 | osjsa         | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 4126169         | 2061516        | 1047094907011 | bajer         | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 7192197         | 2873481        | A000029471398 | majf          | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 5112294         | 2591286        | A000019684414 | 3ra           | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 2576020         | 1795932        | 1028118751015 | 1fa           | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 4461372         | 2606093        | 1607071-1004  | osjf          | t                |
+-----------------+----------------+---------------+---------------+------------------+
| 9918665         | 3246960        | A000061088904 | 1cjho         | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 6559267         | 2733695        | A000032378945 | cvadt         | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 2120915         | 1357195        | 0946007541018 | osjnf         | \-               |
+-----------------+----------------+---------------+---------------+------------------+
| 3488849         | 1197610        | 0941601451029 | 1fa           | \-               |
+-----------------+----------------+---------------+---------------+------------------+

Aggregate Counts
----------------

This basic example gives an overall count of the numbers of items included in the snapshots.

.. code-block:: sql

   select
      count(distinct b.bib_record_num)
   from
      bib as b
      join item as i on i.bib_record_num = b.bib_record_num