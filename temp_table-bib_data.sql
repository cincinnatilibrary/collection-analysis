DROP TABLE IF EXISTS temp_bib_record_metadata
;


-- creating temp table of the record ids, and the bib record numbers that we're interested in
-- (campus_code being blank indicates that the record belongs to us, and not a virtual one (interlibrary loan functions)
CREATE TEMP TABLE temp_bib_record_metadata AS
SELECT
r.id, 
r.record_num as bib_record_num,
r.creation_date_gmt::date as creation_date,
r.record_last_updated_gmt::date as record_last_updated

FROM
sierra_view.record_metadata AS r

WHERE
r.record_type_code = 'b'
AND r.campus_code = ''
AND r.deletion_date_gmt IS NULL
;


DROP TABLE IF EXISTS temp_bib_export
;


-- give this query some extra time to complete (60000 milliseconds = 1 minute)
-- (3600000 milliseconds = 60 minutes)
set statement_timeout to 3600000; commit
;


CREATE TEMP TABLE temp_bib_export AS
SELECT
r.bib_record_num,
r.id as bib_record_id,
(
	SELECT
	string_agg(po.index_entry, ',' ORDER BY po.occurrence, po.id)

	FROM
	sierra_view.phrase_entry as po

	WHERE
	po.record_id = r.id
	AND po.index_tag = 'o'
	AND po.varfield_type_code = 'o'
) AS control_numbers,
r.creation_date,
r.record_last_updated,
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
	v.record_id = r.id
	AND v.marc_tag || v.varfield_type_code = '020i'

	ORDER BY
	v.occ_num

	LIMIT 1

)[1]::varchar(30) as isbn, 
p.best_author,
p.best_author_norm,
p.best_title,
p.best_title_norm,
-- publisher is not not normalized as our sierra instance doesn't index this field
(
	SELECT
	s.content
	FROM
	sierra_view.subfield as s

	WHERE
	s.record_id = r.id
	AND s.field_type_code = 'p'
	AND s.tag = 'b'

	ORDER BY
	s.display_order

	LIMIT 1
) as publisher,
p.publish_year,
-- the normalized call number on the bib
(
	SELECT
	pc.index_entry

	FROM
	sierra_view.phrase_entry as pc

	WHERE
	pc.record_id = r.id
	AND pc.index_tag = 'c'
	AND pc.varfield_type_code = 'c'

	ORDER BY
	pc.id

	LIMIT 1
) as bib_level_callnumber,


-- -- This is the previous method used to extract call number for the bib record
-- (	
-- 	SELECT
-- 	TRIM(s.content || ' ' || COALESCE(sb.content, ''))
-- 	FROM
-- 	sierra_view.subfield as s
-- 
-- 	LEFT OUTER JOIN
-- 	sierra_view.subfield as sb
-- 	ON
-- 	  sb.record_id = r.id
-- 	  AND sb.field_type_code = 'c'
-- 	  AND sb.tag = 'b'
-- 
-- 	WHERE
-- 	s.record_id = r.id
-- 	AND s.field_type_code = 'c'
-- 	AND s.tag = 'a'
-- 
-- 	ORDER BY
-- 	s.display_order
-- 
-- 	LIMIT 1
-- ) as bib_level_callnumber_prev,
-- indexed_subjects are subject headings coming from the normalized and indexed sierra fields for fields tagged 'Subject'
(
	SELECT
	string_agg(p.index_entry, ',' ORDER BY p.occurrence, p.id) as subject

	FROM
	sierra_view.phrase_entry as p

	WHERE
	p.record_id = r.id
	-- index tag d is subject
	AND p.index_tag = 'd'
) as indexed_subjects

FROM
temp_bib_record_metadata as r

JOIN
sierra_view.bib_record_property as p
ON
  p.bib_record_id = r.id

-- TESTING -- only fetch a small sample
LIMIT 20000
;

-- TESTING -- select data from the temp table for output
-- SELECT * FROM temp_bib_export
-- ;