import asyncio
import time

import requests
from pytoniq import LiteClient, LiteServerError


async def check(client: LiteClient, seqno_from: int, seqno_to: int):
    seqno = (seqno_from + seqno_to) // 2

    if seqno_to - seqno_from <= 1:
        return seqno_to

    try:
        await client.lookup_block(wc=-1, shard=-2**63, seqno=seqno)
        print('Block found:', seqno)
        return await check(client, seqno_from, seqno)
    except LiteServerError as e:
        print(e)
        return await check(client, seqno, seqno_to)


async def main():
    config = requests.get('https://ton.org/testnet-global.config.json').json()
    for i in range(len(config['liteservers'])):
        async with LiteClient.from_config(config, i, trust_level=2) as client:
            info = await client.get_masterchain_info()
            print(info)
            known_seqno = await check(client, 0, info['last']['seqno'])
            print(f'Last known block for ls {i}:', known_seqno)
            blk, block = await client.lookup_block(wc=-1, shard=-2**63, seqno=known_seqno)
            print(f'Block was {int(time.time()) - block.info.gen_utime} seconds ago')


asyncio.run(main())
