from Converter import resource
from Converter.converter import Converter
import Converter.pict.reader as pReader
import Converter.ledi.reader as lediReader
import Converter.bspt.reader as bsptReader
from lxml import etree
import argparse
import sys
import json

try:
    import audioop
except:
    print("python module `audioop` not found, no sounds will be exported")


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
    if not audioop:
        return
    for resid in resource.keys():
        snd_dict = resource[resid]
        snd_name = snd_dict['name']
        # raw_data = snd_dict['data']
        filename = "%d_%s" % (resid, snd_name)
        print("Nothing to do for HSND %s" % (filename))
        # TODO: read sound data


def save_shapes(resource):
    bsps = bsptReader.parse(resource)
    for bsp in bsps:
        filename = "%d_%s.avarabsp.json" % (bsp.res_id, bsp.name)
        print("Writing BSPT %s" % filename)
        with open(filename, "w") as bsp_file:
            json.dump(
                bsp.serialize(),
                bsp_file,
                separators=(',', ': '))


def save_maps(resource, set_ledi):
    for pict in resource.values():
        pictname = pict['name']

        if pictname not in set_ledi['items']:
            print("No LEDI found for '%s', skipping" % pictname)
            continue

        ops = pReader.parse(pict['data'])
        conv = Converter()
        mapxml = conv.convert(ops)

        ledi = set_ledi['items'][pictname]

        filename = ledi['title'] + "_" + pictname + '.xml'
        print("Writing level %s to %s" % (ledi['title'], filename))

        if mapxml is None:
            print("Error converting " + filename)
            continue

        xmlstring = etree.tostring(mapxml, pretty_print=True)
        with open(filename, 'w') as f:
            f.write(xmlstring.decode('macintosh'))


def convert_set(resources):
    set_ledi = lediReader.parse(resources['LEDI'])
    if 'HSND' in resources:
        save_hsnds(resources['HSND'])
    if 'BSPT' in resources:
        save_shapes(resources['BSPT'])
    save_maps(resources['PICT'], set_ledi)


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
