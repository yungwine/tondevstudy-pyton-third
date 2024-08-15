import asyncio
import json

from pytoniq import LiteClient, LiteBalancer, WalletV4R2, begin_cell

from secret import mnemo


async def transfer():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        wallet = await WalletV4R2.from_mnemonic(client, mnemo)
        print(wallet)

        body1 = (begin_cell()
                .store_uint(0, 1)
                .end_cell())

        body2 = (begin_cell()
                .store_uint(0x7e8764ec, 32)  # op
                .store_uint(0, 64)  # query_id
                .store_uint(2, 32)  # increase by
                .end_cell())

        await wallet.transfer(destination='EQBJaPv2iqrs9EAppvdF38fPqGMkhksqA-nQKD6p8gG4O-gB', amount=1 * 10**7, body=body2)
        # await wallet.transfer(destination='EQBJaPv2iqrs9EAppvdF38fPqGMkhksqA-nQKD6p8gG4O-gB', amount=1 * 10**7, body=body)


async def trs():

    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        trs = await client.get_transactions('EQBJaPv2iqrs9EAppvdF38fPqGMkhksqA-nQKD6p8gG4O-gB', 2)
        tr = trs[0]
        print(tr.description)


asyncio.run(trs())
