import struct


def bytes_to_string(some_bytes):
    return some_bytes.decode("macintosh")


def bytes_to_int(some_bytes):
    return struct.unpack('>i', some_bytes)[0]


def bytes_to_short(some_bytes):
    return struct.unpack('>h', some_bytes)[0]


def bytes_to_unsigned_short(some_bytes):
    return struct.unpack('>H', some_bytes)[0]


#def bytes_to_string(some_bytes):
#    return struct.unpack('>' + str(len(some_bytes)) + 's', some_bytes)[0]


def byte_to_unsigned_tiny_int(byte):
    # in python 3, slicing off a single byte spins off an int object
    return byte
    # tiny_int = b"\x00%b" % bytes(byte)[:1]
    # return struct.unpack('>h', tiny_int)[0]


def byte_to_signed_tiny_int(byte):
    num = byte # byte_to_unsigned_tiny_int(byte)
    if num > 127:
        return 0 - num
    return num
