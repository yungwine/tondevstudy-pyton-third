import asyncio
import hashlib

from pytoniq import StateInit, Contract, LiteBalancer, WalletV4R2
from pytoniq_core import HashMap, begin_cell, Builder, Address, Slice, Cell


async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        lib = Cell.one_from_boc('b5ee9c72010101010023000842028f452d7a4dfd74066b682365177259ed05734435be76b5fd4bd5d8af2b7c3d68')
        print(lib)
        cs = lib.begin_parse()
        cs.skip_bits(8)
        cell_hash = cs.load_bytes(32)
        print(cell_hash.hex())
        res = await client.get_libraries([cell_hash])
        print(res)
        print(res[cell_hash.hex()])
        print(res[cell_hash.hex()].hash.hex())


if __name__ == '__main__':
    asyncio.run(main())
