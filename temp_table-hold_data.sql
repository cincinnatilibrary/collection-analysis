DROP TABLE IF EXISTS temp_holds
;


CREATE TEMP TABLE temp_holds AS
SELECT
h.patron_record_id,
pr.record_num as patron_record_num,
-- we only want to export bib-level holds for examination ...
-- CASE
-- 
-- 	WHEN r.record_type_code = 'i' THEN (
-- 		SELECT
-- 		l.bib_record_id
-- 
-- 		FROM
-- 		sierra_view.bib_record_item_record_link as l
-- 
-- 		WHERE
-- 		l.item_record_id = h.record_id
-- 
-- 		LIMIT 1
-- 	)
-- 	WHEN r.record_type_code = 'j' THEN (
-- 		SELECT
-- 		l.bib_record_id
-- 
-- 		FROM
-- 		sierra_view.bib_record_volume_record_link as l
-- 
-- 		WHERE
-- 		l.volume_record_id = h.record_id
-- 
-- 		LIMIT 1
-- 	)
-- 
-- 	WHEN r.record_type_code = 'b' THEN (
-- 		h.record_id
-- 	)
-- 
-- 	ELSE NULL
-- 
-- END AS bib_record_id,
r.record_type_code,
r.record_num,
h.record_id as bib_record_id,
h.placed_gmt,
(h.placed_gmt + concat(h.delay_days, ' days')::INTERVAL)::DATE as not_needed_before,
h.is_frozen,
h.delay_days,
h.expires_gmt::DATE as expires,
h.status,
h.is_ir,
h.pickup_location_code,
-- P#=1141671, I#=1450442, P=07-22-14, NNB=07-22-14 (0 days), RLA=0, NNA=08-29-14, ST=0, TP=b, PU=wpl  ;
concat(	'"',
	'P#=', pr.record_num,
	', I#=', r.record_num, -- this is just the bib record num, since we're only looking at bib-level holds, but would be the item, or volume number if we were looking at those (then set the TP to the code for that; e.g. i, j
	', P=', h.placed_gmt::DATE,
	', NNB=', (h.placed_gmt + concat(h.delay_days, ' days')::INTERVAL)::DATE, '(', h.delay_days, ' days)',
	', RLA=0', -- it's still unclear what this value is, but it seems to always be `0` in our data export
	', NNA=', coalesce(h.expires_gmt::DATE, (h.placed_gmt + '255 days'::INTERVAL)::DATE), -- this value seems to be null when a hold is in transit (but there's no hold in transit status on the hold itself)
	', ST=0', --it's still unclear what this value is , but it seems to always be either 0, or 116 in our data export (116 being very rare)
	', TP=', r.record_type_code,
	', PU=', h.pickup_location_code,
	'"'
) as hold_string

FROM
sierra_view.hold as h

JOIN
sierra_view.record_metadata as r
ON
  r.id = h.record_id

JOIN
sierra_view.record_metadata as pr
ON
  pr.id = h.patron_record_id

WHERE
r.record_type_code = 'b' -- only concerned with bib-level holds now
-- AND h.expires_gmt IS NOT NULL
;


CREATE INDEX bib_temp_holds ON temp_holds(bib_record_id)
;


SELECT
t.bib_record_id,
t.record_num as bib_record_num,
(
	SELECT
	string_agg(th.hold_string, ';' ORDER BY placed_gmt)

	FROM
	temp_holds as th

	WHERE
	t.bib_record_id = th.bib_record_id

	GROUP BY
	th.bib_record_id
) as holds

FROM
temp_holds as t

GROUP BY
t.bib_record_id,
t.record_num
;




----
-- TESTING / UNUSED
----

-- DROP TABLE IF EXISTS temp_bibs
-- ;


-- CREATE TEMP TABLE temp_bib as
-- SELECT
-- t.bib_record_id,
-- COUNT(*) as count
-- 
-- FROM
-- temp_holds as t
-- 
-- GROUP BY
-- t.bib_record_id
-- ;


-- WITH hold_bibs AS (
-- 	SELECT
-- 	t.bib_record_id
-- 
-- 	FROM
-- 	temp_holds as t
-- 
-- 	GROUP BY
-- 	t.bib_record_id
-- )
-- 
-- SELECT
-- t.bib_record_id,
-- string_agg(t.patron_record_id::TEXT, ';') AS hold_info
-- 
-- FROM
-- hold_bibs as h
-- 
-- JOIN
-- temp_holds as t
-- ON
--   t.bib_record_id = h.bib_record_id
-- 
-- GROUP BY
-- t.bib_record_id