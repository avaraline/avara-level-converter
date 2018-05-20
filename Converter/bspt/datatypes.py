from Converter.helpers import *


UniquePointLength = 16


class UniquePoint(object):
    size = 16

    def __init__(self, raw_data):
        assert(len(raw_data) == UniquePointLength)
        self.x = bytes_to_fixed(raw_data[0:4])
        self.y = bytes_to_fixed(raw_data[4:8])
        self.z = bytes_to_fixed(raw_data[8:12])
        self.w = bytes_to_fixed(raw_data[12:16])

    def __repr__(self):
        tup = (self.x, self.y, self.z, self.w)
        return "UniquePoint(%f %f %f %f)" % tup


NormalRecordLength = 8


class NormalRecord(object):
    def __init__(self, raw_data):
        assert(len(raw_data) == NormalRecordLength)
        self.normal_index = bytes_to_unsigned_short(raw_data[0:2])
        self.base_point_index = bytes_to_unsigned_short(raw_data[2:4])
        self.color_index = bytes_to_unsigned_short(raw_data[4:6])
        self.visibility_flags = bytes_to_unsigned_short(raw_data[6:8])

    def __repr__(self):
        tup = (self.normal_index, self.base_point_index, self.color_index, self.visibility_flags)
        return "NormalRecord (%d %d %d %d)" % tup


EdgeRecordLength = 4


class EdgeRecord(object):
    def __init__(self, raw_data):
        assert(len(raw_data) == EdgeRecordLength)
        self.a = bytes_to_unsigned_short(raw_data[0:2])
        self.b = bytes_to_unsigned_short(raw_data[2:4])

    def __repr__(self):
        tup = (self.a, self.b)
        return "EdgeRecord (%d %d)" % tup


PolyRecordLength = 16


class PolyRecord(object):
    def __init__(self, raw_data):
        assert(len(raw_data) == PolyRecordLength)
        self.first_edge = bytes_to_unsigned_short(raw_data[0:2])
        self.edge_count = bytes_to_unsigned_short(raw_data[2:4])
        self.normal_index = bytes_to_unsigned_short(raw_data[4:6])
        self.front_poly = bytes_to_unsigned_short(raw_data[6:8])
        self.back_poly = bytes_to_unsigned_short(raw_data[8:10])
        self.visibility = bytes_to_unsigned_short(raw_data[10:12])
        self.reserved = bytes_to_unsigned_long(raw_data[12:16])

    def __repr__(self):
        tup = (self.first_edge, self.edge_count, self.normal_index, self.front_poly, self.back_poly, self.visibility)
        return "PolyRecord (%d %d %d %d %d %d)" % tup


ColorRecordLength = (32 * 2) + 4


class ColorRecord(object):
    def __init__(self, raw_data):
        assert(len(raw_data) == ColorRecordLength)
        self.color = bytes_to_long(raw_data[0:4])
        # colorCache[32] (COLORCACHESIZE)
        self.color_cache = [bytes_to_unsigned_short(x) for x in chunks(raw_data[4:ColorRecordLength], 2)]

    def __repr__(self):
        tup = (self.color, self.color_cache)
        return "ColorRecord (%s %s)" % tup
