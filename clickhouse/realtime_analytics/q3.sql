with recevied_by_cte as (
    select from_address,count(*) as received_count from arda_test.transactions group by from_address
),
     transfers_sent_cte as (
         select to_address,count(*) as transfer_count from arda_test.transactions group by to_address
     )
select coalesce(from_address,to_address) as address , received_count,transfer_count from recevied_by_cte full outer join transfers_sent_cte on recevied_by_cte.from_address=transfers_sent_cte.to_address
