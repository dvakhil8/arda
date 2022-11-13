select timestamp,avg(transaction_count) over (order by timestamp asc ROWS BETWEEN 100 PRECEDING AND CURRENT ROW ) as moving_average
 from arda_test.blocks order by timestamp desc