Static SQL Queries & Reports: Holds
===================================

The following queries are useful for reporting purposes related to holds.

**NOTE** should the `Defining` queries be updated, ensure that the queries re-using those are updated as well. 

.. contents::

Defining "active holds"
-----------------------

`click to run query on "current_collection" <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=with+active_holds+as+%28%0D%0A++--+%22active+holds%22%0D%0A++--+--------------%0D%0A++--+This+will+produce+a+list+of+holds+meeting+the+following+criteria%3A%0D%0A++--+*+hold+that+is+not+Frozen+%28except+for+holds+placed+by+patrons+with+ptype+196%29%0D%0A++--+*+hold+with+zero+delay+days+OR+the+hold+delay+has+passed+%28hold+placed+date+%2B+delay+days+is+not+a+date+in+the+future%29%0D%0A++--+*+hold+placed+by+patron+with+one+of+the+following+ptype+codes%3A%0D%0A++--+++%28+0%2C+1%2C+2%2C+5%2C+6%2C+10%2C+11%2C+12%2C+15%2C+22%2C+30%2C+31%2C+32%2C+40%2C+41%2C+196+%29%0D%0A++--+*+hold+status+is+%22on+hold%22%0D%0A++select%0D%0A++++h.*%0D%0A++from%0D%0A++++hold+as+h%0D%0A++++join+record_metadata+as+r+on+%28%0D%0A++++++--+TODO+figure+out+if+maybe+we+could+just+use+the+%60is_ill%60+boolean+value+to+do+this+%28this+is+still+fast+since+it%27s+an+indexed+search%29%0D%0A++++++r.record_type_code+%3D+%27b%27%0D%0A++++++and+r.record_num+%3D+h.bib_record_num%0D%0A++++++and+r.campus_code+%3D+%27%27%0D%0A++++%29+--+join+the+record+metadata+so+that+we%27re+only+concerning+ourselves+with+titles+that+belong+to+us+%28to+filter+out+ILL+holds%29%0D%0A++where%0D%0A++++--+*+hold+that+is+not+Frozen+%28except+for+holds+placed+by+patrons+with+ptype+196%29%0D%0A++++%28%0D%0A++++++h.is_frozen+is+FALSE%0D%0A++++++OR+h.patron_ptype_code+%3D+196%0D%0A++++%29%0D%0A++++AND+--+*+hold+with+zero+delay+days+OR+the+hold+delay+has+passed+%28hold+placed+date+%2B+delay+days+is+not+in+the+future%29%0D%0A++++%28%0D%0A++++++julianday%28datetime%28%27now%27%29%29+-+%28%0D%0A++++++++julianday%28h.placed_gmt%29+%2B+%28h.delay_days+*+1.0%29%0D%0A++++++%29%0D%0A++++%29+%3E+0%0D%0A++++AND+--+*+hold+placed+by+patron+with+one+of+the+following+ptype+codes%3A%0D%0A++++--+++%28+0%2C+1%2C+2%2C+5%2C+6%2C+10%2C+11%2C+12%2C+15%2C+22%2C+30%2C+31%2C+32%2C+40%2C+41%2C+196+%29%0D%0A++++h.patron_ptype_code+IN+%28%0D%0A++++++0%2C%0D%0A++++++1%2C%0D%0A++++++2%2C%0D%0A++++++5%2C%0D%0A++++++6%2C%0D%0A++++++10%2C%0D%0A++++++11%2C%0D%0A++++++12%2C%0D%0A++++++15%2C%0D%0A++++++22%2C%0D%0A++++++30%2C%0D%0A++++++31%2C%0D%0A++++++32%2C%0D%0A++++++40%2C%0D%0A++++++41%2C%0D%0A++++++196%0D%0A++++%29%0D%0A++++AND+--+*+hold+status+is+%22on+hold%22%0D%0A++++h.hold_status+%3D+%27on+hold%27%0D%0A%29%0D%0Aselect%0D%0A++*%0D%0Afrom%0D%0A++active_holds>`__

**IMPORTANT** remember to update this in any of the queries that utilize this if we make changes to this definition.

This query is written so that it can be re-used in conjunction with another query or search where "active holds" are wanting to be considered.

.. code-block:: sql

      with active_holds as (
        -- "active holds"
        -- --------------
        -- This will produce a list of holds meeting the following criteria:
        -- * hold that is not Frozen (except for holds placed by patrons with ptype 196)
        -- * hold with zero delay days OR the hold delay has passed (hold placed date + delay days is not a date in the future)
        -- * hold placed by patron with one of the following ptype codes:
        --   ( 0, 1, 2, 5, 6, 10, 11, 12, 15, 22, 30, 31, 32, 40, 41, 196 )
        -- * hold status is "on hold"
        select
          h.*
        from
          hold as h
          join record_metadata as r on (
            -- TODO figure out if maybe we could just use the `is_ill` boolean value to do this (this is still fast since it's an indexed search)
            r.record_type_code = 'b'
            and r.record_num = h.bib_record_num
            and r.campus_code = ''
          ) -- join the record metadata so that we're only concerning ourselves with titles that belong to us (to filter out ILL holds)
        where
          -- * hold that is not Frozen (except for holds placed by patrons with ptype 196)
          (
            h.is_frozen is FALSE
            OR h.patron_ptype_code = 196
          )
          AND -- * hold with zero delay days OR the hold delay has passed (hold placed date + delay days is not in the future)
          (
            julianday(datetime('now')) - (
              julianday(h.placed_gmt) + (h.delay_days * 1.0)
            )
          ) > 0
          AND -- * hold placed by patron with one of the following ptype codes:
          --   ( 0, 1, 2, 5, 6, 10, 11, 12, 15, 22, 30, 31, 32, 40, 41, 196 )
          h.patron_ptype_code IN (
            0,
            1,
            2,
            5,
            6,
            10,
            11,
            12,
            15,
            22,
            30,
            31,
            32,
            40,
            41,
            196
          )
          AND -- * hold status is "on hold"
          h.hold_status = 'on hold'
      )
      select
        *
      from
        active_holds
   

Defining "active items"
-----------------------
  
`click to run query on "current_collection" <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=with+active_items+as+%28%0D%0A++--+%22active+items%22%0D%0A++--+--------------%0D%0A++--+This+will+produce+a+list+of+items+meeting+the+following+criteria%3A%0D%0A++--+*+item+status+is+one+of+the+following+codes%3A%0D%0A++--+++%28%27-%27%2C+%27%21%27%2C+%27b%27%2C+%27p%27%2C+%27%28%27%2C+%27%40%27%2C+%27%29%27%2C+%27_%27%2C+%27%3D%27%2C+%27%2B%27%2C+%27t%27%29%0D%0A++--+*+if+the+item+has+a+due+date%2C+then+it+must+be+less+than+60+days+overdue%3A%0D%0A++--+++coalesce%28+%28julianday%28date%28%27now%27%29%29+-+julianday%28item.due_date%29+%3E+60.0+%29%2C+FALSE%29%0D%0A++select%0D%0A++++item.item_record_num%2C%0D%0A++++v.volume_record_num%2C%0D%0A++++v.volume_statement%2C%0D%0A++++v.items_display_order%2C%0D%0A++++item.bib_record_num%0D%0A++from%0D%0A++++item+--+we+need+to+consider+volume+information+for+volume-level+holds%0D%0A++++left+outer+join+volume_record_item_record_link+as+v+on+v.item_record_num+%3D+item.item_record_num%0D%0A++++join+record_metadata+as+r+on+%28%0D%0A++++++r.record_type_code+%3D+%27b%27%0D%0A++++++and+r.record_num+%3D+item.bib_record_num%0D%0A++++++and+r.campus_code+%3D+%27%27%0D%0A++++%29%0D%0A++where%0D%0A++++--+*+item+status+is+one+of+the+following+codes%3A%0D%0A++++--+++%28%27-%27%2C+%27%21%27%2C+%27b%27%2C+%27p%27%2C+%27%28%27%2C+%27%40%27%2C+%27%29%27%2C+%27_%27%2C+%27%3D%27%2C+%27%2B%27%2C+%27t%27%29%0D%0A++++item.item_status_code+in+%28%0D%0A++++++%27-%27%2C%0D%0A++++++%27%21%27%2C%0D%0A++++++%27b%27%2C%0D%0A++++++%27p%27%2C%0D%0A++++++%27%28%27%2C%0D%0A++++++%27%40%27%2C%0D%0A++++++%27%29%27%2C%0D%0A++++++%27_%27%2C%0D%0A++++++%27%3D%27%2C%0D%0A++++++%27%2B%27%2C%0D%0A++++++%27t%27%0D%0A++++%29+--+*+if+the+item+has+a+due+date%2C+then+it+must+be+less+than+60+days+overdue%3A%0D%0A++++--+++coalesce%28+%28julianday%28date%28%27now%27%29%29+-+julianday%28item.due_date%29+%3E+60.0+%29%2C+FALSE%29%0D%0A++++and+coalesce%28%0D%0A++++++%28%0D%0A++++++++julianday%28date%28%27now%27%29%29+-+julianday%28item.due_date%29+%3E+60.0%0D%0A++++++%29%2C%0D%0A++++++FALSE%0D%0A++++%29+is+FALSE%0D%0A%29%0D%0Aselect%0D%0A++*%0D%0Afrom%0D%0A++active_items>`__

.. code-block:: sql
   
   with active_items as (
     -- "active items"
     -- --------------
     -- This will produce a list of items meeting the following criteria:
     -- * item status is one of the following codes:
     --   ('-', '!', 'b', 'p', '(', '@', ')', '_', '=', '+', 't')
     -- * if the item has a due date, then it must be less than 60 days overdue:
     --   coalesce( (julianday(date('now')) - julianday(item.due_date) > 60.0 ), FALSE)
     select
       item.bib_record_num,
       item.item_record_num,
       v.volume_record_num,
       v.volume_statement,
       v.items_display_order
     from
       item
       left outer join volume_record_item_record_link as v on v.item_record_num = item.item_record_num -- we need to consider volume information for volume-level holds
       join record_metadata as r on (
         r.record_type_code = 'b'
         and r.record_num = item.bib_record_num
         and r.campus_code = ''
       ) -- considers only items belonging to us (no virtual items)
     where
       -- * item status is one of the following codes:
       --   ('-', '!', 'b', 'p', '(', '@', ')', '_', '=', '+', 't')
       item.item_status_code in (
         '-',
         '!',
         'b',
         'p',
         '(',
         '@',
         ')',
         '_',
         '=',
         '+',
         't'
       ) -- * if the item has a due date, then it must be less than 60 days overdue:
       --   coalesce( (julianday(date('now')) - julianday(item.due_date) > 60.0 ), FALSE)
       and coalesce(
         (
           julianday(date('now')) - julianday(item.due_date) > 60.0
         ),
         FALSE
       ) is FALSE
   )
   select
     *
   from
     active_items

----

"active holds" by title (sorted by count "active holds")
--------------------------------------------------------

`click to run query on "current_collection" <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection?sql=with+active_holds+as+%28%0D%0A++--+%22active+holds%22%0D%0A++--+--------------%0D%0A++--+This+will+produce+a+list+of+holds+meeting+the+following+criteria%3A%0D%0A++--+*+hold+that+is+not+Frozen+%28except+for+holds+placed+by+patrons+with+ptype+196%29%0D%0A++--+*+hold+with+zero+delay+days+OR+the+hold+delay+has+passed+%28hold+placed+date+%2B+delay+days+is+not+a+date+in+the+future%29%0D%0A++--+*+hold+placed+by+patron+with+one+of+the+following+ptype+codes%3A%0D%0A++--+++%28+0%2C+1%2C+2%2C+5%2C+6%2C+10%2C+11%2C+12%2C+15%2C+22%2C+30%2C+31%2C+32%2C+40%2C+41%2C+196+%29%0D%0A++--+*+hold+status+is+%22on+hold%22%0D%0A++select%0D%0A++++h.*%0D%0A++from%0D%0A++++hold+as+h%0D%0A++++join+record_metadata+as+r+on+%28%0D%0A++++++--+TODO+figure+out+if+maybe+we+could+just+use+the+%60is_ill%60+boolean+value+to+do+this+%28this+is+still+fast+since+it%27s+an+indexed+search%29%0D%0A++++++r.record_type_code+%3D+%27b%27%0D%0A++++++and+r.record_num+%3D+h.bib_record_num%0D%0A++++++and+r.campus_code+%3D+%27%27%0D%0A++++%29+--+join+the+record+metadata+so+that+we%27re+only+concerning+ourselves+with+titles+that+belong+to+us+%28to+filter+out+ILL+holds%29%0D%0A++where%0D%0A++++--+*+hold+that+is+not+Frozen+%28except+for+holds+placed+by+patrons+with+ptype+196%29%0D%0A++++%28%0D%0A++++++h.is_frozen+is+FALSE%0D%0A++++++OR+h.patron_ptype_code+%3D+196%0D%0A++++%29%0D%0A++++AND+--+*+hold+with+zero+delay+days+OR+the+hold+delay+has+passed+%28hold+placed+date+%2B+delay+days+is+not+in+the+future%29%0D%0A++++%28%0D%0A++++++julianday%28datetime%28%27now%27%29%29+-+%28%0D%0A++++++++julianday%28h.placed_gmt%29+%2B+%28h.delay_days+*+1.0%29%0D%0A++++++%29%0D%0A++++%29+%3E+0%0D%0A++++AND+--+*+hold+placed+by+patron+with+one+of+the+following+ptype+codes%3A%0D%0A++++--+++%28+0%2C+1%2C+2%2C+5%2C+6%2C+10%2C+11%2C+12%2C+15%2C+22%2C+30%2C+31%2C+32%2C+40%2C+41%2C+196+%29%0D%0A++++h.patron_ptype_code+IN+%28%0D%0A++++++0%2C%0D%0A++++++1%2C%0D%0A++++++2%2C%0D%0A++++++5%2C%0D%0A++++++6%2C%0D%0A++++++10%2C%0D%0A++++++11%2C%0D%0A++++++12%2C%0D%0A++++++15%2C%0D%0A++++++22%2C%0D%0A++++++30%2C%0D%0A++++++31%2C%0D%0A++++++32%2C%0D%0A++++++40%2C%0D%0A++++++41%2C%0D%0A++++++196%0D%0A++++%29%0D%0A++++AND+--+*+hold+status+is+%22on+hold%22%0D%0A++++h.hold_status+%3D+%27on+hold%27%0D%0A%29%0D%0Aselect%0D%0A++a.bib_record_num%2C%0D%0A++count%28a.bib_record_num%29+as+count_active_holds%2C%0D%0A++round%28%0D%0A++++avg%28%0D%0A++++++julianday%28%27now%27%29+-+%28julianday%28a.placed_gmt%29+%2B+%28a.delay_days+*+1.0%29%29%0D%0A++++%29%2C%0D%0A++++2%0D%0A++%29+as+average_age_days_of_hold%2C%0D%0A++bib.best_author%2C%0D%0A++bib.best_title%2C%0D%0A++bib.publish_year%2C%0D%0A++bib.creation_date+as+bib_creation_date%2C%0D%0A++bib.bib_level_callnumber%0D%0Afrom%0D%0A++active_holds+as+a%0D%0A++join+bib+on+bib.bib_record_num+%3D+a.bib_record_num%0D%0Agroup+by%0D%0A++a.bib_record_num%0D%0Aorder+by%0D%0A++count_active_holds+desc>`__

.. code-block:: sql

   with active_holds as (
     -- "active holds"
     -- --------------
     -- This will produce a list of holds meeting the following criteria:
     -- * hold that is not Frozen (except for holds placed by patrons with ptype 196)
     -- * hold with zero delay days OR the hold delay has passed (hold placed date + delay days is not a date in the future)
     -- * hold placed by patron with one of the following ptype codes:
     --   ( 0, 1, 2, 5, 6, 10, 11, 12, 15, 22, 30, 31, 32, 40, 41, 196 )
     -- * hold status is "on hold"
     select
       h.*
     from
       hold as h
       join record_metadata as r on (
         -- TODO figure out if maybe we could just use the `is_ill` boolean value to do this (this is still fast since it's an indexed search)
         r.record_type_code = 'b'
         and r.record_num = h.bib_record_num
         and r.campus_code = ''
       ) -- join the record metadata so that we're only concerning ourselves with titles that belong to us (to filter out ILL holds)
     where
       -- * hold that is not Frozen (except for holds placed by patrons with ptype 196)
       (
         h.is_frozen is FALSE
         OR h.patron_ptype_code = 196
       )
       AND -- * hold with zero delay days OR the hold delay has passed (hold placed date + delay days is not in the future)
       (
         julianday(datetime('now')) - (
           julianday(h.placed_gmt) + (h.delay_days * 1.0)
         )
       ) > 0
       AND -- * hold placed by patron with one of the following ptype codes:
       --   ( 0, 1, 2, 5, 6, 10, 11, 12, 15, 22, 30, 31, 32, 40, 41, 196 )
       h.patron_ptype_code IN (
         0,
         1,
         2,
         5,
         6,
         10,
         11,
         12,
         15,
         22,
         30,
         31,
         32,
         40,
         41,
         196
       )
       AND -- * hold status is "on hold"
       h.hold_status = 'on hold'
   )
   select
     a.bib_record_num,
     count(a.bib_record_num) as count_active_holds,
     round(
       avg(
         julianday('now') - (julianday(a.placed_gmt) + (a.delay_days * 1.0))
       ),
       2
     ) as average_age_days_of_hold,
     bib.best_author,
     bib.best_title,
     bib.publish_year,
     bib.creation_date as bib_creation_date,
     bib.bib_level_callnumber
   from
     active_holds as a
     join bib on bib.bib_record_num = a.bib_record_num
   group by
     a.bib_record_num
   order by
     count_active_holds desc
