from Converter import resource
from Converter.converter import Converter
import Converter.pict.reader as pReader
import Converter.ledi.reader as lediReader
import Converter.bspt.reader as bsptReader
from lxml import etree
import wave
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
    for resid in resource.keys():
        snd_dict = resource[resid]
        snd_name = snd_dict['name']
        raw_data = snd_dict['data']
        filename = snd_name + ".wav"
        print("Writing HSND %s as %s" % (snd_name, filename))
        with wave.open(filename, 'wb') as wavfile:
            wavfile.setparams((2, 2, 22050, 0, 'NONE', 'NONE'))
            wavfile.writeframes(raw_data)


def save_shapes(resource):
    bsps = bsptReader.parse(resource)
    for bsp in bsps:
        # TODO: save something
        # (we have data but no intermediary format)
        # print(bsp)
        print("Nothing to do for BSPT %s" % bsp.name)


def save_maps(resource, set_ledi):
    for pict in resource.values():
        ops = pReader.parse(pict['data'])
        conv = Converter()
        mapxml = conv.convert(ops)
        pictname = pict['name']
        filename = pictname + '.xml'
        if pictname not in set_ledi['items']:
            print("No LEDI found for %s, skipping" % pictname)
            continue
        ledi = set_ledi['items'][pictname]

        print("Writing level %s to %s" % (ledi['title'], filename))

        if mapxml is None:
            print("Error converting " + filename)
            continue

        xmlstring = etree.tostring(mapxml, pretty_print=True)
        f = open(filename, 'w')
        f.write(xmlstring.decode('macintosh'))
        f.close()


def convert_set(resources):
    set_ledi = lediReader.parse(resources['LEDI'])
    save_hsnds(resources['HSND'])
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
