DROP TABLE IF EXISTS temp_map_item_type
;


CREATE TEMP TABLE temp_map_item_type AS
SELECT
p.code_num as code,
n.name as name

FROM
sierra_view.itype_property as p

JOIN
sierra_view.itype_property_name as n
ON
  n.itype_property_id = p.id

ORDER BY
code
;


CREATE INDEX temp_map_item_type_code ON temp_map_item_type(code)
;


-- TESTING
-- SELECT
-- *
-- FROM
-- temp_map_item_type


DROP TABLE IF EXISTS temp_item_export
;


-- give this query some extra time to complete (60000 milliseconds = 1 minute)
-- (3600000 milliseconds = 60 minutes)
set statement_timeout to 3600000; commit
;


CREATE TEMP TABLE temp_item_export AS
SELECT
r.id as item_record_id,
r.record_num as item_record_num,
br.id as bib_record_id,
br.record_num as bib_record_num,
r.creation_date_gmt::date AS creation_date,
r.record_last_updated_gmt::date as record_last_updated,
p.barcode,
i.agency_code_num,
i.location_code,
i.checkout_statistic_group_code_num,
i.checkin_statistics_group_code_num,
c.checkout_gmt::date as checkout_date,
c.due_gmt::date as due_date,
(
	SELECT
	p.home_library_code

	FROM
	sierra_view.patron_record as p

	WHERE
	p.record_id = c.patron_record_id

	LIMIT 1
) as patron_branch_code,
i.last_checkout_gmt::date as last_checkout_date,
i.last_checkin_gmt::date as last_checkin_date,
i.checkout_total,
i.renewal_total,
-- isbn being pulled from the bib record marc varfield
(
	SELECT
	regexp_matches(
		--regexp_replace(trim(v.field_content), '(\|[a-z]{1})', '', 'ig'), -- get the call number strip the subfield indicators
		v.field_content,
		'[0-9]{9,10}[x]{0,1}|[0-9]{12,13}[x]{0,1}', -- the regex to match on (10 or 13 digits, with the possibility of the 'X' character in the check-digit spot)
		'i' -- regex flags; ignore case
	)

	FROM
	sierra_view.varfield as v

	WHERE
	v.record_id = br.id
	AND v.marc_tag || v.varfield_type_code = '020i'

	ORDER BY
	v.occ_num

	LIMIT 1
)[1]::varchar(30) as isbn,
(
	SELECT
	t.name

	FROM
	temp_map_item_type AS t	

	WHERE
	t.code = i.itype_code_num

	LIMIT 1
) as item_format,
i.item_status_code,
i.price::numeric(30,2)::money AS price,
p.call_number_norm AS item_callnumber
 
FROM
sierra_view.record_metadata as r

JOIN
sierra_view.item_record_property as p
ON
  p.item_record_id = r.id

JOIN
sierra_view.item_record as i
ON
  i.record_id = r.id

-- item may not be checked out, so we want to left join so we don't exclude items that are not checked out
LEFT OUTER JOIN
sierra_view.checkout as c
ON
  c.item_record_id = r.id

JOIN
sierra_view.bib_record_item_record_link as l
ON
  l.item_record_id = r.id

JOIN
sierra_view.record_metadata as br
ON
  br.id = l.bib_record_id

WHERE
r.record_type_code = 'i'
AND r.campus_code = ''
AND r.deletion_date_gmt is NULL

-- TESTING -- only fetch a small sample
LIMIT 20000
;


-- TESTING -- select data from the temp table for output
-- SELECT * FROM temp_item_export
-- ;