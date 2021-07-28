with hold_data as (
  select
    datetime('now') as timestamp_now,
    -- consider the "delay days" as part of the age of the hold
    julianday(datetime('now')) - (julianday(h.placed_gmt) + h.delay_days) as hold_age,
    cast(
      julianday(datetime('now')) - julianday(placed_gmt) as integer
    ) as hold_age_days,
    *
  from
    hold as h
  where
    h.is_frozen is false
    and h.is_ir is false
    and h.is_ill is false
    and h.patron_ptype_code IN (
      0,
      1,
      2,
      3,
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
)
select
  -- pickup_location_code,
  (
    select
      case
        when branch_name.name = 'Main Library' then ' Main Library'
        else branch_name.name
      end
    from
      location
      join location_name on location_name.location_id = location.id
      join branch on branch.code_num = location.branch_code_num
      join branch_name on branch_name.branch_id = branch.id
    where
      location.code = hold_data.pickup_location_code
  ) as pickup_location,
  patron_ptype_code,
  count(distinct bib_record_num) as count_distinct_titles,
  count(*) as count,
  round(
    (count(*) * 1.0) / (count(distinct bib_record_num) * 1.0),
    2
  ) as avg_hold_per_title
from
  hold_data
group by
  1,
  2
order by
  1,
  2,
  3 desc
