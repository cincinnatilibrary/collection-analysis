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
`click to run Item Records Deleted Within the Last Week query <https://ilsweb.cincinnatilibrary.org/collection-analysis/_memory?sql=--+This+is+a+list+of+metadata+from+bib+records+that+have+been+deleted+in+the+previouse+week%0D%0A--+NOTE%3A+page+numbers+start+at+0%2C+and+will+produce+a+max+of+3000+records+until+no+more+remain+to+populate+a+%22page%22%0D%0Awith+deleted_items+as+%28%0D%0A++select%0D%0A++++ip.item_record_num%2C%0D%0A++++ip.bib_record_num%2C%0D%0A++++ip.location_code%2C%0D%0A++++ip.item_callnumber%2C%0D%0A++++ip.item_format%2C%0D%0A++++ip.last_checkout_date%2C%0D%0A++++ip.checkout_total%2C%0D%0A++++ip.item_status_code%0D%0A++from%0D%0A++++collection_prev.item+as+ip%0D%0A++++left+outer+join+current_collection.item+as+ic+on+ic.item_record_num+%3D+ip.item_record_num%0D%0A++where%0D%0A++++ic.item_record_num+is+null%0D%0A%29%0D%0Aselect%0D%0A++di.%2A%2C%0D%0A++b.best_author%2C%0D%0A++b.best_title%2C%0D%0A++b.publish_year%2C%0D%0A++b.bib_level_callnumber%0D%0Afrom%0D%0A++deleted_items+as+di%0D%0A++left+outer+join+collection_prev.bib+as+b+on+b.bib_record_num+%3D+di.bib_record_num%0D%0Aorder+by%0D%0A++di.location_code%0D%0Alimit%0D%0A++3000+offset+%3Apage+%2A+3000&page=0&_hide_sql=1>`__

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

Note: This query accepts the query parameter, ``branch_code_num``. These codes for CHPL Branch locations can be found from the following query: `branch names and code numbers <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=select+br.code_num%2C+bn.name%0Afrom+branch+as+br+join+branch_name+as+bn+on+bn.branch_id+%3D+br.id>`_

`click to run query on current_collection database <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=select%0D%0A++i.location_code%2C%0D%0A++ln.name%2C%0D%0A++--+loc.branch_code_num%2C%0D%0A++--+bn.name+as+branch_name%2C%0D%0A++count%28%2A%29+as+count_total_available_items%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item+as+i2%0D%0A++++where%0D%0A++++++i2.location_code+%3D+i.location_code%0D%0A++++++and+i2.item_status_code+%3D+%27-%27%0D%0A++++++and+i2.checkout_total+%3D+0%0D%0A++%29+as+count_items_0_checkouts%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item+as+i2%0D%0A++++where%0D%0A++++++i2.location_code+%3D+i.location_code%0D%0A++++++and+i2.item_status_code+%3D+%27-%27%0D%0A++++++and+i2.checkout_total+%3E+0%0D%0A++%29+as+count_items_gt_0_checkouts%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item+as+i2%0D%0A++++where%0D%0A++++++i2.location_code+%3D+i.location_code%0D%0A++++++and+i2.item_status_code+%3D+%27-%27%0D%0A++++++and+i2.checkout_date+is+not+null%0D%0A++%29+as+count_curr_checked_out%0D%0Afrom%0D%0A++item+as+i%0D%0A++left+outer+join+location+as+loc+on+loc.code+%3D+i.location_code%0D%0A++left+outer+join+location_name+as+ln+on+ln.location_id+%3D+loc.id%0D%0A++left+outer+join+branch+as+br+on+br.code_num+%3D+loc.branch_code_num%0D%0A++left+outer+join+branch_name+as+bn+on+bn.branch_id+%3D+br.id%0D%0Awhere%0D%0A++i.item_status_code+%3D+%27-%27%0D%0A++and+br.code_num+%3D+%3Abranch_code_num%0D%0Agroup+by%0D%0A++i.location_code%2C%0D%0A++ln.name+--+loc.branch_code_num%2C%0D%0A++--+branch_name%0D%0Aorder+by%0D%0A++loc.branch_code_num&branch_code_num=1&_hide_sql=1>`__

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



Lucky Day Leased Books and Leased DVDs Analysis
-----------------------------------------------

`click to run query on current_collection database <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=--+find+lucky+day+leased+books+and+leased+dvds%2C+and+provide+some+basic+statistics+around+those+items+grouped+by+title%0D%0Awith+ld_item_info+as+%28%0D%0A++select%0D%0A++++item.bib_record_num%2C%0D%0A++++price_cents%2C%0D%0A++++item.checkout_total%2C%0D%0A++++--+lucky+day+items+are+not+renewable%0D%0A++++--+item.renewal_total%2C%0D%0A++++item.item_status_code%2C%0D%0A++++item.creation_date%2C%0D%0A++++item.barcode%2C%0D%0A++++item.item_format%0D%0A++from%0D%0A++++item%0D%0A++where%0D%0A++++item.item_format+in+%28%27Leased+Book%27%2C+%27Leased+DVD%27%29%0D%0A++++and+lower%28item.barcode%29+LIKE+%22l%25%22%0D%0A%29%0D%0Aselect%0D%0A++bib.best_title%2C%0D%0A++bib.bib_record_num%2C%0D%0A++bib.creation_date+as+bib_creation_date%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++COUNT%28%2A%29%0D%0A++++from%0D%0A++++++item%0D%0A++++where%0D%0A++++++item.bib_record_num+%3D+bib.bib_record_num%0D%0A++++++and+item.item_format+not+in+%28%27Leased+Book%27%2C+%27Leased+DVD%27%29%0D%0A++++limit%0D%0A++++++1%0D%0A++%29+as+count_non_ld_items%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++sum%28checkout_total%29%0D%0A++++from%0D%0A++++++item%0D%0A++++where%0D%0A++++++item.bib_record_num+%3D+bib.bib_record_num%0D%0A++++++and+item.item_format+not+in+%28%27Leased+Book%27%2C+%27Leased+DVD%27%29%0D%0A++++limit%0D%0A++++++1%0D%0A++%29+as+total_non_ld_items_checkouts%2C%0D%0A++ld.item_format+as+ld_item_format%2C%0D%0A++round%28%0D%0A++++avg%28%0D%0A++++++%28julianday%28%27now%27%29+-+julianday%28ld.creation_date%29%29%0D%0A++++%29%2C%0D%0A++++1%0D%0A++%29+as+avg_ld_item_age_days%2C%0D%0A++count%28%2A%29+as+count_ld_items%2C%0D%0A++sum%28checkout_total%29+as+total_ld_items_checkouts%2C%0D%0A++sum%28price_cents%29+%2F+100.0+as+total_ld_items_price%2C%0D%0A++round%28%0D%0A++++%28sum%28price_cents%29+%2F+100.0%29+%2F+sum%28checkout_total%29%2C%0D%0A++++2%0D%0A++%29+as+cost_per_ld_checkout%0D%0Afrom%0D%0A++ld_item_info+as+ld%0D%0A++join+bib+on+bib.bib_record_num+%3D+ld.bib_record_num%0D%0Agroup+by%0D%0A++bib.best_title%2C%0D%0A++bib.bib_record_num%2C%0D%0A++bib.creation_date%2C%0D%0A++ld.item_format%0D%0Aorder+by%0D%0A++avg_ld_item_age_days&_hide_sql=1>`__

This report will produce a simple analysis of the Lucky Day Items (identified by items with the item format ('Leased Book', 'Leased DVD') and item barcodes starting with the character `l`). The report is Title-based, and compiles the average age in days of linked items, total counts of linked items, total checkouts linked items, and a cost per item checkout (based on the item price).

.. code-block:: sql

   -- find lucky day leased books and leased dvds, and provide some basic statistics around those items grouped by title
   with ld_item_info as (
     select
       item.bib_record_num,
       price_cents,
       item.checkout_total,
       -- lucky day items are not renewable
       -- item.renewal_total,
       item.item_status_code,
       item.creation_date,
       item.barcode,
       item.item_format
     from
       item
     where
       item.item_format in ('Leased Book', 'Leased DVD')
       and lower(item.barcode) LIKE "l%"
   )
   select
     bib.best_title,
     bib.bib_record_num,
     bib.creation_date as bib_creation_date,
     (
       select
         COUNT(*)
       from
         item
       where
         item.bib_record_num = bib.bib_record_num
         and item.item_format not in ('Leased Book', 'Leased DVD')
       limit
         1
     ) as count_non_ld_items,
     (
       select
         sum(checkout_total)
       from
         item
       where
         item.bib_record_num = bib.bib_record_num
         and item.item_format not in ('Leased Book', 'Leased DVD')
       limit
         1
     ) as total_non_ld_items_checkouts,
     ld.item_format as ld_item_format,
     round(
       avg(
         (julianday('now') - julianday(ld.creation_date))
       ),
       1
     ) as avg_ld_item_age_days,
     count(*) as count_ld_items,
     sum(checkout_total) as total_ld_items_checkouts,
     sum(price_cents) / 100.0 as total_ld_items_price,
     round(
       (sum(price_cents) / 100.0) / sum(checkout_total),
       2
     ) as cost_per_ld_checkout
   from
     ld_item_info as ld
     join bib on bib.bib_record_num = ld.bib_record_num
   group by
     bib.best_title,
     bib.bib_record_num,
     bib.creation_date,
     ld.item_format
   order by
     avg_ld_item_age_days


Item Data Consistency Report -- Excluded Titles
-----------------------------------------------

`click to run query on current_collection database <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection-204d100?sql=--+this+query+will+display+some+bib+and+item+information+for+titles+that+are+to+be+excluded+from+the+Item+Data+Consistency+Report%0D%0Aselect%0D%0A++b.bib_record_num%2C%0D%0A++b.best_author%2C%0D%0A++b.best_title%2C%0D%0A++cast%28publish_year+as+integer%29+as+publish_year%2C%0D%0A++b.creation_date%2C%0D%0A++b.record_last_updated%2C%0D%0A++b.isbn%2C%0D%0A++%28%0D%0A++++select%0D%0A++++++count%28%2A%29%0D%0A++++from%0D%0A++++++item%0D%0A++++where%0D%0A++++++item.bib_record_num+%3D+b.bib_record_num%0D%0A++%29+as+total_item_count%2C%0D%0A++%28%0D%0A++++with+locations+as+%28%0D%0A++++++select%0D%0A++++++++DISTINCT+location_code%0D%0A++++++from%0D%0A++++++++item%0D%0A++++++where%0D%0A++++++++item.bib_record_num+%3D+b.bib_record_num%0D%0A++++++order+by%0D%0A++++++++location_code%0D%0A++++%29%0D%0A++++select%0D%0A++++++group_concat+%28location_code%29%0D%0A++++from%0D%0A++++++locations%0D%0A++%29+as+item_locations%0D%0Afrom%0D%0A++bib+as+b%0D%0Awhere%0D%0A++--+these+titles+are+considered+%22teen+classics%22+or+otherwise%2C+and+are+excluded+from+the+IDC+report%0D%0A++bib_record_num+in+%28%0D%0A++++1008088%2C%0D%0A++++1008092%2C%0D%0A++++1008324%2C%0D%0A++++1009074%2C%0D%0A++++1012471%2C%0D%0A++++1012960%2C%0D%0A++++1016931%2C%0D%0A++++1023324%2C%0D%0A++++1025647%2C%0D%0A++++1026944%2C%0D%0A++++1030135%2C%0D%0A++++1032779%2C%0D%0A++++1033764%2C%0D%0A++++1035984%2C%0D%0A++++1036364%2C%0D%0A++++1038132%2C%0D%0A++++1041785%2C%0D%0A++++1042130%2C%0D%0A++++1044943%2C%0D%0A++++1045391%2C%0D%0A++++1057164%2C%0D%0A++++1068843%2C%0D%0A++++1069142%2C%0D%0A++++1080942%2C%0D%0A++++1098072%2C%0D%0A++++1123311%2C%0D%0A++++1125257%2C%0D%0A++++1131252%2C%0D%0A++++1136783%2C%0D%0A++++1137858%2C%0D%0A++++1149649%2C%0D%0A++++1156722%2C%0D%0A++++1163065%2C%0D%0A++++1195037%2C%0D%0A++++1198983%2C%0D%0A++++1208160%2C%0D%0A++++1208782%2C%0D%0A++++1214946%2C%0D%0A++++1258923%2C%0D%0A++++1260206%2C%0D%0A++++1262052%2C%0D%0A++++1262195%2C%0D%0A++++1263884%2C%0D%0A++++1268373%2C%0D%0A++++1268384%2C%0D%0A++++1274970%2C%0D%0A++++1276299%2C%0D%0A++++1283114%2C%0D%0A++++1285037%2C%0D%0A++++1318751%2C%0D%0A++++1321722%2C%0D%0A++++1328024%2C%0D%0A++++1330867%2C%0D%0A++++1332284%2C%0D%0A++++1375132%2C%0D%0A++++1376771%2C%0D%0A++++1386082%2C%0D%0A++++1392809%2C%0D%0A++++1395441%2C%0D%0A++++1405850%2C%0D%0A++++1417890%2C%0D%0A++++1422875%2C%0D%0A++++1427726%2C%0D%0A++++1465219%2C%0D%0A++++1465868%2C%0D%0A++++1473691%2C%0D%0A++++1476334%2C%0D%0A++++1482199%2C%0D%0A++++1500156%2C%0D%0A++++1500725%2C%0D%0A++++1519112%2C%0D%0A++++1519118%2C%0D%0A++++1520620%2C%0D%0A++++1521555%2C%0D%0A++++1523209%2C%0D%0A++++1524032%2C%0D%0A++++1524039%2C%0D%0A++++1524049%2C%0D%0A++++1528683%2C%0D%0A++++1534705%2C%0D%0A++++1542739%2C%0D%0A++++1555182%2C%0D%0A++++1557339%2C%0D%0A++++1557775%2C%0D%0A++++1564639%2C%0D%0A++++1573242%2C%0D%0A++++1579598%2C%0D%0A++++1584994%2C%0D%0A++++1596027%2C%0D%0A++++1610988%2C%0D%0A++++1630040%2C%0D%0A++++1637976%2C%0D%0A++++1639082%2C%0D%0A++++1639351%2C%0D%0A++++1657016%2C%0D%0A++++1657539%2C%0D%0A++++1723544%2C%0D%0A++++1732910%2C%0D%0A++++1748806%2C%0D%0A++++1750917%2C%0D%0A++++1751512%2C%0D%0A++++1753059%2C%0D%0A++++1756363%2C%0D%0A++++1765488%2C%0D%0A++++1777013%2C%0D%0A++++1777554%2C%0D%0A++++1789689%2C%0D%0A++++1798623%2C%0D%0A++++1806397%2C%0D%0A++++1815906%2C%0D%0A++++1821901%2C%0D%0A++++1823479%2C%0D%0A++++1824853%2C%0D%0A++++1824863%2C%0D%0A++++1824881%2C%0D%0A++++1837580%2C%0D%0A++++1874105%2C%0D%0A++++1874105%2C%0D%0A++++1874617%2C%0D%0A++++1881635%2C%0D%0A++++1891612%2C%0D%0A++++1893725%2C%0D%0A++++1900878%2C%0D%0A++++1915536%2C%0D%0A++++1933582%2C%0D%0A++++1934753%2C%0D%0A++++1960352%2C%0D%0A++++1961576%2C%0D%0A++++1961887%2C%0D%0A++++1967302%2C%0D%0A++++1986993%2C%0D%0A++++1992305%2C%0D%0A++++1996454%2C%0D%0A++++2005510%2C%0D%0A++++2006956%2C%0D%0A++++2006985%2C%0D%0A++++2008273%2C%0D%0A++++2012712%2C%0D%0A++++2014369%2C%0D%0A++++2028943%2C%0D%0A++++2040871%2C%0D%0A++++2048799%2C%0D%0A++++2052473%2C%0D%0A++++2069758%2C%0D%0A++++2070459%2C%0D%0A++++2080910%2C%0D%0A++++2081561%2C%0D%0A++++2086313%2C%0D%0A++++2089850%2C%0D%0A++++2092147%2C%0D%0A++++2092155%2C%0D%0A++++2111249%2C%0D%0A++++2118284%2C%0D%0A++++2130304%2C%0D%0A++++2133134%2C%0D%0A++++2137975%2C%0D%0A++++2169420%2C%0D%0A++++2171086%2C%0D%0A++++2186599%2C%0D%0A++++2203330%2C%0D%0A++++2203330%2C%0D%0A++++2203367%2C%0D%0A++++2204141%2C%0D%0A++++2210745%2C%0D%0A++++2212066%2C%0D%0A++++2215585%2C%0D%0A++++2220611%2C%0D%0A++++2225085%2C%0D%0A++++2228373%2C%0D%0A++++2229190%2C%0D%0A++++2229649%2C%0D%0A++++2247002%2C%0D%0A++++2506864%2C%0D%0A++++2252851%2C%0D%0A++++2264431%2C%0D%0A++++2265447%2C%0D%0A++++2268806%2C%0D%0A++++2270361%2C%0D%0A++++2315417%2C%0D%0A++++2325236%2C%0D%0A++++2330280%2C%0D%0A++++2331675%2C%0D%0A++++2349894%2C%0D%0A++++2377225%2C%0D%0A++++2385659%2C%0D%0A++++2388695%2C%0D%0A++++2390408%2C%0D%0A++++2399213%2C%0D%0A++++2401846%2C%0D%0A++++2402050%2C%0D%0A++++2403296%2C%0D%0A++++2424769%2C%0D%0A++++2427365%2C%0D%0A++++2439149%2C%0D%0A++++2449995%2C%0D%0A++++2454966%2C%0D%0A++++2460026%2C%0D%0A++++2467038%2C%0D%0A++++2476394%2C%0D%0A++++2476870%2C%0D%0A++++2487394%2C%0D%0A++++2492541%2C%0D%0A++++2493883%2C%0D%0A++++2494668%2C%0D%0A++++2508710%2C%0D%0A++++2518435%2C%0D%0A++++2526514%2C%0D%0A++++2530079%2C%0D%0A++++2530507%2C%0D%0A++++2532883%2C%0D%0A++++2538123%2C%0D%0A++++2540289%2C%0D%0A++++2540405%2C%0D%0A++++2547935%2C%0D%0A++++2556742%2C%0D%0A++++2560158%2C%0D%0A++++2566314%2C%0D%0A++++2572417%2C%0D%0A++++2574892%2C%0D%0A++++2578161%2C%0D%0A++++2592633%2C%0D%0A++++2598018%2C%0D%0A++++2610287%2C%0D%0A++++2610368%2C%0D%0A++++2611069%2C%0D%0A++++2611525%2C%0D%0A++++2613714%2C%0D%0A++++2615465%2C%0D%0A++++2615487%2C%0D%0A++++2615515%2C%0D%0A++++2615605%2C%0D%0A++++2615620%2C%0D%0A++++2615705%2C%0D%0A++++2615908%2C%0D%0A++++2619886%2C%0D%0A++++2624870%2C%0D%0A++++2628120%2C%0D%0A++++2628125%2C%0D%0A++++2638970%2C%0D%0A++++2640657%2C%0D%0A++++2643029%2C%0D%0A++++2654111%2C%0D%0A++++2659891%2C%0D%0A++++2663126%2C%0D%0A++++2667577%2C%0D%0A++++2670636%2C%0D%0A++++2670823%2C%0D%0A++++2676813%2C%0D%0A++++2693063%2C%0D%0A++++2697347%2C%0D%0A++++2702313%2C%0D%0A++++2712108%2C%0D%0A++++2712532%2C%0D%0A++++2712549%2C%0D%0A++++2712608%2C%0D%0A++++2713686%2C%0D%0A++++2713850%2C%0D%0A++++2726440%2C%0D%0A++++2729046%2C%0D%0A++++2738268%2C%0D%0A++++2739884%2C%0D%0A++++2741117%2C%0D%0A++++2772166%2C%0D%0A++++2784353%2C%0D%0A++++2784616%2C%0D%0A++++2785618%2C%0D%0A++++2788500%2C%0D%0A++++2792223%2C%0D%0A++++2792790%2C%0D%0A++++2823065%2C%0D%0A++++2883551%2C%0D%0A++++2886553%2C%0D%0A++++2963099%2C%0D%0A++++2969363%2C%0D%0A++++2972940%2C%0D%0A++++2994736%2C%0D%0A++++3134360%2C%0D%0A++++3192709%2C%0D%0A++++3193734%2C%0D%0A++++3202674%2C%0D%0A++++3285022%2C%0D%0A++++3293824%2C%0D%0A++++1416907%2C%0D%0A++++2493664%2C%0D%0A++++2985934%2C%0D%0A++++2985935%2C%0D%0A++++2493587%2C%0D%0A++++1803522%2C%0D%0A++++2755125%2C%0D%0A++++2714814%2C%0D%0A++++2500300%2C%0D%0A++++2985933%2C%0D%0A++++3108309%2C%0D%0A++++3108308%2C%0D%0A++++2884705%2C%0D%0A++++2275400%2C%0D%0A++++3229667%2C%0D%0A++++1803502%2C%0D%0A++++1803512%2C%0D%0A++++2275489%2C%0D%0A++++2985932%2C%0D%0A++++2981982%2C%0D%0A++++1832463%2C%0D%0A++++1971745%2C%0D%0A++++1770999%2C%0D%0A++++2318436%2C%0D%0A++++2096954%2C%0D%0A++++3181534%2C%0D%0A++++3181535%2C%0D%0A++++3181536%2C%0D%0A++++3245632%2C%0D%0A++++2970259%2C%0D%0A++++3204670%2C%0D%0A++++3509035%2C%0D%0A++++3208365%2C%0D%0A++++2662378%2C%0D%0A++++3383599%2C%0D%0A++++3371597%2C%0D%0A++++3383599%2C%0D%0A++++2247002%2C%0D%0A++++3371597%2C%0D%0A++++2506864%2C%0D%0A++++1906584%2C%0D%0A++++2750249%2C%0D%0A++++2410509%2C%0D%0A++++742749%2C%0D%0A++++3059271%2C%0D%0A++++2508695%2C%0D%0A++++3352422%2C%0D%0A++++3150089%2C%0D%0A++++2555245%2C%0D%0A++++3208436%2C%0D%0A++++2884408%2C%0D%0A++++2786980%2C%0D%0A++++2544222%2C%0D%0A++++2686721%2C%0D%0A++++3287286%2C%0D%0A++++2987092%2C%0D%0A++++3238720%2C%0D%0A++++3393392%2C%0D%0A++++3466158%2C%0D%0A++++2599355%2C%0D%0A++++1579122%2C%0D%0A++++2771545%0D%0A++%29%0D%0Aorder+by%0D%0A++creation_date&_hide_sql=1>`_

.. code-block:: sql

   -- this query will display some bib and item information for titles that are to be excluded from the Item Data Consistency Report
   select
     b.bib_record_num,
     b.best_author,
     b.best_title,
     cast(publish_year as integer) as publish_year,
     b.creation_date,
     b.record_last_updated,
     b.isbn,
     (
       select
         count(*)
       from
         item
       where
         item.bib_record_num = b.bib_record_num
     ) as total_item_count,
     (
       with locations as (
         select
           DISTINCT location_code
         from
           item
         where
           item.bib_record_num = b.bib_record_num
         order by
           location_code
       )
       select
         group_concat (location_code)
       from
         locations
     ) as item_locations
   from
     bib as b
   where
     -- these titles are considered "teen classics" or otherwise, and are excluded from the IDC report
     bib_record_num in (
       1008088,
       1008092,
       1008324,
       1009074,
       1012471,
       1012960,
       1016931,
       1023324,
       1025647,
       1026944,
       1030135,
       1032779,
       1033764,
       1035984,
       1036364,
       1038132,
       1041785,
       1042130,
       1044943,
       1045391,
       1057164,
       1068843,
       1069142,
       1080942,
       1098072,
       1123311,
       1125257,
       1131252,
       1136783,
       1137858,
       1149649,
       1156722,
       1163065,
       1195037,
       1198983,
       1208160,
       1208782,
       1214946,
       1258923,
       1260206,
       1262052,
       1262195,
       1263884,
       1268373,
       1268384,
       1274970,
       1276299,
       1283114,
       1285037,
       1318751,
       1321722,
       1328024,
       1330867,
       1332284,
       1375132,
       1376771,
       1386082,
       1392809,
       1395441,
       1405850,
       1417890,
       1422875,
       1427726,
       1465219,
       1465868,
       1473691,
       1476334,
       1482199,
       1500156,
       1500725,
       1519112,
       1519118,
       1520620,
       1521555,
       1523209,
       1524032,
       1524039,
       1524049,
       1528683,
       1534705,
       1542739,
       1555182,
       1557339,
       1557775,
       1564639,
       1573242,
       1579598,
       1584994,
       1596027,
       1610988,
       1630040,
       1637976,
       1639082,
       1639351,
       1657016,
       1657539,
       1723544,
       1732910,
       1748806,
       1750917,
       1751512,
       1753059,
       1756363,
       1765488,
       1777013,
       1777554,
       1789689,
       1798623,
       1806397,
       1815906,
       1821901,
       1823479,
       1824853,
       1824863,
       1824881,
       1837580,
       1874105,
       1874105,
       1874617,
       1881635,
       1891612,
       1893725,
       1900878,
       1915536,
       1933582,
       1934753,
       1960352,
       1961576,
       1961887,
       1967302,
       1986993,
       1992305,
       1996454,
       2005510,
       2006956,
       2006985,
       2008273,
       2012712,
       2014369,
       2028943,
       2040871,
       2048799,
       2052473,
       2069758,
       2070459,
       2080910,
       2081561,
       2086313,
       2089850,
       2092147,
       2092155,
       2111249,
       2118284,
       2130304,
       2133134,
       2137975,
       2169420,
       2171086,
       2186599,
       2203330,
       2203330,
       2203367,
       2204141,
       2210745,
       2212066,
       2215585,
       2220611,
       2225085,
       2228373,
       2229190,
       2229649,
       2247002,
       2506864,
       2252851,
       2264431,
       2265447,
       2268806,
       2270361,
       2315417,
       2325236,
       2330280,
       2331675,
       2349894,
       2377225,
       2385659,
       2388695,
       2390408,
       2399213,
       2401846,
       2402050,
       2403296,
       2424769,
       2427365,
       2439149,
       2449995,
       2454966,
       2460026,
       2467038,
       2476394,
       2476870,
       2487394,
       2492541,
       2493883,
       2494668,
       2508710,
       2518435,
       2526514,
       2530079,
       2530507,
       2532883,
       2538123,
       2540289,
       2540405,
       2547935,
       2556742,
       2560158,
       2566314,
       2572417,
       2574892,
       2578161,
       2592633,
       2598018,
       2610287,
       2610368,
       2611069,
       2611525,
       2613714,
       2615465,
       2615487,
       2615515,
       2615605,
       2615620,
       2615705,
       2615908,
       2619886,
       2624870,
       2628120,
       2628125,
       2638970,
       2640657,
       2643029,
       2654111,
       2659891,
       2663126,
       2667577,
       2670636,
       2670823,
       2676813,
       2693063,
       2697347,
       2702313,
       2712108,
       2712532,
       2712549,
       2712608,
       2713686,
       2713850,
       2726440,
       2729046,
       2738268,
       2739884,
       2741117,
       2772166,
       2784353,
       2784616,
       2785618,
       2788500,
       2792223,
       2792790,
       2823065,
       2883551,
       2886553,
       2963099,
       2969363,
       2972940,
       2994736,
       3134360,
       3192709,
       3193734,
       3202674,
       3285022,
       3293824,
       1416907,
       2493664,
       2985934,
       2985935,
       2493587,
       1803522,
       2755125,
       2714814,
       2500300,
       2985933,
       3108309,
       3108308,
       2884705,
       2275400,
       3229667,
       1803502,
       1803512,
       2275489,
       2985932,
       2981982,
       1832463,
       1971745,
       1770999,
       2318436,
       2096954,
       3181534,
       3181535,
       3181536,
       3245632,
       2970259,
       3204670,
       3509035,
       3208365,
       2662378,
       3383599,
       3371597,
       3383599,
       2247002,
       3371597,
       2506864,
       1906584,
       2750249,
       2410509,
       742749,
       3059271,
       2508695,
       3352422,
       3150089,
       2555245,
       3208436,
       2884408,
       2786980,
       2544222,
       2686721,
       3287286,
       2987092,
       3238720,
       3393392,
       3466158,
       2599355,
       1579122,
       2771545
     )
   order by
     creation_date