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
)
select
  (
    select
      count(hold_id) as count_holds
    from
      hold_data
    where
      patron_is_active is false
  ) as count_holds_for_inactive_patrons,
  (
    select
      count(hold_id) as count_holds
    from
      hold_data
    where
      patron_is_active is true
  ) as count_holds_for_active_patrons