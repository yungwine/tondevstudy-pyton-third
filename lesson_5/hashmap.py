from pytoniq_core import HashMap, begin_cell, Builder, Slice, Address


def key_serializer(src):
    return len(src)


def value_serializer(src, dest: Builder):
    return dest.store_uint(src, 16)


hm = HashMap(256, key_serializer=key_serializer, value_serializer=value_serializer)

hm.set('333', 15)
hm.set('4444', 10)
hm.set('55555', 20)

hm_cell = hm.serialize()
print(hm_cell)


def key_deserializer(src):
    src = int(src, 2)
    return str(src) * src


def value_deserializer(src: Slice):
    return src.load_uint(16)


hm_parsed = HashMap.parse(hm_cell.begin_parse(), 256, key_deserializer=key_deserializer, value_deserializer=value_deserializer)


hm2 = HashMap(267).with_coins_values()

hm2.set(Address('EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'), 100)
hm2.set(Address('UQCPCZU37-aComPLgaQBcOkevn4x5GJHSfZsFt6eF9DpHZH9'), 200*10**9)

hm2_cell = hm2.serialize()
print(hm2_cell)

hm2_slice = hm2_cell.begin_parse()


def key_deserializer2(src):
    return begin_cell().store_bits(src).to_slice().load_address()


def value_deserializer2(src: Slice):
    return src.load_coins()


d = hm2_slice.load_hashmap(267, key_deserializer=key_deserializer2, value_deserializer=value_deserializer2)

print(d)


real_hm = begin_cell().store_dict(hm2_cell).end_cell()
print(real_hm)

print(real_hm.begin_parse().load_dict(267))
