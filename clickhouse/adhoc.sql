-- How many ERC-20 token contracts were found? (token_address gives the address of the ERC-20 contract)

-- Current balance for any token address (difference between value in transfers involving the address in to_address and from_address)

-- Highest transaction in a block

select block_hash,max(value) as max_transaction_value from arda_test.transactions group by block_hash order by max_transaction_value desc;
