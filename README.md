# avara-level-converter
Python 3 script that reads resource fork data and produces modern files

Original code by [sgsabbage](https://github.com/sgsabbage) as part of the [pavara](https://github.com/avaraline/pavara) project

Required Python modules: `lxml`, `wave` (probably included with python 3.6+)

### Usage
`python convert_levels.py path/to/file.rsrc`

The resource file will be parsed for PICT and other data. 
* Each PICT resource is given its own xml file matching the name found for the PICT resource.
* The LEDI resource is parsed to get the level names, TAGN identities, and pict file paths for each.
* Each HSND resource is exported as a 22.05khz WAV file, named as it is in the resource.
* TEXT resources are parsed to get set-level variables and shape/sound aliases
* Each BSPT resource should be exported to its own geometry file (unfinished) 

### Details
This first attempts to read the resource fork via HFS+ extended attributes, 
the "file/..namedfork/rsrc" method. This should be available on actual macos
machines as well as some \*nix HFS drivers (the FUSE HFS driver, the BSD one, 
etc) 

If that does not work, it attempts to assume that the file passed IS the 
resource fork, presented as binary data. This second type of file can be
produced on macos (at the time of this writing in May 2018) by doing 
a `cp path/to/file/..namedfork/rsrc path/to/file.rsrc`

The converter actually parses and loads all resources present in the file
(by nature of the binary resource fork format), which may be useful for other 
people looking to parse and work with resource fork data in general.
