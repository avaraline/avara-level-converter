# avara-level-converter
Python 3 script that reads resource fork PICT data and produces files in an XML format

Original code by [sgsabbage](https://github.com/sgsabbage) as part of the [pavara](https://github.com/avaraline/pavara) project

### Usage
`python convert_levels.py path/to/file.rsrc`

The resource file will be parsed for PICT and other data. Each PICT resource 
is given its own xml file matching the name found for the PICT resource. 

### Details
This first attempts to read the resource fork via HFS+ extended attributes, 
the "file/..namedfork/rsrc" method. If that does not work, it attempts to assume
that the file passed IS the resource fork as binary data. This second type of file
can be produced on macos (at the time of this writing) by doing 
a `cp path/to/file/..namedfork/rsrc path/to/file.rsrc`

The converter actually parses and loads all resources present in the file
(by nature of the binary resource fork format), which may be useful for other 
people looking to parse and work with resource fork data in general.
