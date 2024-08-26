import asyncio
import hashlib

from pytoniq import StateInit, Contract, LiteBalancer, WalletV4R2
from pytoniq_core import HashMap, begin_cell, Builder, Address, Slice


def make_hash(key):
    return int.from_bytes(hashlib.sha256(key.encode()).digest(), 'big')


def get_keys():
    attrs = ['uri', 'name', 'description', 'image', 'image_data', 'symbol', 'decimals']
    res = {}
    for a in attrs:
        res[make_hash(a)] = a
    return res


def parse_metadata(cs: Slice):
    if cs.load_uint(8):
        return {'uri': cs.load_snake_string()}

    def value_deserializer(src: Slice):
        src = src.load_ref().begin_parse()
        if src.load_uint(8) == 0:
            return src.load_snake_string()
        return None

    def key_deserializer(src):
        return get_keys().get(int(src, 2))

    return cs.load_dict(256, value_deserializer=value_deserializer, key_deserializer=key_deserializer)


async def get_jetton(client: LiteBalancer, jetton_address: str):
    result = await client.run_get_method(jetton_address, 'get_jetton_data', [])
    content = parse_metadata(result[3].begin_parse())
    return {'total_supply': result[0], 'owner': result[2].load_address(), 'content': content}


async def get_wallet_address(client: LiteBalancer, jetton_address: str, user_address: str):
    cs = begin_cell().store_address(user_address).to_slice()
    result = await client.run_get_method(jetton_address, 'get_wallet_address', [cs])
    return result[0].load_address()


async def get_wallet_data(client: LiteBalancer, wallet_address: str):
    result = await client.run_get_method(wallet_address, 'get_wallet_data', [])
    return {'balance': result[0], 'owner_address': result[1].load_address(), 'jetton_master_address': result[2].load_address()}


async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        data = await get_jetton(client, 'EQDI4tLpoDYtLwfC_HEaI6TroiyPQ8NbGl1smxwm4ehByFQt')
        print(data)
        addr = await get_wallet_address(client, 'EQDI4tLpoDYtLwfC_HEaI6TroiyPQ8NbGl1smxwm4ehByFQt', 'EQB0kGaLCLg57ocVM0M6lYRiruTWssqunNg2Pb8tpSBOZF4i')
        print(addr)
        wallet_data = await get_wallet_data(client, 'EQB0kGaLCLg57ocVM0M6lYRiruTWssqunNg2Pb8tpSBOZF4i')
        print(wallet_data)


if __name__ == '__main__':
    asyncio.run(main())
