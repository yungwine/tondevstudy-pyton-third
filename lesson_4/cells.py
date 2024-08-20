import base64

from pytoniq_core import Builder, Cell, Slice, begin_cell, Address

b = begin_cell().store_uint(5, 32)
c = b.end_cell()

address = 'UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9'

b2 = begin_cell().store_ref(c).store_ref(c).store_coins(100).store_address(address)

# print(b2)

c2 = b2.end_cell()

print(c2.hash)
boc = c2.to_boc()
print(boc.hex(), base64.b64encode(boc))

c3 = Cell.one_from_boc('b5ee9c7201010201002d0002451648011e132a6fdfcd0544c797034802e1d23d7cfc63c8c48e93ecd82dbd3c2fa1d23b0101000800000005')
print(c3)

b3 = c3.to_builder()
print([b3])

s3 = c3.begin_parse()

print([s3])

print(s3.preload_coins())
print(s3.load_coins())
print(s3.load_ref() == c)
s3.load_ref()
addr = s3.load_address()
print(s3)

print(addr)
print(addr.wc, addr.hash_part)
print(addr.to_str(is_bounceable=False))
print(addr.to_str(is_user_friendly=False))
print(addr.to_str(is_url_safe=False))
print(addr.to_str(is_test_only=True), addr.to_str(is_test_only=True, is_bounceable=False))

Address('UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9')
Address((0, b'\x8f\t\x957\xef\xe6\x82\xa2c\xcb\x81\xa4\x01p\xe9\x1e\xbe~1\xe4bGI\xf6l\x16\xde\x9e\x17\xd0\xe9\x1d'))


print(begin_cell().store_snake_string('abc'*100).end_cell())
