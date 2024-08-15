import asyncio
import json

from pytoniq import LiteClient, LiteBalancer, LiteServerError, RunGetMethodError


async def liteserver():

    client = LiteClient.from_mainnet_config(ls_i=5, trust_level=2)

    await client.connect()

    info = await client.get_masterchain_info()
    print(info)

    await client.close()

    async with LiteClient.from_mainnet_config(ls_i=5, trust_level=2) as client:
        info = await client.get_masterchain_info()
        print(info)


async def balancer():
    client = LiteBalancer.from_mainnet_config(trust_level=2)

    await client.start_up()

    # info = await client.get_masterchain_info()
    # print(info)
    try:
        await client.lookup_block(-1, -2**63, seqno=1)
    except LiteServerError as e:
        print(e.code, e.message)

    try:
        await client.run_get_method('UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9', 'seqnoo', stack=[])
    except RunGetMethodError as e:
        print(e.address, e.method, e.exit_code)

    # await client.lookup_block(-1, -2**63, seqno=1, only_archive=True)
    # await client.get_masterchain_info(choose_random=True)

    await client.close_all()

    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        info = await client.get_masterchain_info()
        print(info)


asyncio.run(balancer())


