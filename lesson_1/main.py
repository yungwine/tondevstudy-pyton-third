import asyncio

from pytoniq import LiteClient, Contract, WalletV4R2
from pytoniq_core import Cell, Address, StateInit, begin_cell

from secret import mnemo

code_boc = 'b5ee9c7241010c0100bd000114ff00f4a413f4bcf2c80b01020120020b02014803080202ce0407020120050600671b088831c02456f8007434c0cc1c6c244c383c0074c7f4cfcc4060841fa1d93beea6f4c7cc3e1080683e18bc00b80c2103fcbc20001d3b513434c7c07e1874c7c07e18b46000194f842f841c8cb1fcb1fc9ed54802016e090a000db5473e003f0830000db63ffe003f0850005af2d31fd33f31d31ff001f84212baf2e3e9f8000182107e8764efba9bd31f30f84201a0f862f002e030840ff2f04a2d931d'

code = Cell.one_from_boc(code_boc)

data = begin_cell().store_uint(101, 32).store_uint(0, 32).end_cell()

state_init = StateInit(code=code, data=data)

address = Address((0, state_init.serialize().hash))
print(address.to_str(is_bounceable=False))


async def external(contract):
    body = (begin_cell()
            .store_uint(0x7e8764ef, 32)  # op
            .store_uint(0, 64)  # query_id
            .store_uint(1, 32)  # current_value
            .store_uint(3, 32)  # increase by
            .end_cell())

    await contract.send_external(state_init=state_init, body=body)


async def main():
    async with LiteClient.from_mainnet_config(ls_i=7, trust_level=2) as client:
        print(await client.get_masterchain_info())
        contract = await Contract.from_state_init(client, 0, state_init)

        wallet = await WalletV4R2.from_mnemonic(client, mnemo)
        print(wallet)

        body = (begin_cell()
                .store_uint(0x7e8764ef, 32)  # op
                .store_uint(0, 64)  # query_id
                .store_uint(2, 32)  # increase by
                .end_cell())

        # await wallet.transfer(destination=address.to_str(is_bounceable=False), amount=5 * 10**6, state_init=state_init, body=body)
        result = await client.run_get_method(address, 'get_counter', stack=[])
        print(result)


asyncio.run(main())
