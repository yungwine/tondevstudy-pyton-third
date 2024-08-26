import asyncio
import hashlib

from pytoniq import StateInit, Contract, LiteBalancer, WalletV4R2
from pytoniq_core import HashMap, begin_cell, Builder, Address, Slice


async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        assets = await client.run_get_method(address='EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r', method='get_assets', stack=[])
        print(assets)

        native_asset = -1

        if assets[0].load_uint(4) == 0:
            native_asset = 0
        else:
            native_asset = 1

        reserves = await client.run_get_method(address='EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r',
                                             method='get_reserves', stack=[])
        print(reserves)

        rate = (reserves[not native_asset] // 10**6) / (reserves[native_asset] // 10**9)
        print(rate)


asyncio.run(main())
