Static SQL Queries
==================

The following queries are useful for reporting purposes

.. contents::

Bib Records Deleted Within the Last Week
----------------------------------------
`click to run Bib Records Deleted Within the Last Week query <https://ilsweb.cincinnatilibrary.org/collection-analysis/_memory-000?sql=--+This+is+a+list+of+metadata+from+bib+records+that+have+been+deleted+in+the+previouse+week%0D%0A--+NOTE%3A+page+numbers+start+at+0%2C+and+will+produce+a+max+of+3000+records+until+no+more+remain+to+populate+a+%22page%22%0D%0Awith+deleted_bibs+as+%28%0D%0A++select%0D%0A++++bp.bib_record_num%0D%0A++from%0D%0A++++collection_prev.bib+as+bp%0D%0A++++left+outer+join+current_collection.bib+as+bc+on+bc.bib_record_num+%3D+bp.bib_record_num%0D%0A++where%0D%0A++++bc.bib_record_num+is+null%0D%0A++order+by%0D%0A++++bp.bib_level_callnumber%2C%0D%0A++++bp.best_author%2C%0D%0A++++bp.best_title%2C%0D%0A++++bp.bib_record_num%0D%0A%29%0D%0Aselect%0D%0A++db.bib_record_num%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++deletion_date_gmt%0D%0A++++from%0D%0A++++++collection_prev.record_metadata+as+p%0D%0A++++where%0D%0A++++++p.record_num+%3D+db.bib_record_num%0D%0A++++++and+p.record_type_code+%3D+%27b%27%0D%0A++++limit%0D%0A++++++1%0D%0A++%29+as+deletion_date%2C%0D%0A++b.%2A%0D%0Afrom%0D%0A++deleted_bibs+as+db%0D%0A++join+collection_prev.bib+as+b+on+b.bib_record_num+%3D+db.bib_record_num%0D%0Alimit%0D%0A++3000+offset+%3Apage+%2A+3000&page=0&_hide_sql=1>`_

.. code-block:: sql

    -- This is a list of metadata from bib records that have been deleted in the previous week
    -- NOTE: page numbers start at 0, and will produce a max of 3000 records until no more remain to populate a "page"
    with deleted_bibs as (
    select
        bp.bib_record_num
    from
        collection_prev.bib as bp
        left outer join current_collection.bib as bc on bc.bib_record_num = bp.bib_record_num
    where
        bc.bib_record_num is null
    order by
        bp.bib_level_callnumber,
        bp.best_author,
        bp.best_title,
        bp.bib_record_num
    )
    select
    db.bib_record_num,
    (
        select
        deletion_date_gmt
        from
        collection_prev.record_metadata as p
        where
        p.record_num = db.bib_record_num
        and p.record_type_code = 'b'
        limit
        1
    ) as deletion_date,
    b.*
    from
    deleted_bibs as db
    join collection_prev.bib as b on b.bib_record_num = db.bib_record_num
    limit
    3000 offset :page * 3000

Item Records Deleted Within the Last Week
-----------------------------------------
`click to run Item Records Deleted Within the Last Week query <https://ilsweb.cincinnatilibrary.org/collection-analysis/_memory?sql=--+This+is+a+list+of+metadata+from+bib+records+that+have+been+deleted+in+the+previouse+week%0D%0A--+NOTE%3A+page+numbers+start+at+0%2C+and+will+produce+a+max+of+3000+records+until+no+more+remain+to+populate+a+%22page%22%0D%0Awith+deleted_items+as+%28%0D%0A++select%0D%0A++++ip.item_record_num%2C%0D%0A++++ip.bib_record_num%2C%0D%0A++++ip.location_code%2C%0D%0A++++ip.item_callnumber%2C%0D%0A++++ip.item_format%2C%0D%0A++++ip.last_checkout_date%2C%0D%0A++++ip.checkout_total%2C%0D%0A++++ip.item_status_code%0D%0A++from%0D%0A++++collection_prev.item+as+ip%0D%0A++++left+outer+join+current_collection.item+as+ic+on+ic.item_record_num+%3D+ip.item_record_num%0D%0A++where%0D%0A++++ic.item_record_num+is+null%0D%0A%29%0D%0Aselect%0D%0A++di.%2A%2C%0D%0A++b.best_author%2C%0D%0A++b.best_title%2C%0D%0A++b.publish_year%2C%0D%0A++b.bib_level_callnumber%0D%0Afrom%0D%0A++deleted_items+as+di%0D%0A++left+outer+join+collection_prev.bib+as+b+on+b.bib_record_num+%3D+di.bib_record_num%0D%0Aorder+by%0D%0A++di.location_code%0D%0Alimit%0D%0A++3000+offset+%3Apage+%2A+3000&page=0&_hide_sql=1>`_

.. code-block:: sql

    -- This is a list of metadata from item records that have been deleted in the previouse week
    -- NOTE: page numbers start at 0, and will produce a max of 3000 records until no more remain to populate a "page"
    with deleted_items as (
    select
        ip.item_record_num,
        ip.bib_record_num,
        ip.location_code,
        ip.item_callnumber,
        ip.item_format,
        ip.last_checkout_date,
        ip.checkout_total,
        ip.item_status_code
    from
        collection_prev.item as ip
        left outer join current_collection.item as ic on ic.item_record_num = ip.item_record_num
    where
        ic.item_record_num is null
    )
    select
    di.*,
    b.best_author,
    b.best_title,
    b.publish_year,
    b.bib_level_callnumber
    from
    deleted_items as di
    left outer join collection_prev.bib as b on b.bib_record_num = di.bib_record_num
    order by
    di.location_code
    limit
    3000 offset :page * 3000