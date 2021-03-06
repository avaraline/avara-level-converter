# avara-level-converter
Python 3 script that reads [resource fork data](https://en.wikipedia.org/wiki/Resource_fork) and produces [modern](https://www.google.com/search?q=mac+os+system+7+release+date) files that can be read on [real](http://www.vintage-computer.com/powerbook170.shtml) computers.

Original code by [sgsabbage](https://github.com/sgsabbage) as part of the [pavara](https://github.com/avaraline/pavara) project

Required Python modules: `lxml`, `wave`, `json`, `argparse`, `struct`

### Usage
`python convert_levels.py path/to/file.rsrc`

The resource file will be parsed for PICT and other data. 
* Each PICT resource is given its own xml file.
* The LEDI resource is parsed to get the name, tag, and pict file paths for each level in the set. Or it's supposed to, it doesn't work on sets that have level completion dependencies just yet.
* TEXT resources are parsed to get set-level variables and shape/sound aliases.
* Each BSPT resource is exported to a json file that contains a representation of [Avara's BSP format](https://github.com/jmunkki/Avara/blob/a328b9e502d549364439c1c0ef4310a1e3a136dc/src/Libraries/BSP/BSPResStructures.h). 

### Details
This first attempts to read the resource fork via HFS+ extended attributes, 
the "file/..namedfork/rsrc" method. This should be available on actual macos
machines as well as some \*nix HFS drivers (the FUSE HFS driver, the BSD one, 
etc) 

If that does not work, it attempts to assume that the file passed IS the 
resource fork, presented as binary data. This second type of file can be
produced on macos (at the time of this writing in May 2018) by doing 
a `cp path/to/file/..namedfork/rsrc path/to/file.rsrc`. With these files
in hand you can run the converter on anything that runs Python instead of 
being limited to macos.

The converter actually parses and loads all resources present in the file
(by nature of the binary resource fork format), which may be useful for other 
people looking to parse and work with resource fork data in general.

### BSP JSON format

* There's a list of points, edges, polygons, normals, colors, vectors, "unique edges"
* each edge number corresponds to a point
* each polygon refers to one or more edge numbers
* each polygon also refers to a normal
* each normal refers to a color 
* each color record also contains a cache of different shades of that color (for white light only)
* I do not export this cache for that reason and instead colors are in 4 floats in RGBA
* if you have `numpy` and `triangle` installed, included are `triangles_polys` and `riangles_verts_polys`
* these triangulate polygonal faces in avara bsps (in Avara, bsp faces were filled all at once, no matter how many vertexes or edges!)
* `triangles_verts_polys` will be a list of verts in each poly for each poly so `poly[0]` will have `triangles_verts_polys[0]`, itself a list of vert indexes
* the triangles_polys array contains a list of triangle faces that are indexes into triangles_verts_polys
* I needed this to use an engine that only expected quads/triangles (as most do these days?!) 
