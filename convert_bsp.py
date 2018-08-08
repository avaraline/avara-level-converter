#!/usr/bin/env python

from Converter.bspt.reader import BSP
import json, sys


if __name__ == '__main__':
    data = open(sys.argv[1], 'rb').read()
    bsp = BSP({'data': data, 'name': ''})
    d = bsp.serialize()
    out = {
        'points': [p[:3] for p in d['points']],
        'bounds': {
            'min': d['min_bounds'][:3],
            'max': d['max_bounds'][:3],
        },
        'center': d['enclosure_point'][:3],
        'radius1': d['enclosure_point'][3],
        'radius2': d['enclosure_radius'],
        'polys': [],
    }
    for idx, (fe, ec, normal_idx, fp, bp, pvis, rs) in enumerate(d['polys']):
        vec_idx, basept, color_idx, nvis = d['normals'][normal_idx]
        normal = d['vectors'][vec_idx][:3]
        color = d['colors'][color_idx]
        tris = d['triangles_poly'][idx]
        tri_points = d['triangles_verts_poly'][idx]
        out['polys'].append({
            'normal': normal,
            'color': color,
            'tris': [[tri_points[i] for i in t] for t in tris],
        })
    print(json.dumps(out, indent=2, sort_keys=True))
