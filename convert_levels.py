from Converter import resource
from Converter.converter import Converter
import Converter.pict.reader as pReader
import Converter.ledi.reader as lediReader
import Converter.hsnd.reader as hsndReader
from lxml import etree
import argparse
import sys


def try_read(file):
    f = open(file, 'rb')
    data = f.read()

    if len(data) == 0:
        print("Couldn't read resource fork directly")

        f = open(file + '/..namedfork/rsrc', 'rb')
        data = f.read()

        if len(data) == 0:
            print("Couldn't read resource fork from /..namedfork/")
            return False
        else:
            return data
    else:
        return data


def get_resources(file):
    data = try_read(file)
    if data is False:
        print("No data to read")
        sys.exit(1)
    reader = resource.Reader()
    resources = reader.parse(data)

    return resources


def save_hsnds(resource):
    hsndReader.parse(resource)

def convert_set(resources):
    set_ledi = lediReader.parse(resources['LEDI'])
    save_hsnds(resources['HSND'])
    picts_r = resources['PICT']
    for pict in picts_r.values():
        ops = pReader.parse(pict['data'])
        conv = Converter()
        mapxml = conv.convert(ops)
        pictname = pict['name']
        filename = pictname + '.xml'
        ledi = set_ledi['items'][pictname]

        print("Writing level %s to %s" % (ledi['title'], filename))

        if mapxml is None:
            print("Error converting " + filename)
            continue

        xmlstring = etree.tostring(mapxml, pretty_print=True).decode('macintosh')
        f = open(filename, 'w')
        f.write(xmlstring)
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='file')

    args = parser.parse_args()

    resources = get_resources(args.file)
    # print resources.keys()
    # print resources['TMPL']
    # print resources['LEDI'][128]['data']
    print("Found resources: %s" % ", ".join(resources.keys()))
    convert_set(resources)
