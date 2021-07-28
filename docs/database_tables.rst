Database Tables, Columns, and Definitions
=========================================

.. contents::

The following are tables contained in each of the database snapshots.

The two primary tables are ``bib`` (representing *title* metadata--``best_author`` and 
``best_title`` for example) and ``item`` (representing *item* metadata--``barcode`` and 
``price_cents`` for example)

**bib** Table, **item** Table Relationship
------------------------------------------

The **bib** Table and **item** Table are linked via the **bib_record_num** foreign key value, in a *one-to-many* relationship

The following SQL, for example, shows how you can count the number of items (**item_record_num**) associated with the selected **bib_record_num**

.. code-block:: sql

   select
     bib.bib_record_num,
     (
       select
         count(item.item_record_num)
       from
         item
       where
         item.bib_record_num = bib.bib_record_num
     ) as count_attached_items
   from
     bib
   limit
     100

**bib** Table
-------------

Data in the ``bib`` table provides information about a resource's metadata as described below:

==================== ============
column name          description 
==================== ============
bib_record_num       foreign key to ``record_metadata.record_num`` value associated with bib record
creation_date        ISO 8601 formatted date (YYYY-MM-DD) that the resource
                     
                     was created in the CHPL catalog system
record_last_updated  ISO 8601 formatted date (YYYY-MM-DD) that the resource was last changed
isbn                 International Standard Book Number (if available)
                     associated with the resource
best_author          The primary author (if available) associated with the resource
best_title           The primary title associated with the resource
publisher            Company or person associated with publishing the resource  
publish_year         The year of publication associated with the resource
bib_level_callnumber The library classification call number associated with the

                     resource (this may be different than the item call number)
indexed_subjects     Subject headings, subject terms, index terms, or descriptors associated 
                     
                     with the resource
==================== ============

`Browse the current_collection bib table <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection/bib>`_

**item** Table
--------------

Data in the ``item`` table provides information about a resource's metadata as described below:

=================================   ===========
column name                         description 
=================================   ===========
item_record_num                     foreign key to ``record_metadata.record_num`` value associated
                                    
                                    with item record
bib_record_num                      foreign key to ``record_metadata.record_num`` value associated 

                                    with bib record
creation_date                       ISO 8601 formatted date (YYYY-MM-DD) that the resource
                     
                                    was created in the CHPL catalog system
record_last_updated                 ISO 8601 formatted date (YYYY-MM-DD) that the resource 

                                    was last changed
barcode                             Machine-readable ID that is affixed or kept with the 

                                    physical material
agency_code_num                     Owning / original agency associated with the item
location_code                       Physical location of the item
checkout_statistic_group_code_num   Last assigned statistical code--assigned by a specific terminal / 

                                    location at the last checkout transaction
checkin_statistics_group_code_num   Last assigned statistical code--assigned by a specific terminal / 

                                    location at the last check in transaction
checkout_date                       If the item was checked out at the time of the snapshot, this 

                                    value will represent the ISO 8601 formatted (YYYY-MM-DD) 
                                    
                                    check out date  
due_date                            If the item was checked out at the time of the snapshot, this 

                                    value will represent the ISO 8601 formatted (YYYY-MM-DD) 
                                    
                                    due date of the item, otherwise the value is NULL
patron_branch_code                  If the item was checked out at the time of the snapshot, this 

                                    value will represent the "home library" code for the patron, 
                                    
                                    otherwise the value is NULL
last_checkout_date                  ISO 8601 formatted date (YYYY-MM-DD) that the resource 

                                    was last checked out (if the item is currently checked out,
                                    
                                    this will represent the previous checkout date) 
last_checkin_date                   ISO 8601 formatted date (YYYY-MM-DD) that the resource  

                                    was last checked in
checkout_total                      Total count of check out transactions associated with the item
renewal_total                       Total count of renewal transactions associated with the item
isbn                                International Standard Book Number (if available) associated

                                    with the resource
item_format                         Controlled-vocabulary description of the type of item
item_status_code                    Code representing a controlled-vocabulary description of the  

                                    status of the item
price_cents                         Assigned value of the item in USD (represented as an integer  

                                    value in cents)
item_callnumber                     The library classification call number associated with the

                                    resource
=================================   ===========

`Browse the current_collection item table <https://ilsweb.cincinnatilibrary.org/collection-analysis/current_collection/item>`_

**bib_record** Table
--------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for row
record_id                           foreign key to ``record_metadata`` table
language_code                       code as defined in ``language_property`` table
bcode1                              fixed field "Bib Level" code as defined in ``bib_level_property_myuser`` table
bcode2                              fixed field: "Format (Mat Type)" code as defined in 

                                    ``material_property_myuser`` table
bcode3                              fixed field: "Suppress". Possible codes are the following:

                                    ``-``: —,
                                    
                                    ``d``: DELETE CODE,

                                    ``n``: SUPPRESS, 
                                    
                                    ``c``: SUPPRESS ORD, 

                                    ``s``: SYMPHONY SUPPRESS
country_code                        code as defined in ``country_property_myuser`` table
index_change_count                  count changes to index
is_on_course_reserve                N/A
is_right_result_exact               N/A
allocation_rule_code                N/A
skip_num                            ignored characters at start of ``best_title`` column in ``bib``
cataloging_date_gmt                 ISO 8601 formatted date (YYYY-MM-DD) that the resource

                                    was made available to the public access catalog
marc_type_code                      N/A
is_suppressed                       boolean value indicating if a bib is is_suppressed to the 

                                    public access catalog
=================================   ===========

**item_status_property_myuser** Table
-------------------------------------

=================================   ===========
column name                         description 
=================================   ===========
code                                item status code
display_order                       display order
name                                full item status name
=================================   ===========

**itype_property_myuser** Table
-------------------------------

=================================   ===========
column name                         description 
=================================   ===========
code                                itype code
display_order                       display order
itype_property_category_id          N/A
physical_format_id                  foreign key to physical_format
target_audience_id                  N/A
name                                full itype name
=================================   ===========

**physical_format_myuser** Table
--------------------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for ``physical_format``
is_default                          N/A
display_order                       display order
name                                full physical format name
=================================   ===========

**country_property_myuser** Table
---------------------------------

=================================   ===========
column name                         description 
=================================   ===========
code                                county code
display_order                       display order
name                                full country name
=================================   ===========

**language_property** Table
---------------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for row
code                                language code
display_order                       display order
name                                full language name
=================================   ===========

**record_metadata** Table
-------------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for record
record_type_code                    code indicating the type of record. Possible codes are the following:

                                    ``b``: bibliographic

                                    ``i``: item

                                    ``j``: volume
                                                                        
record_num                          primary key for record number
creation_date_gmt                   ISO 8601 formatted date (YYYY-MM-DD) that the record

                                    was created

deletion_date_gmt                   ISO 8601 formatted date (YYYY-MM-DD) that the record

                                    was deleted
campus_code                         campus code (blank indicating the record is not virtual)
agency_code_num                     N/A
record_last_updated_gmt             ISO 8601 formatted date (YYYY-MM-DD) that the record

                                    was last updated
=================================   ===========

**bib_record_item_record_link** Table
-------------------------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for row
bib_record_id                       foreign key to ``record_metadata`` table
item_record_id                      foreign key to ``record_metadata`` table
items_display_order                 multiple items attached to bib will have this order
bibs_display_order                  N/A
=================================   ===========

----

**location** Table, **location_name** Table, **branch** Table, **branch_name** Table Relationship
-------------------------------------------------------------------------------------------------

This SQL example shows the relationship between tables ``location``, ``location_name``, ``branch``, and ``branch_name``

.. code-block:: sql

   select
     "location".*,
     "location_name".*,
     "branch".*,
     "branch_name".*
   from
     "location"
     join "location_name" on "location_name".location_id = "location".id
     join "branch" on "branch".code_num = "location".branch_code_num
     join "branch_name" on "branch_name".branch_id = "branch".id
   order by
     "location".id

**location** Table
------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for location
code                                location code
branch_code_num                     foreign key to ``branch`` (code)
parent_location_code                N/A
is_public                           indicates if patrons see the code in the public interfaces
is_requestable                      N/A
=================================   ===========

**location_name** Table
-----------------------

=================================   ===========
column name                         description 
=================================   ===========
location_id                         foreign key to ``location`` table
name                                location full name
iii_language_id                     N/A
=================================   ===========

**branch** Table
----------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for row
address                             post office address for branch
email_source                        source email address for email sent by branch
email_reply_to                      reply email address for email sent by branch
address_latitude                    approximate branch latitude
address_longitude                   approximate branch longitude
code_num                            primary key (branch code number)
=================================   ===========

**branch_name** Table
---------------------

=================================   ===========
column name                         description 
=================================   ===========
branch_id                           foreign key to ``branch``
name                                branch full name
iii_language_id                     N/A
=================================   ===========

**phrase_entry** Table
----------------------

=================================   ===========
column name                         description 
=================================   ===========
id                                  primary key for row
record_id                           foreign key to record_metadata
index_tag                           type of index (this data only contains "d"--subject indexes)
varfield_type_code                  type of varfield (this data only contains "d"--subject varfields)
occurrence                          N/A
is_permuted                         boolean value indicating if text is permuted
type2                               N/A
type3                               suppression code for public display: 

                                    ``n``: suppress from public display``
                                    
                                    (blank): do not suppress from public display

index_entry                         index value (subject index)
insert_title                        normalized title
phrase_rule_rule_num                N/A
phrase_rule_operation               N/A
phrase_rule_subfield_list           N/A
original_content                    non-normalized original input
parent_record_id                    N/A
insert_title_tag                    N/A
insert_title_occ                    N/A
=================================   ===========
