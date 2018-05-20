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


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def list_of_fixedsize_recs(data, offset, size, count, the_class):
    list_end = offset + (size * count)
    list_data = data[offset:list_end]
    return [the_class(x) for x in chunks(list_data, size)]


class BSP(object):
    # https://github.com/jmunkki/Avara/blob/master/src/Libraries/BSP/BSPResStructures.h
    def __init__(self, bsp_dict):
        self.name = bsp_dict['name']
        raw_data = bsp_dict['data']
        self.ref_count = bytes_to_unsigned_short(raw_data[0:2])
        self.lock_count = bytes_to_unsigned_short(raw_data[2:4])

        self.enclosure_point = UniquePoint(raw_data[4:20])
        self.enclosure_radius = bytes_to_fixed(raw_data[20:24])

        self.min_bounds = UniquePoint(raw_data[24:40])
        self.max_bounds = UniquePoint(raw_data[40:56])

        self.normal_count = bytes_to_unsigned_long(raw_data[56:60])
        self.edge_count = bytes_to_unsigned_long(raw_data[60:64])
        self.poly_count = bytes_to_unsigned_long(raw_data[64:68])
        self.color_count = bytes_to_unsigned_long(raw_data[68:72])
        self.point_count = bytes_to_unsigned_long(raw_data[72:76])
        self.vector_count = bytes_to_unsigned_long(raw_data[76:80])
        self.unique_edge_count = bytes_to_unsigned_long(raw_data[80:84])

        normal_offset = bytes_to_unsigned_long(raw_data[84:88])
        poly_offset = bytes_to_unsigned_long(raw_data[88:92])
        edge_offset = bytes_to_unsigned_long(raw_data[92:96])
        color_offset = bytes_to_unsigned_long(raw_data[96:100])
        point_offset = bytes_to_unsigned_long(raw_data[100:104])
        vector_offset = bytes_to_unsigned_long(raw_data[104:108])
        unique_edge_offset = bytes_to_unsigned_long(raw_data[108:112])

        self.normals = list_of_fixedsize_recs(
            raw_data,
            normal_offset,
            NormalRecordLength,
            self.normal_count,
            NormalRecord)

        self.polys = list_of_fixedsize_recs(
            raw_data,
            poly_offset,
            PolyRecordLength,
            self.poly_count,
            PolyRecord)

        # Edges are a list of shorts indexing verticies
        self.edges = list_of_fixedsize_recs(
            raw_data,
            edge_offset,
            2,
            self.edge_count,
            bytes_to_unsigned_short)

        self.colors = list_of_fixedsize_recs(
            raw_data,
            color_offset,
            ColorRecordLength,
            self.color_count,
            ColorRecord)

        self.points = list_of_fixedsize_recs(
            raw_data,
            point_offset,
            UniquePointLength,
            self.point_count,
            UniquePoint)

        # vectors are 4 part just like unique point
        self.vectors = list_of_fixedsize_recs(
            raw_data,
            vector_offset,
            UniquePointLength,
            self.vector_count,
            UniquePoint)

        self.unique_edges = list_of_fixedsize_recs(
            raw_data,
            unique_edge_offset,
            EdgeRecordLength,
            self.unique_edge_count,
            EdgeRecord)

    def __repr__(self):
        r = "%s - Total verticies: %d" % (self.name, self.point_count)
        r += "\nmin bound: %s" % self.min_bounds
        r += "\nmax bound: %s" % self.max_bounds
        r += "\npoints: %d" % self.point_count
        r += "\nedges: %s" % self.edges
        r += "\npolys: %s" % self.polys
        r += "\nnormals: %s" % self.normals
        r += "\ncolors: %s" % self.colors
        r += "\nvectors: %s" % self.vectors
        r += "\nunique edges: %s" % self.unique_edges
        return r


def parse(resource):
    bsps = []
    for res_id in resource.keys():
        bsp = BSP(resource[res_id])
        bsps.append(bsp)
    return bsps
