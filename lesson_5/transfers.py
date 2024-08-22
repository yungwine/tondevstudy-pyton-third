import asyncio
import hashlib

from pytoniq import StateInit, Contract, LiteBalancer, WalletV4R2
from pytoniq_core import HashMap, begin_cell, Builder, Address
from secret import mnemo


def get_transfer_body(amount: int, destination: Address, response_destination: Address, comment: str = ''):
    comment_cell = begin_cell().store_uint(0, 32).store_snake_string(comment).end_cell()
    return (begin_cell()
            .store_uint(0x0f8a7ea5, 32)
            .store_uint(0, 64)
            .store_coins(amount * 10**9)
            .store_address(destination)
            .store_address(response_destination)
            .store_bit_int(0)
            .store_coins(1)  # forward amount
            .store_bit_int(1)
            .store_ref(comment_cell)  # forward payload
            .end_cell()
            )


def get_burn_body(amount: int, response_destination: Address):
    return (begin_cell()
            .store_uint(0x595f07bc, 32)
            .store_uint(0, 64)
            .store_coins(amount * 10**9)
            .store_address(response_destination)
            .store_bit_int(0)
            .end_cell()
            )


async def transfer(client: LiteBalancer):
    body = get_transfer_body(
        amount=1000,
        destination='EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c',
        response_destination='UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9',
        comment='Hello from tondevstudy'
    )
    wallet = await WalletV4R2.from_mnemonic(client, mnemo)
    await wallet.transfer(destination='EQB0kGaLCLg57ocVM0M6lYRiruTWssqunNg2Pb8tpSBOZF4i', amount=2*10**8, body=body)


async def burn(client: LiteBalancer):
    body = get_burn_body(
        amount=1000,
        response_destination='UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9',
    )
    wallet = await WalletV4R2.from_mnemonic(client, mnemo)
    await wallet.transfer(destination='EQB0kGaLCLg57ocVM0M6lYRiruTWssqunNg2Pb8tpSBOZF4i', amount=2*10**8, body=body)


async def main():
    async with LiteBalancer.from_mainnet_config(trust_level=2) as client:
        # await transfer(client)
        await burn(client)

asyncio.run(main())
