Database Tables, Columns, and Definitions
=========================================

The following are tables contained in each of the database snapshots

``bib`` Table
-------------

Data in the ``bib`` table provides information about a resource's metadata as described below:

==================== ============
column name          description 
==================== ============
bib_record_num       distinct record id for the resource
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

``item`` Table
--------------

Data in the ``item`` table provides information about a resource's metadata as described below:

=================================   ===========
column name                         description 
=================================   ===========
item_record_num                     Distinct record id for the resource
bib_record_num                      Record id linking the item to the bib record
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

**TODO**: Add other tables