import asyncio

from pytoniq import LiteClient, LiteBalancer, LiteServerError, RunGetMethodError


async def main():

    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        info = await client.get_masterchain_info()
        print(info)
        print('#' * 30)

        blk, _ = await client.lookup_block(wc=-1, shard=-2**63, seqno=info['last']['seqno'])
        print(blk)
        print('#' * 30)

        block_header = await client.raw_get_block_header(blk)
        print(block_header)
        print('#' * 30)

        block = await client.raw_get_block(blk)
        # print(block)
        print('#' * 30)
        # print(block.state_update.new)
        print('#' * 30)
        # print(block.extra)

        # trs = await client.raw_get_block_transactions(blk)
        # print(trs)
        # trs2 = await client.get_transactions(trs[0]['account'], count=1, from_lt=trs[0]['lt'], from_hash=trs[0]['hash'])
        # print(trs2)

        # trs = await client.raw_get_block_transactions_ext(blk)
        # print(trs)

        # shards = await client.get_all_shards_info(blk)
        # print(shards)
        #
        # for shard in shards:
        #     trs = await client.raw_get_block_transactions_ext(shard)
        #     print(len(trs))

        config = await client.get_config_all()
        print(config)

        params = await client.get_config_params(params=[1, 2, 14, 15])
        print(params)


asyncio.run(main())
