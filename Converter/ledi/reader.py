from Converter.helpers import *


def tiny_int_from_single_byte(byte):
    tiny_int = b"\x00%b" % byte
    return struct.unpack('>h', tiny_int)[0]


def parse(resource):
    # LEDI resource is always at index 128
    ledis_raw = resource[128]['data']

    ledi = {}  # results
    # each record is separated by 9 null values
    terminator = b''.join(b'\x00' for x in range(9))

    set_ident = bytes_to_string(ledis_raw[:4])
    set_length = bytes_to_short(ledis_raw[4:6])
    ledi['ident'] = set_ident
    ledi['count'] = set_length
    ledi['items'] = {}
    ledis_raw_list = ledis_raw[6:].split(terminator)[:-1]
    for ledi_raw in ledis_raw_list:
        # some of these are padded with nulls
        # (to be an even number of bytes i guess)
        ledi_raw = ledi_raw.strip(b"\x00")
        this_ledi = {}
        ident = bytes_to_string(ledi_raw[:4])

        the_data = ledi_raw[4:]
        strs = []
        while len(the_data) > 0:
            str_len = tiny_int_from_single_byte(the_data[:1])
            astr = the_data[1:str_len + 1]
            strs.append(astr)
            the_data = the_data[str_len + 1:]
            if the_data[:1] == b'\x00':
                the_data = the_data[1:]

        this_ledi['ident'] = ident
        this_ledi['title'] = bytes_to_string(strs[0])
        this_ledi['msg'] = bytes_to_string(strs[1])
        this_ledi['file'] = bytes_to_string(strs[2])

        ledi['items'][this_ledi['file']] = this_ledi

    return ledi
