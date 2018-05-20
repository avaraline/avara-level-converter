from Converter.helpers import *
from Converter.bspt.datatypes import *


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
