/*postgres syntax*/
with sitevisits as (select s.customer_id,count(distinct s.page_id) as total_site_visits,
(extract(days from (max(s.event_time) - min(s.event_time))))::int/7 as weeks_active from sf.site_visit s
group by 1),

orders as (select o.customer_id,sum(total_amount) as total_expenditure from sf.order o group by 1)

select c.id,c.last_name,COALESCE(52 * 10 * ((total_expenditure/total_site_visits) * (total_site_visits::float/nullif(weeks_active,0))),0) as life_time_value
from sf.customer c
left join sitevisits s on s.customer_id = c.id
left join orders o on o.customer_id = c.id
order by 3 desc;
