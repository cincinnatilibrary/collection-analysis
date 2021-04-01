Static SQL Queries & Reports
============================

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

Collection Value
----------------

`click to run Collection Value query on current_collection database <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=with+branch_locations+as+(%0D%0A++select%0D%0A++++n.name%2C%0D%0A++++b.code_num%2C%0D%0A++++l.*%0D%0A++from%0D%0A++++branch_name+as+n%0D%0A++++join+branch+as+b+on+b.id+%3D+n.branch_id%0D%0A++++join+location+as+l+on+l.branch_code_num+%3D+b.code_num%0D%0A)%0D%0Aselect%0D%0A++l.name+as+branch_name%2C%0D%0A++item_format%2C%0D%0A++sum(price_cents)+%2F+100.0+as+total_value%0D%0Afrom%0D%0A++branch_locations+as+l%0D%0A++%0D%0A++join%0D%0A++item+as+i+on+i.location_code+%3D+l.code%0D%0A++%0D%0Agroup+by+%0D%0Al.name%2C%0D%0Ai.item_format&_hide_sql=1>`_

`click to run Collection Value query on collection-2021-01-04 database <https://ilsweb.cincinnatilibrary.org/collection-analysis/collection-2021-01-04?sql=with+branch_locations+as+%28%0D%0A++select%0D%0A++++n.name%2C%0D%0A++++b.code_num%2C%0D%0A++++l.%2A%0D%0A++from%0D%0A++++branch_name+as+n%0D%0A++++join+branch+as+b+on+b.id+%3D+n.branch_id%0D%0A++++join+location+as+l+on+l.branch_code_num+%3D+b.code_num%0D%0A%29%0D%0Aselect%0D%0A++l.name+as+branch_name%2C%0D%0A++item_format%2C%0D%0A++sum%28price_cents%29+%2F+100.0+as+total_value%0D%0Afrom%0D%0A++branch_locations+as+l%0D%0A++%0D%0A++join%0D%0A++item+as+i+on+i.location_code+%3D+l.code%0D%0A++%0D%0Agroup+by+%0D%0Al.name%2C%0D%0Ai.item_format&_hide_sql=1>`_

`click to run Collection Value query on collection-2020-01-06 database <https://ilsweb.cincinnatilibrary.org/collection-analysis/collection-2020-01-06-50dd950?sql=with+branch_locations+as+%28%0D%0A++select%0D%0A++++n.name%2C%0D%0A++++b.code_num%2C%0D%0A++++l.*%0D%0A++from%0D%0A++++branch_name+as+n%0D%0A++++join+branch+as+b+on+b.id+%3D+n.branch_id%0D%0A++++join+location+as+l+on+l.branch_code_num+%3D+b.code_num%0D%0A%29%0D%0Aselect%0D%0A++l.name+as+branch_name%2C%0D%0A++item_format%2C%0D%0A++sum%28price_cents%29+%2F+100.0+as+total_value%0D%0Afrom%0D%0A++branch_locations+as+l%0D%0A++join+item+as+i+on+i.location_code+%3D+l.code%0D%0Agroup+by%0D%0A++l.name%2C%0D%0A++i.item_format&_hide_sql=1>`_

.. code-block:: sql

   with branch_locations as (
   select
       n.name,
       b.code_num,
       l.*
   from
       branch_name as n
       join branch as b on b.id = n.branch_id
       join location as l on l.branch_code_num = b.code_num
   )
   select
   l.name as branch_name,
   item_format,
   sum(price_cents) / 100.0 as total_value
   from
   branch_locations as l
   
   join
   item as i on i.location_code = l.code
   
   group by 
   l.name,
   i.item_format


Available Items & Circulation Information By Location at Branch 
-----------------------------------------------------------------------------------

For item status ``-``, aggregate count of total items, items with 0 checkouts, items with 1 or more checkouts, and items checked out at the time of the snapshot.

Note: This query accepts the query parameter, ``branch_code_num``. These codes for CHPL Branch locations can be found from the following query: `branch names and code numbers <`https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=select+br.code_num%2C+bn.name%0Afrom+branch+as+br+join+branch_name+as+bn+on+bn.branch_id+%3D+br.id>`_

`click to run query on current_collection database <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=select%0D%0A++i.location_code%2C%0D%0A++ln.name%2C%0D%0A++--+loc.branch_code_num%2C%0D%0A++--+bn.name+as+branch_name%2C%0D%0A++count%28%2A%29+as+count_total_available_items%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item+as+i2%0D%0A++++where%0D%0A++++++i2.location_code+%3D+i.location_code%0D%0A++++++and+i2.item_status_code+%3D+%27-%27%0D%0A++++++and+i2.checkout_total+%3D+0%0D%0A++%29+as+count_items_0_checkouts%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item+as+i2%0D%0A++++where%0D%0A++++++i2.location_code+%3D+i.location_code%0D%0A++++++and+i2.item_status_code+%3D+%27-%27%0D%0A++++++and+i2.checkout_total+%3E+0%0D%0A++%29+as+count_items_gt_0_checkouts%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item+as+i2%0D%0A++++where%0D%0A++++++i2.location_code+%3D+i.location_code%0D%0A++++++and+i2.item_status_code+%3D+%27-%27%0D%0A++++++and+i2.checkout_date+is+not+null%0D%0A++%29+as+count_curr_checked_out%0D%0Afrom%0D%0A++item+as+i%0D%0A++left+outer+join+location+as+loc+on+loc.code+%3D+i.location_code%0D%0A++left+outer+join+location_name+as+ln+on+ln.location_id+%3D+loc.id%0D%0A++left+outer+join+branch+as+br+on+br.code_num+%3D+loc.branch_code_num%0D%0A++left+outer+join+branch_name+as+bn+on+bn.branch_id+%3D+br.id%0D%0Awhere%0D%0A++i.item_status_code+%3D+%27-%27%0D%0A++and+br.code_num+%3D+%3Abranch_code_num%0D%0Agroup+by%0D%0A++i.location_code%2C%0D%0A++ln.name+--+loc.branch_code_num%2C%0D%0A++--+branch_name%0D%0Aorder+by%0D%0A++loc.branch_code_num&branch_code_num=1&_hide_sql=1>`_

.. code-block:: sql

   select
     i.location_code,
     ln.name,
     -- loc.branch_code_num,
     -- bn.name as branch_name,
     count(*) as count_total_available_items,
     (
       select
         count(*)
       from
         item as i2
       where
         i2.location_code = i.location_code
         and i2.item_status_code = '-'
         and i2.checkout_total = 0
     ) as count_items_0_checkouts,
     (
       select
         count(*)
       from
         item as i2
       where
         i2.location_code = i.location_code
         and i2.item_status_code = '-'
         and i2.checkout_total > 0
     ) as count_items_gt_0_checkouts,
     (
       select
         count(*)
       from
         item as i2
       where
         i2.location_code = i.location_code
         and i2.item_status_code = '-'
         and i2.checkout_date is not null
     ) as count_curr_checked_out
   from
     item as i
     left outer join location as loc on loc.code = i.location_code
     left outer join location_name as ln on ln.location_id = loc.id
     left outer join branch as br on br.code_num = loc.branch_code_num
     left outer join branch_name as bn on bn.branch_id = br.id
   where
     i.item_status_code = '-'
     and br.code_num = :branch_code_num
   group by
     i.location_code,
     ln.name
   order by
     loc.branch_code_num